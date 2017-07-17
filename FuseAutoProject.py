import re
import string
import  os
import shutil
import time

unityPath = '/Users/CharlyZhang/Desktop/ARbook0714/Unity-iPhone.xcodeproj'
targetPath = '/Users/CharlyZhang/Git/OrangeCube/E-Publishing.xcodeproj'
targetName = 'FounderReader'

unityFilePath = unityPath + '/project.pbxproj'
targetFilePath = targetPath + '/project.pbxproj'

removePath = targetPath + '/remove'+'/project.pbxproj'

targetProjectName = 'FounderReader'
unityProjectName = 'Unity-iPhone'
unityTargetName = 'Unity-iPhone'
projectTargetName = 'FounderReader'
##备份
isMakeUpOrRevoke = True #False 重置  True 备份
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

def CopyAPPController(path: string):
    path = path[:path.rindex('/')]
    dst = path + '/LoadAR/Classes'
    shutil.copyfile(path + "/UnityAppController.h", dst + "/UnityAppController.h")
    shutil.copyfile(path + "/UnityAppController.mm", dst + "/UnityAppController.mm")
    pass


def CopyReMoveFile(srcPath,dstPath):
    src = srcPath + '/project.pbxproj'
    dst = dstPath + '/remove/project.pbxproj'
    shutil.copyfile(src, dst)
    pass


CopyFiles(unityPath,targetPath)
CopyAPPController(targetPath)




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

removeFileContent = ''
removeFileDic = {}

with open(removePath,'r') as removeFile:
    removeFileContent = removeFile.read()
    sectionPattern = '/\* Begin (.*) section \*/'
    UnityPattersn = re.compile(sectionPattern)
    UnityResult = UnityPattersn.findall(removeFileContent)
    if UnityResult:
        for str in UnityResult:
            s = '/\* Begin %s section \*/([.\s\S]*)/\* End %s section \*/' % (str, str)
            pattersn1 = re.compile(s)
            result1 = pattersn1.findall(removeFileContent)
            if result1:
                removeFileDic[str] = result1[0]

#获取三个分组中的id
rmGroupArray = []
rmBuildFileArray = []
rmFileRefArray = []
rmResourceBuildArray = []
removeGroupPattern = re.compile('([A-F0-9]{24} /\*.*?\*/ = {)')
removeGroupString =  removeFileDic['PBXGroup']
# print(removeGroupString)
for single in  removeGroupPattern.findall(removeGroupString):
    # print(single)
    pass
rmGroupArray = removeGroupPattern.findall(removeGroupString)


removeFileString = removeFileDic['PBXBuildFile']
removeFilePattern = re.compile('([A-F0-9]{24}).* =')
for single in removeFilePattern.findall(removeFileString):
    # print(single)
    pass
rmBuildFileArray = removeFilePattern.findall(removeFileString)

removeFileRefSting = removeFileDic['PBXFileReference']
# print(removeFileRefSting)
for single in removeFilePattern.findall(removeFileRefSting):
    # print(single)
    pass
rmFileRefArray = removeFilePattern.findall(removeFileRefSting)

rmSourceBuildPattern = re.compile('([A-F0-9]{24}) /\*')
removeSourceBuildString = removeFileDic['PBXSourcesBuildPhase']
rmResourceBuildArray = rmSourceBuildPattern.findall(removeSourceBuildString)


## 获取主RootObject
rootObjectString = ''
rootobjectPattern = re.compile('rootObject = ([a-zA-Z0-9]*) /\*')
rootObjectResult = rootobjectPattern.findall(fileContent)
if rootObjectResult:
    rootObjectString = rootObjectResult[0]

#处理unityProject
# unity的主分组
PBXProjectPattern = re.compile('mainGroup = ([A-F0-9]{24})')
UnityMaingroup = ''
UnityGroupString = ''
UnityMainGroupResult = PBXProjectPattern.findall(UnityFileContent)
if UnityMainGroupResult:
    UnityMaingroup = UnityMainGroupResult[0]


