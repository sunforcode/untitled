import re
import string
import tkinter.filedialog

# filename=tkinter.filedialog.askopenfilename(filetypes=[("bmp格式","avi")])


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

targetName = 'TestPythonUnity'
# target的变量
targetFileDic = {}
rootObjectString = ''

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

rootobjectPattern = re.compile('rootObject = ([a-zA-Z0-9]*) /\*')
rootObjectResult = rootobjectPattern.findall(fileContent)
if rootObjectResult:
    rootObjectString = rootObjectResult[0]
# print(rootObjectString)

shellScriptPattern = re.compile('([0-9A-F]{24} /\* ShellScript \*/,)')
unityNativeTargetString = unityDic['PBXNativeTarget']
shellScriptString = shellScriptPattern.findall(unityNativeTargetString)[0]


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
                print(result[0]+'===' +targetName)
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
# print(resultStringLast)

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
if targetSourceResult:
    for singleResource in targetSourceResult:
        if singleResource.__contains__(NativeTargetDic['Sources']):
            targetSourceResult1 = TargetFrameWorkPattern.findall(singleResource)
            if targetSourceResult1:
                for singleResource1 in  targetSourceResult1[0].split(','):
                    if singleResource1 in unitySourceNameArray:
                        singleResource.replace(singleResource1+',', '')
                    elif singleResource1.strip() != '':
                        targetResultString1 = targetResultString1+singleResource1+','
                # print(targetResultString1)
targetResultString1 = targetResultString1 +unitySourceContentString
targetFileDic['PBXSourcesBuildPhase'] = targetResultString1





# 重新写入文件中
resultString = ''
for key in targetFileDic:
    begin = "/* Begin %s section */"%key
    end =  "/* End %s section */\n"%key
    content = targetFileDic[key]
    resultString =resultString + begin + content + end

resultString = "// !$*UTF8*$!\n{\n\t\tarchiveVersion = 1;\n\tclasses = {\n\t};\n\tobjectVersion = 46;\n\tobjects = {"+resultString + "};\nrootObject = "+rootObjectString+" /* Project object */;\n}"
with open(targetFilePath, "r+") as testProject:
    # testProject.truncate()
    # testProject.write(resultString)
    print('success')
