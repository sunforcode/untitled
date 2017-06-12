import re
import string
import tkinter.filedialog

# filename=tkinter.filedialog.askopenfilename(filetypes=[("bmp格式","avi")])

unityFilePath = '/Users/CharlyZhang/Desktop/605-003/Unity-iPhone.xcodeproj/project.pbxproj'
targetFilePath = '/Users/CharlyZhang/Desktop/TestPythonUnity/TestPythonUnity.xcodeproj/project.pbxproj'
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

targetPBXNativeString = targetFileDic['PBXNativeTarget']
# print(targetPBXNativeString)
NativeTargetDic = {}
NativeTargetPattern = re.compile('([.\s\S]*?)};')
NativeTargetNamePattern = re.compile('name = ([a-zA-Z]*)')
NativeTargetBuildPattern = re.compile('buildPhases = \(([.\s\S]*?)\);')
NativeTargetDicPattern = re.compile('([A-F0-9]{24}) /\* ([a-zA-Z-]*?) \*/,')
NativeTargetResult = NativeTargetPattern.findall(targetPBXNativeString)
if NativeTargetResult:
    # print(NativeTargetResult[0] + '---\n'+ NativeTargetResult[1])
    for singleString in NativeTargetResult :
        result = NativeTargetNamePattern.findall(singleString)
        if result :
            if result[0] == targetName:
                buildResult = NativeTargetBuildPattern.findall(singleString)
                if buildResult:
                   # print(buildResult[0])
                   dicResult = NativeTargetDicPattern.findall(buildResult[0])
                   if dicResult:
                       for array in dicResult :
                           NativeTargetDic[array[1]] = array[0]

    print(NativeTargetDic)




UnityFrameWorkPattern = re.compile('files = \(([.\s\S]*)\);')
# target
TargetFrameworkString = targetFileDic['PBXFrameworksBuildPhase']
UnityFrameWorkNamePattern = re.compile('/\* ([a-zA-Z\.]*) in Frameworks \*/')
# print(UnityFrameworkString)
TargetFrameWorkNameArray = []
TargetFrameWorkPattern = re.compile('files = \(([.\s\S]*)\);')
TargetFrameWorkResult = TargetFrameWorkPattern.findall(TargetFrameworkString)
TargetFrameWorkNamePattern = re.compile('/\* ([a-zA-Z\.]*) in Frameworks \*/')
if TargetFrameWorkResult:
    TargetFrameWorkResultArray = TargetFrameWorkResult[0].split(',')
    for sinleTargetFrameWork in TargetFrameWorkResultArray:
        nameTargetResult = UnityFrameWorkNamePattern.findall(sinleTargetFrameWork)
        if nameTargetResult:
            TargetFrameWorkNameArray.append(nameTargetResult[0])

# print(TargetFrameWorkNameArray)


#解析Unity的框架
UnityFrameworkString = unityDic['PBXFrameworksBuildPhase']
# print(UnityFrameworkString)
UnityFrameWorkNameArray = []
UnityFrameWrokFinalString = ''
frameWorkResult = UnityFrameWorkPattern.findall(UnityFrameworkString)
if frameWorkResult:
   frameWorkResultArray = frameWorkResult[0].split(',')
   for sinleFrameWork in frameWorkResultArray:
       nameResult = UnityFrameWorkNamePattern.findall(sinleFrameWork)
       if nameResult:
           if (nameResult[0] in TargetFrameWorkNameArray):
               print(sinleFrameWork)
               # print('---------')
           # for targetFrameworkName in TargetFrameWorkNameArray:

               # if  (nameResult[0].__eq__(targetFrameworkName)):
               #      print(nameResult[0])
               #      # print(targetFrameworkName)
               #      break
               UnityFrameWrokFinalString = UnityFrameWrokFinalString +sinleFrameWork +','
           UnityFrameWorkNameArray.append(nameResult[0])
# print(UnityFrameWrokFinalString)

# print(UnityFrameworkString)
#将内容写进去
PBXGroupSingle = UnityFrameworkString.split('files = (')[0] + 'files = (\n' + '\t\t\t\t' + UnityFrameWrokFinalString + UnityFrameworkString.split('files = (')[1] + '\n'
# print(PBXGroupSingle)
targetFileDic['PBXFrameworksBuildPhase'] = PBXGroupSingle;

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