PBXGroupString = unityDic['PBXGroup']
PBXChildPattern = re.compile('children = (\([.\s\S]*?)\);')
PBXGroupPattern = re.compile('([.\s\S]*?};)')
PBXGroupResult = PBXGroupPattern.findall(PBXGroupString)
if PBXGroupResult:
    for PBXGroupSingle in PBXGroupResult:
        if PBXGroupSingle.__contains__(UnityMaingroup):
            PBXGroupSingle = PBXGroupSingle.replace("name = CustomTemplate;","name = LoadAR;")
            handleString = ''
            for single in  PBXChildPattern.findall(PBXGroupSingle)[0].split(','):
                if single.__contains__('.xcassets') or single.__contains__('Unity-iPhone Tests') or single.__contains__('Products') or single.__contains__('Info.plist')or single.__contains__('.xib') or single.__contains__('.png'):
                    pass
                elif single.__contains__('/* libiconv.2.dylib */') or single.__contains__('/* Security1.framework */'):
                    pass
                else:
                    if single.strip() != '':
                       handleString += single + ','

            PBXGroupSingle = PBXGroupSingle.split('children = (')[0] + 'children = ' + handleString+'\n\t\t\t);' +PBXGroupSingle.split(');')[1]

            UnityGroupString += PBXGroupSingle
        elif PBXGroupSingle.__contains__('Unity-iPhone Tests'):
            continue
        elif PBXGroupSingle.__contains__('/* Libraries */ = {'):
            PBXGroupSingle = PBXGroupSingle.replace('path = Libraries;','path = LoadAR/Libraries;\n\t\t\t\tname = Libraries;\n')
            UnityGroupString += PBXGroupSingle
            pass
        elif PBXGroupSingle.__contains__('/* Classes */ = {'):
            PBXGroupSingle = PBXGroupSingle.replace('path = Classes;','path = LoadAR/Classes;\n\t\t\t\tname = Classes;\n')
            UnityGroupString += PBXGroupSingle
            pass
        else:
            UnityGroupString += PBXGroupSingle
    unityDic['PBXGroup'] = UnityGroupString

targetResultString = ''
PBXProjectString = targetFileDic['PBXProject']
PBXProjectResult = PBXProjectPattern.findall(PBXProjectString)
if PBXProjectResult:
    TargetMaingroup = PBXProjectResult[0]

targetFileGroupString = targetFileDic['PBXGroup']
PBXGroupPattern = re.compile('([.\s\S]*?};)')
loadArPattern = re.compile('([A-F0-9]{24} /\* LoadAR \*/,)')
PBXGroupResult = PBXGroupPattern.findall(targetFileGroupString)
if PBXGroupResult:
    for PBXGroupSingle in PBXGroupResult:
        containMain = PBXGroupSingle.__contains__(TargetMaingroup)
        containLoadAR =  PBXGroupSingle.__contains__('/* LoadAR */,')
        if containMain:
            if containLoadAR:
                PBXGroupSingle = PBXGroupSingle.replace(loadArPattern.findall(PBXGroupSingle)[0],'')#将LoadAR删除掉
            unityDic['PBXGroup'] = unityDic['PBXGroup'].replace('/* Classes */','/* UnityClasses */')
            PBXGroupSingle = PBXGroupSingle.split('children = (')[0] + 'children = (\n' + '\t\t\t\t'+UnityMaingroup+' /* LoadAR */,' + PBXGroupSingle.split('children = (')[1] + '\n' +unityDic['PBXGroup'].replace('SOURCE_ROOT','\"<group>\"')
            targetResultString += PBXGroupSingle
        elif PBXGroupSingle.__contains__('path = LoadAR/Classes;') or PBXGroupSingle.__contains__('/* UnityAds */ = {') or PBXGroupSingle.__contains__('/* PluginBase */ = {') \
                or PBXGroupSingle.__contains__('/* UI */ = {') or PBXGroupSingle.__contains__('/* Unity */ = {') \
                or PBXGroupSingle.__contains__('/* Native */ = {') or PBXGroupSingle.__contains__('/* Libraries */ = {') or PBXGroupSingle.__contains__('/* Plugins */ = {')\
                or PBXGroupSingle.__contains__('/* iOS */ = {'):
            # print(PBXGroupSingle)
            pass
        else:
            targetResultString += PBXGroupSingle
            pass
    # targetResultString =  targetResultString.replace('SOURCE_ROOT','\"<group>\"')
    targetFileDic['PBXGroup'] = targetResultString


