import re
import string
import  os
import shutil

unityPath = '/Users/CharlyZhang/Desktop/XCode/Unity-iPhone.xcodeproj'
targetPath = '/Users/CharlyZhang/Desktop/TestPythonUnity/TestPythonUnity.xcodeproj'

targetName = 'TestPythonUnity'
# targetPath = '/Users/sunyongji/Desktop/TestPythonUnity/TestPythonUnity.xcodeproj'
# unityPath = '/Users/sunyongji/Desktop/staturdayUnity/Unity-iPhone.xcodeproj'



unityFilePath = unityPath + '/project.pbxproj'
targetFilePath = targetPath + '/project.pbxproj'

targetProjectName = 'TestPythonUnity'
unityProjectName = 'Unity-iPhone'
unityTargetName = 'Unity-iPhone'
projectTargetName = 'TestPythonUnity'
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

##增加文件


unityFileString = unityDic['PBXBuildFile']
# print(unityFileString)

singleFilePattern = re.compile('([0-9A-F]{24}[.\s\S]*?\};\n)')
unityBuildFilePattern = re.compile('/\* (.*) in')

singlePatternResult = singleFilePattern.findall(unityFileString)
fileRefResult = ''
fileNameBackUpArray = []
if singlePatternResult:
    for single in singlePatternResult:
        # print(single)
        fileNameResult = unityBuildFilePattern.findall(single)
        if fileNameResult:
            # print(fileNameResult[0])
            if fileNameResult[0].__contains__('.png') or fileNameResult[0].__contains__('.xib') or fileNameResult[0].__contains__('.plist') or fileNameResult[0].__contains__('xcassets') :
                # print(single)
                pass
            else:
                # fileRefResult = fileRefResult +'\t\t' +single + '\n'
                fileNameBackUpArray.append(fileNameResult[0])
                pass
        fileRefResult = fileRefResult + '\t\t' + single + '\n'
unityDic['PBXBuildFile'] = fileRefResult
# print(fileRefResult)

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
                0].__contains__('.plist') or fileNameResult[0].__contains__('xcassets'):
                single = ''
                pass
            else:
                resultstring1 = ''
                for spiltString in  single.strip().split(';'):
                    if spiltString.__contains__('.framework') or spiltString.__contains__('.strings')or spiltString.__contains__('.pch'):
                        pass
                    elif spiltString.__contains__('path = Data/Raw/QCAR') or spiltString.__contains__('path = Data') or spiltString.__contains__('path = Data/Raw/Vuforia'):
                        spiltString = 'path = LoadAR/%s' % spiltString.split('=')[1].strip()
                        print(spiltString)
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
                # print(single)
                pass
        unityFilerefenceResult = unityFilerefenceResult + '\t\t'+single + '\n'
unityDic['PBXFileReference'] = unityFilerefenceResult


targetFileDic['PBXBuildFile'] = targetFileDic['PBXBuildFile'] + unityDic['PBXBuildFile']
targetFileDic['PBXFileReference'] = targetFileDic['PBXFileReference'] + unityDic['PBXFileReference']

#-------------------------------------------------分割线
##增加shellScriptPattern
shellScriptIDPattern = re.compile('[A-Z0-9]{24}')
shellScriptStringId = ''
shellScriptPattern = re.compile('([0-9A-F]{24} /\* ShellScript \*/,)')
unityNativeTargetString = unityDic['PBXNativeTarget']
shellScriptString = shellScriptPattern.findall(unityNativeTargetString)[0]
shellScriptStringId = shellScriptIDPattern.findall(shellScriptString)[0]
print(shellScriptStringId)
print(shellScriptString)


targetPBXNativeString = targetFileDic['PBXNativeTarget']
# print(targetPBXNativeString)
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
                # print(result[0]+'===' +targetName)
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

print( NativeTargetDic)

