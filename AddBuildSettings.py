import re
import string
import tkinter.filedialog

# filename=tkinter.filedialog.askopenfilename(filetypes=[("bmp格式","avi")])

unityFilePath = '/Users/CharlyZhang/Desktop/XCode/Unity-iPhone.xcodeproj/project.pbxproj'
targetFilePath = '/Users/CharlyZhang/Desktop/TestPythonUnity/TestPythonUnity.xcodeproj/project.pbxproj'

unityTargetName = 'Unity-iPhone'
projectTargetName = 'TestPythonUnity'

# target的变量
targetFileDic = {}
rootObjectString = ''

PBXProjectPattern = re.compile('mainGroup = ([a-zA-Z0-9]{24}) ')
# 打开目标的文件路径并格式化
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

rootobjectPattern = re.compile('rootObject = ([a-zA-Z0-9]*) /\*')
rootObjectResult = rootobjectPattern.findall(fileContent)
if rootObjectResult:
    rootObjectString = rootObjectResult[0]
    # print(rootObjectString)

# 1.打开Unity的文件路径并格式化
with open(unityFilePath, 'r') as f:
    UnityFileContent = f.read()
    sectionPattern = '/\* Begin (.*) section \*/'
    UnityPattersn = re.compile(sectionPattern)
    UnityResult = UnityPattersn.findall(UnityFileContent)
    unityDic = {}
    if UnityResult:
        for str in UnityResult:
            s = '/\* Begin %s section \*/([.\s\S]*)/\* End %s section \*/' % (str, str)
            pattersn1 = re.compile(s)
            result1 = pattersn1.findall(UnityFileContent)
            if result1:
                unityDic[str] = result1[0]

#这里是增加script的节点
# targetFileDic['PBXShellScriptBuildPhase'] = '\n 2DD6495F1EEE815700B8B792 /* ShellScript */ = {\n\tisa = PBXShellScriptBuildPhase;\nbuildActionMask = 2147483647;\nfiles = (\n);\ninputPaths = (\n);\noutputPaths = (\n);\nrunOnlyForDeploymentPostprocessing = 0;\nshellPath = /bin/sh;\nshellScript = "\\"$PROJECT_DIR/LoadAR/MapFileParser.sh\\" rm -rf \\"$TARGET_BUILD_DIR/$PRODUCT_NAME.app/LoadAR/Data/Raw/QCAR\\"";\n};\n'
# print(targetFileDic['PBXShellScriptBuildPhase'])

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
                # print(configuationSingle)
                buildResult =  buildConfigurationPattern.findall(configuationSingle)
                if buildResult:
                    for namePair in buildResult[0].split(','):
                        # print(namePair)
                        namePairResult = buildNameAndIdPattern.findall(namePair)
                        if namePairResult:
                            UnityBuildNameAndIdDic[namePairResult[0][1]] = namePairResult[0][0]
    return UnityBuildNameAndIdDic
# {'Release': '1D6058950D05DD3E006BFB54', 'ReleaseForProfiling': '56E860841D67581C00A1AB2B', 'ReleaseForRunning': '56E860811D6757FF00A1AB2B', 'Debug': '1D6058940D05DD3E006BFB54'}

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
            if buildSettingSingle[0].__eq__(fileDebugDic[buildSettingName]):
                buildSettingResult = buildSettingsDicPattern.findall(buildSettingSingle[1])
                if buildSettingResult:
                   for value in buildSettingResult[0].split(';'):
                        result = buildKeyValuePattern.findall(value)
                        if result:
                            vaule1 = result[0][1].replace('(','')
                            vaule1 = vaule1.replace(')', '')
                            idAndContentDic[result[0][0]] = vaule1
                            # print(result[0][0])
    return  idAndContentDic
unityBuildSettingDic =  buildSettingKeyValue(unityDic,unityDebugDic,'ReleaseForRunning')
print(unityBuildSettingDic)

targetBuildSettingDic = buildSettingKeyValue(targetFileDic, targetDebugDic, 'Debug')
# print(targetBuildSettingDic)

# print(unityBuildSettingDic['GCC_PREFIX_HEADER']) #pch
# print(unityBuildSettingDic['OTHER_LDFLAGS']) #other link Flags
# print(unityBuildSettingDic['LD_GENERATE_MAP_FILE']) #write link map file
# print(unityBuildSettingDic['HEADER_SEARCH_PATHS']) #head search path
# print(unityBuildSettingDic['LIBRARY_SEARCH_PATHS']) #libra search path
# print(unityBuildSettingDic['FRAMEWORK_SEARCH_PATHS']) #FrameWork
# print(unityBuildSettingDic['OTHER_CFLAGS']) #other C flags
# print(unityBuildSettingDic['GCC_C_LANGUAGE_STANDARD']) #C++ language dialect
# print(unityBuildSettingDic['CLANG_CXX_LIBRARY']) #C++ standard Library
# print(unityBuildSettingDic['GCC_ENABLE_CPP_RTTI']) #runtime Type
# print(unityBuildSettingDic['CLANG_WARN_DEPRECATED_OBJC_IMPLEMENTATIONS']) #overriding deprecated Objecet-c methods
# print(unityBuildSettingDic['GCC_ENABLE_CPP_EXCEPTIONS'])#enable Object-c extensions
# print(unityBuildSettingDic['GCC_USE_INDIRECT_FUNCTION_CALLS']) #GCC_USE_INDIRECT_FUNCTION_CALLS
# print(unityBuildSettingDic['UNITY_RUNTIME_VERSION'])#UNITY_RUNTIME_VERSION
# print(unityBuildSettingDic['UNITY_SCRIPTING_BACKEND'])#UNITY_SCRIPTING_BACKEND


#GCC_C_LANGUAGE_STANDARD




resultString = ''
for key in targetFileDic:
    begin = "/* Begin %s section */"%key
    end =  "/* End %s section */\n"%key
    content = targetFileDic[key]
    resultString =resultString + begin + content + end + '\n'

resultString = "// !$*UTF8*$!\n{\n\t\tarchiveVersion = 1;\n\tclasses = {\n\t};\n\tobjectVersion = 46;\n\tobjects = {"+resultString + "};\nrootObject = "+rootObjectString+" /* Project object */;\n}"
with open(targetFilePath, "r+") as testProject:
    testProject.truncate()
    testProject.write(resultString)
    print('success')