##----------------------------------------------------------------------------------------------------------------------
##增加文件
unityFileString = unityDic['PBXBuildFile']

singleFilePattern = re.compile('([0-9A-F]{24}[.\s\S]*?\};\n)')
unityBuildFilePattern = re.compile('/\* (.*) in')

singlePatternResult = singleFilePattern.findall(unityFileString)
fileRefResult = ''
fileNameBackUpArray = []
if singlePatternResult:
    for single in singlePatternResult:
        fileNameResult = unityBuildFilePattern.findall(single)
        if fileNameResult:
            if fileNameResult[0].__contains__('.png') or fileNameResult[0].__contains__('.xib') or fileNameResult[0].__contains__('.plist') or fileNameResult[0].__contains__('xcassets') :
                pass
            elif fileNameResult[0].__contains__('.framework'):
                pass
            elif fileNameResult[0].__contains__('main.mm'):
                pass
            elif fileNameResult[0].__contains__('.m'):
                single = single.strip()[:-2] + " settings = {COMPILER_FLAGS = \"-fobjc-arc\"; };" +single.strip()[-2:]
                fileRefResult = fileRefResult + '\t\t' + single + '\n'
                pass
            else:
                fileNameBackUpArray.append(fileNameResult[0])
                fileRefResult = fileRefResult + '\t\t' + single + '\n'
                pass
unityDic['PBXBuildFile'] = fileRefResult


unityFileRefence = unityDic['PBXFileReference']
unityFilerefenceResult = ''
unityFileRefenceName = re.compile('/\* (.*) \*/')
pathPattern = re.compile('path = (.*?);')
singleFileRefResult = singleFilePattern.findall(unityFileRefence)
if singleFileRefResult:
    for single in singleFileRefResult:
        result3 = pathPattern.findall(single)
        fileNameResult = unityFileRefenceName.findall(single)
        if fileNameResult:
            if fileNameResult[0].__contains__('.png') or fileNameResult[0].__contains__('.xib') or fileNameResult[
                0].__contains__('.plist') or fileNameResult[0].__contains__('xcassets') \
                    or fileNameResult[0].__contains__('.app') or fileNameResult[0].__contains__('.xctest') \
                    or fileNameResult[0].__contains__('/ * en * /') :
                single = ''
                pass
            elif fileNameResult[0].__contains__('.framework'):
                single = ''
                pass
            elif fileNameResult[0].__contains__('main.mm'):
                single = ''
                pass
            else:
                resultstring1 = ''
                for spiltString in  single.strip().split(';'):
                    if spiltString.__contains__('.framework') or spiltString.__contains__('.strings')or spiltString.__contains__('.pch'):
                        pass
                    elif spiltString.__contains__('path = Data/Raw/QCAR') or spiltString.__contains__('path = Data/Raw/Vuforia'):
                        spiltString = 'path = LoadAR/%s' % spiltString.split('=')[1].strip()
                        pass
                    elif  spiltString.__contains__('path = Data') :
                        spiltString = 'path = LoadAR/%s; name = Data' % spiltString.split('=')[1].strip()
                        pass
                    elif spiltString.__contains__('.app') :
                        pass
                    elif spiltString.__contains__('.dylib') or spiltString.__contains__('ProductName.xctest') or spiltString.__contains__('Unity-iPhone Tests-Info.plist'):
                        pass
                    elif spiltString.__contains__('path =') and spiltString.__contains__('Classes/Native'):
                        spiltString = 'path = %s'%fileNameResult[0]
                        pass
                    elif spiltString.__contains__('path = Libraries/') or spiltString.__contains__('path = \"Libraries/') :
                        spiltString = 'path = %s' % fileNameResult[0]
                        pass
                    elif spiltString.__contains__('path = Classes/'):
                        spiltString = 'path = %s' % fileNameResult[0]
                        pass
                    resultstring1 = resultstring1+' '+spiltString +';'
                single = '\t\t'+ resultstring1[:-1] + '\n'
                single = single.replace('SOURCE_ROOT','\"<group>\"')
                pass
        if single.strip()!= '':
            unityFilerefenceResult = unityFilerefenceResult + '\t\t'+single + '\n'