UnityFrameWorkPattern = re.compile('files = \(([.\s\S]*?)\);')
# target
TargetFrameworkString = targetFileDic['PBXFrameworksBuildPhase']
UnityFrameWorkNamePattern = re.compile('/\* ([a-zA-Z\.]*) in Frameworks \*/')
# print(TargetFrameworkString)
TargetFrameWorkNameArray = []
TargetFrameWorkPattern = re.compile('files = \(([.\s\S]*?)\);')
TargetFrameWorkResult = TargetFrameWorkPattern.findall(TargetFrameworkString)
TargetFrameWorkNamePattern = re.compile('/\* ([a-zA-Z\.]*) in Frameworks \*/')
if TargetFrameWorkResult:
    # print(TargetFrameWorkResult)
    TargetFrameWorkResultArray = TargetFrameWorkResult[0].split(',')
    for sinleTargetFrameWork in TargetFrameWorkResultArray:
        nameTargetResult = UnityFrameWorkNamePattern.findall(sinleTargetFrameWork)
        if nameTargetResult:
            TargetFrameWorkNameArray.append(nameTargetResult[0])



# 解析Unity的框架
UnityFrameworkString = unityDic['PBXFrameworksBuildPhase']
UnityFrameWorkNameArray = []
UnityFrameWrokFinalString = ''
frameWorkResult = UnityFrameWorkPattern.findall(UnityFrameworkString)
if frameWorkResult:
    UnityFrameWorkNameArray = frameWorkResult[0].split(',')

frameWorkResultString = ''
frameworkResultLast = ''
TargetFrameworkString = targetFileDic['PBXFrameworksBuildPhase']
singleResult = NativeTargetPattern.findall(TargetFrameworkString)
if singleResult:
    for single in singleResult:
        if single.__contains__(NativeTargetDic['Frameworks']):
            result2 = TargetFrameWorkPattern.findall(single)
            if result2:
                for singleFrameWork in result2:
                    if singleFrameWork in UnityFrameWorkNameArray:
                        pass
                    else:
                        frameWorkResultString = frameWorkResultString+singleFrameWork
                        pass
                frameWorkResultString = frameWorkResultString + ','.join(UnityFrameWorkNameArray)
                single = single.split('files = (')[0] + 'files = (\n' + '\t\t\t\t' + frameWorkResultString + single.split('files = (')[1] + '\n'
                # print(single)
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
sourceStringResult = NativeTargetPattern.findall(unitySourceString)
if sourceStringResult:
    sourceFileResult = TargetFrameWorkPattern.findall(sourceStringResult[0])
    if sourceFileResult:
        unitySourceContentString = sourceFileResult[0]
        for single in sourceFileResult[0].split(','):
            result1 = sourceNamePattern.findall(single)
            if result1 :
                unitySourceNameArray.append(result1[0])

## target的source
targetSourceString = targetFileDic['PBXSourcesBuildPhase']
targetSourceResult = NativeTargetPattern.findall(targetSourceString)
targetResultString1 = ''
targetSourcelastString = ''
if targetSourceResult:
    for singleResource in targetSourceResult:
        if singleResource.__contains__(NativeTargetDic['Sources']):
            # print(singleResource)
            targetSourceResult1 = TargetFrameWorkPattern.findall(singleResource)
            if targetSourceResult1:
                for singleResource1 in  targetSourceResult1[0].split(','):
                    if singleResource1 in unitySourceNameArray:
                        singleResource.replace(singleResource1+',', '')
                    elif singleResource1.strip() != '':
                        targetResultString1 = targetResultString1+singleResource1+','
                # print(targetResultString1)
            targetResultString1 = targetResultString1 +unitySourceContentString
            singleResource = singleResource.split('files = (')[0] + 'files = (\n' + '\t\t\t\t' + targetResultString1 + \
                             singleResource.split('files = (')[1] + '\n'
        targetSourcelastString +=singleResource
targetFileDic['PBXSourcesBuildPhase'] = targetSourcelastString

targetFileDic['PBXShellScriptBuildPhase'] = '\n %s /* ShellScript */ = {\n\tisa = PBXShellScriptBuildPhase;\nbuildActionMask = 2147483647;\nfiles = (\n);\ninputPaths = (\n);\noutputPaths = (\n);\nrunOnlyForDeploymentPostprocessing = 0;\nshellPath = /bin/sh;\nshellScript = "\\"$PROJECT_DIR/LoadAR/MapFileParser.sh\\" rm -rf \\"$TARGET_BUILD_DIR/$PRODUCT_NAME.app/LoadAR/Data/Raw/QCAR\\"";\n};\n'%shellScriptStringId







