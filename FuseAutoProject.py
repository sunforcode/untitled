import re
import string
import  os
import shutil

unityPath = '/Users/CharlyZhang/Desktop/XCode/Unity-iPhone.xcodeproj'
targetPath = '/Users/CharlyZhang/Desktop/TestPythonUnity/TestPythonUnity.xcodeproj'

targetPath = '/Users/sunyongji/Desktop/TestPythonUnity/TestPythonUnity.xcodeproj'
unityPath = '/Users/sunyongji/Desktop/staturdayUnity/Unity-iPhone.xcodeproj'



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

## 打开两个文件
targetFileDic = {}
with open(targetFilePath, 'r+') as targetFile:
    fileContent = targetFile.read()
    #目标工程的主分组
    #分组
    sectionPattern = '/\* Begin (.*) section \*/'
    pattersn = re.compile(sectionPattern)
    result = pattersn.findall(fileContent)
    if result:
       for str in result:
          s = '/\* Begin %s section \*/([.\s\S]*)/\* End %s section \*/' % (str, str)
          pattersn1 = re.compile(s)
          result1 = pattersn1.findall(fileContent)
          if result1:
              targetFileDic[str] = result1[0]

unityDic = {}
# 1.打开Unity的文件路径并格式化
with open(unityFilePath, 'r') as f:
    UnityFileContent = f.read()
    sectionPattern = '/\* Begin (.*) section \*/'
    UnityPattersn = re.compile(sectionPattern)
    UnityResult = UnityPattersn.findall(UnityFileContent)
    if UnityResult:
        for str in UnityResult:
            s = '/\* Begin %s section \*/([.\s\S]*)/\* End %s section \*/' % (str, str)
            pattersn1 = re.compile(s)
            result1 = pattersn1.findall(UnityFileContent)
            if result1:
                unityDic[str] = result1[0]

## 获取主RootObject
rootObjectString = ''
rootobjectPattern = re.compile('rootObject = ([a-zA-Z0-9]*) /\*')
rootObjectResult = rootobjectPattern.findall(fileContent)
if rootObjectResult:
    rootObjectString = rootObjectResult[0]

## unity的主分组
PBXProjectPattern = re.compile('mainGroup = ([A-F0-9]{24})')
UnityMaingroup = ''
UnityGroupString = ''
UnityMainGroupResult = PBXProjectPattern.findall(UnityFileContent)
if UnityMainGroupResult:
    UnityMaingroup = UnityMainGroupResult[0]

PBXGroupString = unityDic['PBXGroup']
PBXGroupPattern = re.compile('([.\s\S]*?};)')
PBXGroupResult = PBXGroupPattern.findall(PBXGroupString)
if PBXGroupResult:
    for PBXGroupSingle in PBXGroupResult:
        if PBXGroupSingle.__contains__(UnityMaingroup):
            PBXGroupSingle = PBXGroupSingle.replace("name = CustomTemplate;", "name = LoadAR;")
            UnityGroupString += PBXGroupSingle
        elif PBXGroupSingle.__contains__('Unity-iPhone Tests'):
            continue
        elif PBXGroupSingle.__contains__('/* Libraries */ = {'):
            PBXGroupSingle = PBXGroupSingle.replace('path = Libraries;',
                                                    'path = LoadAR/Libraries;\n\t\t\t\tname = Libraries;\n')
            UnityGroupString += PBXGroupSingle
            pass
        elif PBXGroupSingle.__contains__('/* Classes */ = {'):
            PBXGroupSingle = PBXGroupSingle.replace('path = Classes;',
                                                    'path = LoadAR/Classes;\n\t\t\t\tname = Classes;\n')
            UnityGroupString += PBXGroupSingle
            pass
        else:
            UnityGroupString += PBXGroupSingle
    unityDic['PBXGroup'] = UnityGroupString

# PBXProject 获取主目录的ID 2D9A4B551EDE903E000D8470
targetResultString = ''
PBXProjectString = targetFileDic['PBXProject']
# print(PBXProjectString)
PBXProjectResult = PBXProjectPattern.findall(PBXProjectString)
if PBXProjectResult:
    TargetMaingroup = PBXProjectResult[0]
targetFileGroupString = targetFileDic['PBXGroup']
PBXGroupPattern = re.compile('([.\s\S]*?};)')
PBXGroupResult = PBXGroupPattern.findall(targetFileGroupString)
if PBXGroupResult:
    for PBXGroupSingle in PBXGroupResult:
        containMain = PBXGroupSingle.__contains__(TargetMaingroup)
        containLoadAR = not PBXGroupSingle.__contains__('LoadAR')
        if (containMain and containLoadAR):
            PBXGroupSingle = PBXGroupSingle.split('children = (')[
                                 0] + 'children = (\n' + '\t\t\t\t' + UnityMaingroup + ' /* LoadAR */,' + \
                             PBXGroupSingle.split('children = (')[1] + '\n' + unityDic['PBXGroup']
            targetResultString += PBXGroupSingle
        else:
            targetResultString += PBXGroupSingle
            pass
    targetResultString = targetResultString.replace('SOURCE_ROOT', '\"<group>\"')
    targetFileDic['PBXGroup'] = targetResultString







# 重新写入文件中
resultString = ''
for key in targetFileDic:
    begin = "/* Begin %s section */"%key
    end =  "/* End %s section */\n"%key
    content = targetFileDic[key]
    resultString =resultString + begin + content + end

resultString = "// !$*UTF8*$!\n{\n\t\tarchiveVersion = 1;\n\tclasses = {\n\t};\n\tobjectVersion = 46;\n\tobjects = {"+resultString + "};\nrootObject = "+rootObjectString+" /* Project object */;\n}"
with open(targetFilePath, "r+") as testProject:
    testProject.truncate()
    testProject.write(resultString)
    print('success')