unityDic['PBXFileReference'] = unityFilerefenceResult


targetPBXFileString =  targetFileDic['PBXBuildFile']
singlePattern = re.compile('([.\s\S]*?\n)')
targetfileStringLast = ''
if singlePattern.findall(targetPBXFileString):
    for singleString in singlePattern.findall(targetPBXFileString):
        if removeFilePattern.findall(singleString):
            if removeFilePattern.findall(singleString)[0] in rmBuildFileArray:
                # print(singleString)
                pass
            else:
                targetfileStringLast +=singleString
                pass

targetFileRefString = targetFileDic['PBXFileReference']
targetFileRefLastString = ''
if singlePattern.findall(targetFileRefString):
    for singleString in singlePattern.findall(targetFileRefString):
        if removeFilePattern.findall(singleString):
            if removeFilePattern.findall(singleString)[0] in removeFileRefSting:
                # print(singleString)
                pass
            else:
                targetFileRefLastString +=singleString
                pass

targetFileDic['PBXBuildFile'] = targetfileStringLast + unityDic['PBXBuildFile']
targetFileDic['PBXFileReference'] = targetFileRefLastString + unityDic['PBXFileReference']


#-------------------------------------------------分割线
shellScriptIDPattern = re.compile('[A-Z0-9]{24}')
shellScriptStringId = ''
shellScriptPattern = re.compile('([0-9A-F]{24} /\* ShellScript \*/,)')
unityNativeTargetString = unityDic['PBXNativeTarget']
shellScriptString = shellScriptPattern.findall(unityNativeTargetString)[0]
shellScriptStringId = shellScriptIDPattern.findall(shellScriptString)[0]

targetPBXNativeString = targetFileDic['PBXNativeTarget']
NativeTargetDic = {}
resultStringLast = ''
NativeTargetPattern = re.compile('([.\s\S]*?};)')
NativeTargetNamePattern = re.compile('name = ([a-zA-Z]*);')
NativeTargetBuildPattern = re.compile('buildPhases = \(([.\s\S]*?)\);')
NativeTargetDicPattern = re.compile('([A-F0-9]{24}) /\* ([a-zA-Z-]*?) \*/,')
NativeTargetResult = NativeTargetPattern.findall(targetPBXNativeString)
if NativeTargetResult:
    for singleString in NativeTargetResult :
        result = NativeTargetNamePattern.findall(singleString)
        if result :
            if result[0] == targetName:
                buildResult = NativeTargetBuildPattern.findall(singleString)
                if buildResult:
                   for singleTarget in buildResult[0].split(','):
                        if singleTarget.__contains__('ShellScript'):
                            singleString = singleString.replace(singleTarget+',','')
                   dicResult = NativeTargetDicPattern.findall(buildResult[0])

                   if dicResult:
                       for array in dicResult :
                           NativeTargetDic[array[1]] = array[0]
            singleString = singleString.split('buildPhases = (')[0] + 'buildPhases = (\n' + '\t\t\t\t' + shellScriptString + singleString.split('buildPhases = (')[1] + '\n'
        resultStringLast += singleString