##分割线-----------------------------------------------------------------------------------------------------------------
def getProjectIdAndNameDic(fileConterdic:dict):
    unityProjectIdDic = {}
    unityProjectString = fileConterdic['PBXProject']
    targetPattern = re.compile('targets = \(([.\s\S]*?)\);')
    targetIdPattern = re.compile('([0-9A-F]{24}) /\* (.*) \*/')

    targetResult = targetPattern.findall(unityProjectString)
    if targetResult:
        targetIDResult = targetIdPattern.findall(targetResult[0])
        if targetIDResult:
            for key in targetIDResult:
                unityProjectIdDic[key[1]] = key[0]
 #获取到了targetName 和targetId的字典 {'Unity-iPhone': '1D6058900D05DD3D006BFB54', 'Unity-iPhone Tests': '5623C57217FDCB0800090B9E'}
        return unityProjectIdDic

#获取unity的targetName 和targetID
unityProjectDic = getProjectIdAndNameDic(unityDic)
# print(unityProjectDic)

#获取目标的targetName 和targetID
targetProjectDic = getProjectIdAndNameDic(targetFileDic, )
# print(targetProjectDic)

# 获取了需要融合的target的内容的节点
def getProjectMainIdDictional(fileContentDic, targetNameID):
    ProjectMainIDDic = {}
    UnityNativeTargetString = fileContentDic['PBXNativeTarget']
    NativeTargetPattern = re.compile('([.\s\S]*?)};')
    UnityBuildSettingListIDPattern = re.compile('buildConfigurationList = ([A-F0-9]{24})')
    UnityBuildSettingListId = ''

    unityTargetResult = NativeTargetPattern.findall(UnityNativeTargetString)
    if unityTargetResult:
        for targetString in unityTargetResult:
            if targetString.__contains__(targetNameID):
               buildSettingIdResult = UnityBuildSettingListIDPattern.findall(targetString)
               if buildSettingIdResult:
                   UnityBuildSettingListId = buildSettingIdResult[0]
                   ProjectMainIDDic['buildConfigurationList'] = UnityBuildSettingListId
    return ProjectMainIDDic

porjectMainDic =  getProjectMainIdDictional(targetFileDic,targetProjectDic[projectTargetName])

unityMainIdDic = getProjectMainIdDictional(unityDic,unityProjectDic[unityTargetName])
# print(unityMainIdDic)

def projectReleaseAndDebug(filecontentDic,projectMainDic): # filecontent :主分组, projectMainDic 项目的各个主要信息
    UnityXCConfigurationListString = filecontentDic['XCConfigurationList']
    ConfigurationListPattern = re.compile('([.\s\S]*?};)')
    buildConfigurationPattern = re.compile('buildConfigurations = \(([.\s\S]*?)\);')
    buildNameAndIdPattern = re.compile('([A-F0-9]{24}) /\* ([a-zA-Z]*) \*/')
    UnityBuildNameAndIdDic = {}
    ConfiguationResult = ConfigurationListPattern.findall(UnityXCConfigurationListString)
    if ConfiguationResult:
        for configuationSingle in  ConfiguationResult:
            if configuationSingle.__contains__(projectMainDic['buildConfigurationList']):
                buildResult =  buildConfigurationPattern.findall(configuationSingle)
                if buildResult:
                    for namePair in buildResult[0].split(','):
                        namePairResult = buildNameAndIdPattern.findall(namePair)
                        if namePairResult:
                            UnityBuildNameAndIdDic[namePairResult[0][1]] = namePairResult[0][0]
            elif configuationSingle.__contains__('PBXProject'):
                buildResult =  buildConfigurationPattern.findall(configuationSingle)
                if buildResult:
                    for namePair in buildResult[0].split(','):
                        namePairResult = buildNameAndIdPattern.findall(namePair)
                        if namePairResult:
                            UnityBuildNameAndIdDic['PBXProject' + namePairResult[0][1]] = namePairResult[0][0]
    return UnityBuildNameAndIdDic

# {'Release': '1D6058950D05DD3E006BFB54', 'ReleaseForProfiling': '56E860841D67581C00A1AB2B', 'ReleaseForRunning': '56E860811D6757FF00A1AB2B', 'Debug': '1D6058940D05DD3E006BFB54', 'PBXProjectRelease': 'C01FCF5008A954540054247B', 'PBXProjectReleaseForProfiling': '56E860831D67581C00A1AB2B', 'PBXProjectReleaseForRunning': '56E860801D6757FF00A1AB2B', 'PBXProjectDebug': 'C01FCF4F08A954540054247B'}


