import re
import string
import tkinter.filedialog

# filename=tkinter.filedialog.askopenfilename(filetypes=[("bmp格式","avi")])

unityFilePath = '/Users/CharlyZhang/Desktop/XCode/Unity-iPhone.xcodeproj/project.pbxproj'
targetFilePath = '/Users/CharlyZhang/Desktop/TestPythonUnity/TestPythonUnity.xcodeproj/project.pbxproj'

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

targetFileDic['PBXShellScriptBuildPhase'] = '\n 2DD6495F1EEE815700B8B792 /* ShellScript */ = {\n\tisa = PBXShellScriptBuildPhase;\nbuildActionMask = 2147483647;\nfiles = (\n);\ninputPaths = (\n);\noutputPaths = (\n);\nrunOnlyForDeploymentPostprocessing = 0;\nshellPath = /bin/sh;\nshellScript = "\\"$PROJECT_DIR/LoadAR/MapFileParser.sh\\" rm -rf \\"$TARGET_BUILD_DIR/$PRODUCT_NAME.app/LoadAR/Data/Raw/QCAR\\"";\n};\n'

print(targetFileDic['PBXShellScriptBuildPhase'])

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