targetFileDic['PBXNativeTarget'] = resultStringLast


UnityFrameWorkPattern = re.compile('files = \(([.\s\S]*?)\);')
# target
TargetFrameworkString = targetFileDic['PBXFrameworksBuildPhase']
UnityFrameWorkNamePattern = re.compile('/\* ([a-zA-Z\.]*) in Frameworks \*/')
TargetFrameWorkNameArray = []
TargetFrameWorkPattern = re.compile('files = \(([.\s\S]*?)\);')
TargetFrameWorkResult = TargetFrameWorkPattern.findall(TargetFrameworkString)
TargetFrameWorkNamePattern = re.compile('/\* ([a-zA-Z\.]*) in Frameworks \*/')
if TargetFrameWorkResult:
    TargetFrameWorkResultArray = TargetFrameWorkResult[0].split(',')
    for sinleTargetFrameWork in TargetFrameWorkResultArray:
        nameTargetResult = UnityFrameWorkNamePattern.findall(sinleTargetFrameWork)
        if nameTargetResult:
            TargetFrameWorkNameArray.append(nameTargetResult[0])



# 解析Unity的框架
UnityFrameworkString = unityDic['PBXFrameworksBuildPhase']
singleFrameWorkPattern = re.compile('/\* (.*?) in Frameworks \*/')
UnityFrameWorkNameArray = []
UnityFrameWrokFinalString = ''
unityFrameWorkstring = ''
frameWorkResult = UnityFrameWorkPattern.findall(UnityFrameworkString)
if frameWorkResult:
    unityFrameWorkstring = frameWorkResult[0]
    for singleFrameWork in frameWorkResult[0].split(','):
        if singleFrameWork.__contains__('.a'):
            UnityFrameWrokFinalString = UnityFrameWrokFinalString + singleFrameWork+','
UnityFrameWorkNameArray = singleFrameWorkPattern.findall(UnityFrameWrokFinalString)
# print(UnityFrameWorkNameArray)

frameWorkResultString = ''
frameworkResultLast = ''
tagetFrameReplaceString = ''
TargetFrameworkString = targetFileDic['PBXFrameworksBuildPhase']
singleResult = NativeTargetPattern.findall(TargetFrameworkString)
if singleResult:
    for single in singleResult:
        if single.__contains__(NativeTargetDic['Frameworks']):
            result2 = TargetFrameWorkPattern.findall(single)
            if result2:
                for singleFrameWork in result2[0].split(','):
                    # print(singleFrameWork)
                    if singleFrameWork.strip()!= '':
                        if singleFrameWorkPattern.findall(singleFrameWork)[0].strip() in UnityFrameWorkNameArray:
                           singleFrameWork = ''
                        elif singleFrameWork.strip() != '':
                            tagetFrameReplaceString = tagetFrameReplaceString + singleFrameWork + ','
                        else:
                             pass
                single = single.split('files = (')[0] + 'files = (\n' + '\t\t\t\t' +UnityFrameWrokFinalString +tagetFrameReplaceString + '\t\t\t);\n'+'\t\t\t\trunOnlyForDeploymentPostprocessing = 0;\n'+'\t\t};\n' + '\n'
        frameworkResultLast += single
targetFileDic['PBXFrameworksBuildPhase'] = frameworkResultLast
# print(frameworkResultLast)
## 获取unity的resource内容
unityResourceString = unityDic['PBXResourcesBuildPhase']
resourceResult = NativeTargetPattern.findall(unityResourceString)
resourceArrayString = ''
if resourceResult:
    resourceResult1 = UnityFrameWorkPattern.findall(resourceResult[0])
    if resourceResult1:
         resourceArray = resourceResult1[0].split(',')
         for single in resourceArray:
             if single.__contains__('QCAR') or single.__contains__('Vuforia') or single.__contains__('Data'):
                 resourceArrayString = resourceArrayString+'\t\t\t'+single+','


