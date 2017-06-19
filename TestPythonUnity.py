import  re
import  string
import  os
import shutil
import time
def CopyFiles(scr: string,dst: string):
 if os.path.exists(dst + '/LoadAR'): # 创建LoadAR目录,如果已经存在了就先删除了
  shutil.rmtree(dst + '/LoadAR')
 os.makedirs(dst + '/LoadAR')
 # 复制各个文件
 shutil.copytree(scr+"/Classes",dst+"/LoadAR/Classes")
 shutil.copytree(scr+"/Data",dst+"/LoadAR/Data")
 shutil.copytree(scr+"/Libraries",dst+"/LoadAR/Libraries")
 shutil.copyfile(scr+"/MapFileParser.sh",dst+"/LoadAR/MapFileParser.sh")
 return

CopyFiles('/Users/sunyongji/Desktop/staturdayUnity','/Users/sunyongji/Desktop/TestPythonUnity')

