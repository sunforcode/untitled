import re
import string
import  os
import shutil

unityPath = '/Users/CharlyZhang/Desktop/XCode/Unity-iPhone.xcodeproj'
targetPath = '/Users/CharlyZhang/Desktop/TestPythonUnity/TestPythonUnity.xcodeproj'

unityFilePath = unityPath + '/project.pbxproj'
targetFilePath = targetPath + '/project.pbxproj'

targetProjectName = 'TestPythonUnity'
unityProjectName = 'Unity-iPhone'

##备份
isMakeUpOrRevoke = False #False 重置  True 备份
def makeBackUpFile(targetFilePath):
    targetProjectPath = targetFilePath + '/project.pbxproj'
    targetBackUpPath = targetFilePath + '/backUp'
    if not os.path.exists(targetBackUpPath):
        os.makedirs(targetBackUpPath)
    shutil.copyfile(targetProjectPath,targetBackUpPath +'/project.pbxproj')

def revokeBackUpFile(targetFilePath):
    targetProjectPath = targetFilePath + '/project.pbxproj'
    targetBackUpPath = targetFilePath + '/backUp'
    shutil.copyfile(targetBackUpPath +'/project.pbxproj',targetProjectPath)

if isMakeUpOrRevoke:
    makeBackUpFile(targetPath)
else:
    revokeBackUpFile(targetPath)

##复制文件
def CopyFiles(scr: string,dst: string):
 scr = scr[:scr.rindex('/')]
 dst = dst[:dst.rindex('/')]
 if os.path.exists(dst + '/LoadAR'): # 创建LoadAR目录,如果已经存在了就先删除了
  shutil.rmtree(dst + '/LoadAR')
 os.makedirs(dst + '/LoadAR')
 # 复制各个文件
 shutil.copytree(scr+"/Classes",dst+"/LoadAR/Classes")
 shutil.copytree(scr+"/Data",dst+"/LoadAR/Data")
 shutil.copytree(scr+"/Libraries",dst+"/LoadAR/Libraries")
 shutil.copyfile(scr+"/MapFileParser.sh",dst+"/LoadAR/MapFileParser.sh")
 return

CopyFiles(unityPath,targetPath)


## 最后一步重新把
for key in targetDic:
    begin = "/* Begin %s section */"%key
    end =  "/* End %s section */\n"%key
    content = targetDic[key]
    resultString =resultString + begin + content + end

resultString = "// !$*UTF8*$!\n{\n\t\tarchiveVersion = 1;\n\tclasses = {\n\t};objectVersion = 46;\n\tobjects = {\n\t"+resultString + "};\nrootObject = 2DE8B4DD1ED4098300C1959B /* Project object */;\n}"
with open(targetXcodePath, "r+") as testProject:
    print(resultString)
    # testProject.write(resultString)
    print('success')