## 获取target的Resource内容
targetResouceString = targetFileDic['PBXResourcesBuildPhase']
resourceResult = NativeTargetPattern.findall(targetResouceString)
targetResultstring = ''
targetResultLastString = ''
if resourceResult:
    for string in resourceResult:
        if string.__contains__(NativeTargetDic['Resources']):
            fileResult = UnityFrameWorkPattern.findall(string)
            if fileResult:
                for single in fileResult[0].split(','):
                    if single.__contains__('QCAR') or single.__contains__('Vuforia') or single.__contains__('Data'):
                        string = string.replace(single+',','')
                    elif single.strip() != '' :
                        targetResultstring = targetResultstring + single +','
            string  = string.split('files = (')[0] + 'files = (\n' + '\t\t\t\t' + resourceArrayString + string.split('files = (')[1] + '\n'
        targetResultLastString+=string
targetFileDic['PBXResourcesBuildPhase'] = targetResultLastString


##unity的source
unitySourceString = unityDic['PBXSourcesBuildPhase']
unitySourceNameArray = []
unitySourceContentString = ''
sourceNamePattern = re.compile('/\* (.*?) in Sources \*/')
sourceMainPattern = re.compile('([A-F0-9]{24} /\* main.mm in Sources \*/,)')
sourceStringResult = NativeTargetPattern.findall(unitySourceString)
if sourceStringResult:
    sourceFileResult = TargetFrameWorkPattern.findall(sourceStringResult[0])

    if sourceFileResult:
        unitySourceContentString = sourceFileResult[0]
        if sourceMainPattern.findall(unitySourceContentString):#将main.mm移除掉
            unitySourceContentString = unitySourceContentString.replace(sourceMainPattern.findall(unitySourceContentString)[0],'')

        for single in sourceFileResult[0].split(','):
            result1 = sourceNamePattern.findall(single)
            if result1 :
                unitySourceNameArray.append(result1[0])


## target的source
targetSourceString = targetFileDic['PBXSourcesBuildPhase']
# targetID
targetSourceResult = NativeTargetPattern.findall(targetSourceString)
targetResultString1 = ''
targetSourcelastString = ''
if targetSourceResult:
    for singleResource in targetSourceResult:
        if singleResource.__contains__(NativeTargetDic['Sources']):
            targetSourceResult1 = TargetFrameWorkPattern.findall(singleResource)
            if targetSourceResult1:
                for singleResource1 in  targetSourceResult1[0].split(','):
                    if rmSourceBuildPattern.findall(singleResource1):
                        # print(singleResource1)
                        if rmSourceBuildPattern.findall(singleResource1)[0] in rmResourceBuildArray:
                            print(singleResource1)
                            pass
                        elif singleResource1.strip() != '':
                            targetResultString1 = targetResultString1+singleResource1+','
            targetResultString1 = targetResultString1 +unitySourceContentString
            singleResource = singleResource.split('files = (')[0] + 'files = (\n' + '\t\t\t\t'  + targetResultString1 +'\t\t\t);\n\t\t\trunOnlyForDeploymentPostprocessing = 0;\n\t\t};' + '\n'

        targetSourcelastString +=singleResource
targetFileDic['PBXSourcesBuildPhase'] = targetSourcelastString

# print(targetSourcelastString)
#删除无用的文件
# /Users/CharlyZhang/Desktop/testAUTO/OrangeCube/LoadAR/Data/Raw/AVProVideoSamples



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
    print('success' )
    print(time.time())
CopyReMoveFile(unityPath,targetPath)
import os

os.system('chmod -R 777 /Users/CharlyZhang/Git/OrangeCube/LoadAR/MapFileParser.sh')