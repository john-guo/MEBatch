from __future__ import division
from argparse import ArgumentParser
import urllib3
import mimetypes
from urllib import request
import ntpath
import json
import math
import os
from PIL import Image, ImageFont, ImageDraw

SPACING = 2
LINE_SPACING = 4
UPLOAD_URL = 'https://moeka.me/mangaEditor/upload/'
TRANSLATE_URL = 'https://moeka.me/mangaEditor/translate/'
font = ImageFont.truetype('simhei.ttf', 16)
mimetypes.init()
urllib3.disable_warnings()

def list_files(in_path):
    files = []
    for (dirpath, dirnames, filenames) in os.walk(in_path):
        files.extend(filenames)
        break

    return files

def build_parser():
    parser = ArgumentParser()
    parser.add_argument('--in-path', type=str,
                        dest='in_path',help='dir to translate',
                        metavar='IN_PATH', required=True)

    help_out = 'destination dir of translate'
    parser.add_argument('--out-path', type=str,
                        dest='out_path', help=help_out, metavar='OUT_PATH',
                        required=True)
    return parser

def process(in_file, out_file):
    http = urllib3.PoolManager()
    url = request.pathname2url(in_file)
    mimetype = mimetypes.guess_type(url)[0]
    basename = ntpath.basename(in_file)
    
    with open(in_file, mode='rb') as fp:
        file_data = fp.read()

    r = http.request('POST', UPLOAD_URL, fields={'files': (basename, file_data, mimetype)})
    json_txt = r.data.decode('utf-8')
    # with open(out_file + '.json', 'w') as fp:
    #     fp.write(json_txt)
    json_obj = json.loads(json_txt)
    width = json_obj['dim']['cols']
    height = json_obj['dim']['rows']

    file_id = json_obj['id']
    im = Image.open(in_file)
    im = im.convert('RGB')
    draw = ImageDraw.Draw(im)

    width_ratio = im.width / width
    height_ratio = im.height / height

    # ext = os.path.splitext(in_file)[1][1:]

    for i in range(json_obj['balloonCount']):
        ballon = json_obj[str(i)]
        ballon_url = request.urlparse(ballon['originalURL'])
        fname = ntpath.basename(ballon_url.path)
        r = http.request('POST', TRANSLATE_URL, fields={'fname':fname, 'id':file_id, 'lang':'ja'})
        json_translated = json.loads(r.data.decode('utf-8'))
        translatedText = json_translated['translatedText']
        if not translatedText:
            continue

        boundingRect = ballon['boundingRect']
        x0 = boundingRect['x']
        y0 = boundingRect['y']
        x1 = x0 + boundingRect['width']
        y1 = y0 + boundingRect['height']

        textRectCount = ballon['textRectCount']

        for rect in range(textRectCount):
            textRect = ballon['textRect'][str(rect)]
            x0 = math.floor(width_ratio * textRect['x'] + .5)
            y0 = math.floor(height_ratio * textRect['y'] + .5)
            x1 = x0 + math.floor(width_ratio * textRect['width'] + .5)
            y1 = y0 + math.floor(height_ratio * textRect['height'] + .5)
            draw.rectangle((x0,y0,x1,y1),fill=(255,255,255))
        
        currentTextRect = 0
        textRect = ballon['textRect'][str(currentTextRect)]
        target_x = math.floor(textRect['x'] * width_ratio + .5)
        target_y = math.floor(textRect['y'] * height_ratio + .5)
        target_width = math.floor(textRect['width'] * width_ratio + .5)
        target_height = math.floor(textRect['height'] * height_ratio + .5)
        start_x = target_x + target_width
        start_y = target_y
        linemaxsize = 0

        for ch in translatedText:
            ch_w,ch_h = draw.textsize(ch, spacing=0, font=font)
            if linemaxsize < ch_w:
                linemaxsize = ch_w
            if start_y + ch_h > target_y + target_height:
                start_x -= linemaxsize + LINE_SPACING
                start_y = target_y
            
            if start_x - ch_w < target_x:
                currentTextRect += 1
                if currentTextRect >= textRectCount:
                    break
                textRect = ballon['textRect'][str(currentTextRect)]
                target_x = math.floor(textRect['x'] * width_ratio + .5)
                target_y = math.floor(textRect['y'] * height_ratio + .5)
                target_width = math.floor(textRect['width'] * width_ratio + .5)
                target_height = math.floor(textRect['height'] * height_ratio + .5)
                start_x = target_x + target_width
                start_y = target_y
                linemaxsize = ch_w

            ch_x = start_x - ch_w
            ch_y = start_y
            start_y += ch_h + SPACING
            draw.text((ch_x, ch_y), ch, font=font, fill=(0,0,0))

        # need_size = draw.textsize(translatedText[0], spacing=0, font=font)
        # texttodraw = translatedText
        # if need_size > target_size:
        #     texttodraw = ''
        #     lines = math.ceil(need_size / target_size)
        #     textperline = math.ceil(len(translatedText) / lines)
        #     for j in range(lines):
        #         texttodraw += translatedText[j*textperline:(j+1)*textperline]
        #         texttodraw += os.linesep
        # draw.text((target_x, target_y), texttodraw, font=font, spacing=4, fill=(0,0,0,255), direction='ttb')
    
    im.save(out_file)

def main():
    parser = build_parser()
    opts = parser.parse_args()    

    files = list_files(opts.in_path)
    full_in = [os.path.join(opts.in_path,x) for x in files]
    full_out = [os.path.join(opts.out_path,x) for x in files]

    for i in range(len(full_in)):
        in_image = full_in[i]
        out_image = full_out[i]
        process(in_image, out_image)

if __name__ == '__main__':
    main()

