# MEBatch

## 目的  

这是一个基于[https://moeka.me/mangaEditor/] 在线漫画汉化编辑器进行自动汉化批处理作业的Python脚本，目前功能可以批处理输入目录下所有图片文件，所使用的对话气泡抽取以及日文文本识别翻译均使用mangaEditor的网络服务，如果没有网络或者mangaEditor停止服务本脚本将不能正常工作，具体使用请看后面介绍。

## 安装  

windows新手用户推荐先安装Anaconda[https://repo.anaconda.com/archive/Anaconda3-5.2.0-Windows-x86_64.exe]  
安装完Anaconda后打开Anaconda Prompt, 可能Anaconda默认带的python版本较低，建议先更新python以免后面出现报错:  
`conda upgrade pip`  
出现提示按Y即可  
然后进入项目目录运行:  
`pip install -r requirements.txt`  
如果显示类似如下提示就说明没问题了  
`Requirement already satisfied: urllib3 in c:\anaconda3_64\lib\site-packages (from -r requirements.txt (line 1)) (1.22)`  
`Requirement already satisfied: pillow in c:\anaconda3_64\lib\site-packages (from -r requirements.txt (line 2)) (5.1.0)`  
到此就算安装完毕  
  
## 使用  

打开anaconda prompt在脚本所在目录中运行：  
`python mebatch.py --in-path 漫画图片全路径 --out-path 翻译后图片所要放的路径`  
  
比如假设脚本所在目录是 C:\mebatch ， 漫画图片都放在 C:\in 目录下，想把翻译的图片放在 C:\out 目录下，打开Anaconda Prompt，输入如下命令:  
`C:`  
`cd C:\mebatch`  
`python mebatch.py --in-path C:\in --out-path C:\out`  
等执行完后就能在C:\out里找到自动汉化完成的漫画图片。

## 限制  

由于是自动化处理，所以完全依赖mangaEditor的识别能力，并且由于是自动化处理，翻译以及嵌字效果都达不到人工操作的理想程度，而且很有可能产生很糟糕的效果，这时可用LabelPlus[http://noodlefighter.com/label_plus/] 来进行手工辅助汉化处理  
并且再次说明**本脚本极度依赖mangaEditor**