targetDebugDic = projectReleaseAndDebug(targetFileDic,porjectMainDic)
# print(targetDebugDic)
unityDebugDic = projectReleaseAndDebug(unityDic,unityMainIdDic)
# print(unityDebugDic)

def buildSettingKeyValue(filecontentDic,fileDebugDic,buildSettingName):
    buildSettingString = filecontentDic['XCBuildConfiguration']
    idAndContentDic = {}
    buildSettingPattern = re.compile('([A-F0-9]{24})([.\s\S]*?)name = [a-zA-Z]*;\\n[\t]*\};')
    buildSettingsDicPattern = re.compile('buildSettings = \{([.\s\S]*)\};')
    buildKeyValuePattern = re.compile('([A-Z_]*) = ([.\s\S]*)')
    buildSettingPatternResult = buildSettingPattern.findall(buildSettingString)

    if buildSettingPatternResult :
        for buildSettingSingle in buildSettingPatternResult:

            if buildSettingSingle[0].__eq__(fileDebugDic['Debug']):
                buildSettingResult = buildSettingsDicPattern.findall(buildSettingSingle[1])
                if buildSettingResult:
                    for value in buildSettingResult[0].split(';'):
                        result = buildKeyValuePattern.findall(value)
                        if result:
                            vaule1 = result[0][1] #.replace('(', '')
                            # vaule1 = vaule1.replace(')', '')
                            idAndContentDic['Debug' + result[0][0]] = vaule1

            if buildSettingSingle[0].__eq__(fileDebugDic[buildSettingName]):
                buildSettingResult = buildSettingsDicPattern.findall(buildSettingSingle[1])
                if buildSettingResult:
                   for value in buildSettingResult[0].split(';'):
                        result = buildKeyValuePattern.findall(value)
                        if result:
                            vaule1 = result[0][1] #.replace('(','')
                            # vaule1 = vaule1.replace(')', '')
                            idAndContentDic[ buildSettingName+ result[0][0]] = vaule1

            if buildSettingSingle[0].__eq__(fileDebugDic['PBXProject'+ buildSettingName]):
                buildSettingResult = buildSettingsDicPattern.findall(buildSettingSingle[1])
                if buildSettingResult:
                   for value in buildSettingResult[0].split(';'):
                        result = buildKeyValuePattern.findall(value)
                        if result:
                            vaule1 = result[0][1]#.replace('(','')
                            # vaule1 = vaule1.replace(')', '')
                            idAndContentDic['PBXProject'+ buildSettingName + result[0][0]] = vaule1

            if buildSettingSingle[0].__eq__(fileDebugDic['PBXProject'+ 'Debug']):
                buildSettingResult = buildSettingsDicPattern.findall(buildSettingSingle[1])
                if buildSettingResult:
                   for value in buildSettingResult[0].split(';'):
                        result = buildKeyValuePattern.findall(value)
                        if result:
                            vaule1 = result[0][1]#.replace('(','')
                            # vaule1 = vaule1.replace(')', '')
                            idAndContentDic['PBXProject'+ 'Debug' + result[0][0]] = vaule1
    return  idAndContentDic
unityBuildSettingDic =  buildSettingKeyValue(unityDic,unityDebugDic,'ReleaseForRunning')

targetBuildSettingDic = buildSettingKeyValue(targetFileDic, targetDebugDic, 'Release')
# print(targetBuildSettingDic)

def UnityKeyValueDic(dic: dict,key:str,buildProjectName:str):
  if dic.__contains__(buildProjectName + key):
      return dic[buildProjectName + key]
  elif   dic.__contains__('Debug'+key):
      return dic['Debug'+key]
  elif dic.__contains__('PBXProject'+ buildProjectName + key):
      return dic['PBXProject'+ buildProjectName + key]
  elif dic.__contains__('PBXProject'+ 'Debug' + key):
      return dic['PBXProject'+ 'Debug' + key]
  else:
      return '1111111111111111111'

UnitybuildSettingLastDic = {}


UnitybuildSettingLastDic['OTHER_LDFLAGS'] = UnityKeyValueDic(unityBuildSettingDic,'OTHER_LDFLAGS','ReleaseForRunning')

UnitybuildSettingLastDic['LD_GENERATE_MAP_FILE'] = UnityKeyValueDic(unityBuildSettingDic,'LD_GENERATE_MAP_FILE','ReleaseForRunning')

