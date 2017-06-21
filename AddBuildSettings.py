import re
import string
import tkinter.filedialog

# filename=tkinter.filedialog.askopenfilename(filetypes=[("bmp格式","avi")])

unityFilePath = '/Users/CharlyZhang/Desktop/XCode/Unity-iPhone.xcodeproj/project.pbxproj'
targetFilePath = '/Users/CharlyZhang/Desktop/TestPythonUnity/TestPythonUnity.xcodeproj/project.pbxproj'

# unityFilePath = '/Users/sunyongji/Desktop/staturdayUnity/Unity-iPhone.xcodeproj/project.pbxproj'
# targetFilePath = '/Users/sunyongji/Desktop/FounderAR606cao/E-Publishing.xcodeproj/project.pbxproj'


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
# print(unityBuildSettingDic)

targetBuildSettingDic = buildSettingKeyValue(targetFileDic, targetDebugDic, 'Release')
print(targetBuildSettingDic)

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
         if headString.strip() != '':
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
                        # print(tempString)
                        tempString = tempString.strip()
                        tempString = tempString[1:]
                        # print(tempString)
                        tempString = tempString[:-1]
                        # print(tempString)
                    elif tempString.__contains__("\""):
                        tempString = tempString.replace("\"", "\\\"")
                    resultString1 = resultString1+ ' ' +tempString.strip()+' '
                # print(targetBuildSettingDic[key][:-1])
                # print(key)
                UnitybuildSettingLastDic[keystr] = targetBuildSettingDic[key][:-1] + resultString1 + '\"'
                # print(targetBuildSettingDic['USER_HEADER_SEARCH_PATHS'])
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
    pass