UnitybuildSettingLastDic['HEADER_SEARCH_PATHS'] = UnityKeyValueDic(unityBuildSettingDic,'HEADER_SEARCH_PATHS','ReleaseForRunning')

UnitybuildSettingLastDic['LIBRARY_SEARCH_PATHS'] = UnityKeyValueDic(unityBuildSettingDic,'LIBRARY_SEARCH_PATHS','ReleaseForRunning')

UnitybuildSettingLastDic['FRAMEWORK_SEARCH_PATHS'] = UnityKeyValueDic(unityBuildSettingDic,'FRAMEWORK_SEARCH_PATHS','ReleaseForRunning')

UnitybuildSettingLastDic['OTHER_CFLAGS'] = UnityKeyValueDic(unityBuildSettingDic,'OTHER_CFLAGS','ReleaseForRunning')

UnitybuildSettingLastDic['GCC_C_LANGUAGE_STANDARD'] = UnityKeyValueDic(unityBuildSettingDic,'GCC_C_LANGUAGE_STANDARD','ReleaseForRunning')

UnitybuildSettingLastDic['CLANG_CXX_LIBRARY'] = UnityKeyValueDic(unityBuildSettingDic,'CLANG_CXX_LIBRARY','ReleaseForRunning')

UnitybuildSettingLastDic['GCC_ENABLE_CPP_RTTI'] = UnityKeyValueDic(unityBuildSettingDic,'GCC_ENABLE_CPP_RTTI','ReleaseForRunning')

UnitybuildSettingLastDic['CLANG_WARN_DEPRECATED_OBJC_IMPLEMENTATIONS'] = UnityKeyValueDic(unityBuildSettingDic,'CLANG_WARN_DEPRECATED_OBJC_IMPLEMENTATIONS','ReleaseForRunning')

UnitybuildSettingLastDic['GCC_ENABLE_CPP_EXCEPTIONS'] = UnityKeyValueDic(unityBuildSettingDic,'GCC_ENABLE_CPP_EXCEPTIONS','ReleaseForRunning')

UnitybuildSettingLastDic['GCC_USE_INDIRECT_FUNCTION_CALLS'] = UnityKeyValueDic(unityBuildSettingDic,'GCC_USE_INDIRECT_FUNCTION_CALLS','ReleaseForRunning')

UnitybuildSettingLastDic['UNITY_RUNTIME_VERSION'] = UnityKeyValueDic(unityBuildSettingDic,'UNITY_RUNTIME_VERSION','ReleaseForRunning')

UnitybuildSettingLastDic['UNITY_SCRIPTING_BACKEND'] = UnityKeyValueDic(unityBuildSettingDic,'UNITY_SCRIPTING_BACKEND','ReleaseForRunning')

UnitybuildSettingLastDic['OTHER_CPLUSPLUSFLAGS'] = UnityKeyValueDic(unityBuildSettingDic,'OTHER_CPLUSPLUSFLAGS','ReleaseForRunning')

# 处理headSearchpath
def handleDicValue(handleKey):
    headSearchPath = UnitybuildSettingLastDic[handleKey]
    headSearchPath = headSearchPath.replace('(','')
    headSearchPath = headSearchPath.replace(')','')
    headSearchArray = headSearchPath.split(',')
    headSearchResult = ''
    for headString in headSearchArray :
         if headString.__contains__('/'):
            array =  headString.split('/')
            stringM = ''
            for i in range(len(array)):
                if i == 0:
                    stringM = array[i] + '/LoadAR'
                else:
                    stringM = stringM+'/'+ array[i]
            headString = stringM
         headSearchResult += headString + ','
    return headSearchResult

headSearchResult = handleDicValue('HEADER_SEARCH_PATHS')
headSearchResult.replace(')','')

UnitybuildSettingLastDic['HEADER_SEARCH_PATHS'] = '(\n' +  headSearchResult + ')'
UnitybuildSettingLastDic ['USER_HEADER_SEARCH_PATHS'] = '(\n' +  headSearchResult + ')'

librarySearchString = handleDicValue('LIBRARY_SEARCH_PATHS')
UnitybuildSettingLastDic['LIBRARY_SEARCH_PATHS'] = '(\n' + librarySearchString + ')'

for key in targetBuildSettingDic:
    if  key.startswith('Release'):
        keystr = key[len('Release'):]
        # print(keystr)
        if keystr in ['OTHER_CFLAGS', 'LIBRARY_SEARCH_PATHS', 'OTHER_LDFLAGS', 'HEADER_SEARCH_PATHS','OTHER_CPLUSPLUSFLAGS', 'USER_HEADER_SEARCH_PATHS']:
            if targetBuildSettingDic[key] == '\"\"':
                UnitybuildSettingLastDic[keystr] = UnitybuildSettingLastDic[keystr]
                pass
            elif keystr == 'USER_HEADER_SEARCH_PATHS':
                tempString = UnitybuildSettingLastDic[keystr].replace('(', '')
                tempString = tempString.replace(')', '')
                tempArray = tempString.split(',')
                resultString1 = ''
                resultString1.__contains__("\"\\\"")
                resultString1.replace("\"\\\"", "\"")
                for tempString in tempArray:
                    # print(tempString)
                    if tempString.__contains__("\"\\\""):
                        print(tempString)
                        tempString = tempString.strip()
                        tempString = tempString[1:]
                        print(tempString)
                        tempString = tempString[:-1]
                        print(tempString)
                    elif tempString.__contains__("\""):
                        tempString = tempString.replace("\"", "\\\"")
                    resultString1 = resultString1+ ' ' +tempString.strip()+' '
                UnitybuildSettingLastDic[keystr] = targetBuildSettingDic[key][:-1] + resultString1 + '\"'
                # print(UnitybuildSettingLastDic[keystr])
            else:
            #     print(keystr)
                tempString = UnitybuildSettingLastDic[keystr].replace('(', '')
                tempString = tempString.replace(')', '')
                tempArray = tempString.split(',')
                tempStringTarget = targetBuildSettingDic[key].replace(')', '')
                tempStringTarget = tempStringTarget.replace('(', '')
                for string1 in tempArray:
                    if tempStringTarget.__contains__(string1):
                        pass
                    elif tempStringTarget.strip() != '':
                        tempStringTarget = tempStringTarget + string1 + ',\n'
                # print(tempStringTarget)
                UnitybuildSettingLastDic[keystr] = '(\n' + tempStringTarget+ '\n' + ')'
                pass
        else:
            if not (keystr in UnitybuildSettingLastDic):
                pass
            else:
                pass

for key in  UnitybuildSettingLastDic:
    if UnitybuildSettingLastDic[key].__contains__('(\n'):
        pass

targetBuildSettingDic = UnitybuildSettingLastDic
#重新构建

buildSettingString = targetFileDic['XCBuildConfiguration']
buildSettingPattern = re.compile('([A-F0-9]{24}[.\s\S]*?name = [a-zA-Z]*;\\n[\t]*\};)?')
buildSettingsDicPattern = re.compile('buildSettings = \{([.\s\S]*)\};')
buildKeyValuePattern = re.compile('([A-Z_]*) = ([.\s\S]*)')

buildString = ''

reWriteBuildSettingResult = buildSettingPattern.findall(buildSettingString)
if reWriteBuildSettingResult:
    for reWriteString in reWriteBuildSettingResult:
        debugString = 'Debug'
        if reWriteString.__contains__(targetDebugDic[debugString]):
            debugKeyValueString = ''
            for keyString in targetBuildSettingDic:
                if True:
                   string = '\t\t\t\t'+keyString[len(''):] + ' = ' + targetBuildSettingDic[keyString] + ';' + '\n'
                   debugKeyValueString +=  string
                   pass
            resultWriterStr = reWriteString.split('buildSettings = {')[0] + 'buildSettings = {\n' + debugKeyValueString + '};\n\t\t\t\tname = %s;\n\t\t\t\t\t};'%debugString
            reWriteString = resultWriterStr
            pass
        elif reWriteString.__contains__(targetDebugDic['Release']):
            debugKeyValueString = ''
            for keyString in targetBuildSettingDic:
                if True:
                    string = '\t\t\t\t' + keyString + ' = ' + targetBuildSettingDic[keyString] + ';' + '\n'
                    debugKeyValueString += string
                    pass
            resultWriterStr = reWriteString.split('buildSettings = {')[0] + 'buildSettings = {\n' + debugKeyValueString + '};\n\t\t\t\tname = %s;\n\t\t\t\t\t};' % 'Release'
            reWriteString = resultWriterStr
            pass
        else:
            pass
        buildString += reWriteString + '\n'
    targetFileDic['XCBuildConfiguration'] = buildString

















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

