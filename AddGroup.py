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

#处理unityProject
    # unity的主分组
    UnityMaingroup = ''
    UnityGroupString = ''
    UnityMainGroupResult = PBXProjectPattern.findall(UnityFileContent)
    if UnityMainGroupResult:
        UnityMaingroup = UnityMainGroupResult[0]
        # print(UnityMaingroup)
    # PBXProjectString = targetFileDic['PBXProject']
    PBXGroupString = unityDic['PBXGroup']
    PBXGroupPattern = re.compile('([.\s\S]*?};)')
    PBXGroupResult = PBXGroupPattern.findall(PBXGroupString)
    # print(UnityMaingroup)
    if PBXGroupResult:
        for PBXGroupSingle in PBXGroupResult:
            if PBXGroupSingle.__contains__(UnityMaingroup):
                # print(PBXGroupSingle)
                PBXGroupSingle = PBXGroupSingle.replace("name = CustomTemplate;","name = LoadAR;")
                UnityGroupString += PBXGroupSingle
            elif PBXGroupSingle.__contains__('Unity-iPhone Tests'):
                continue
            elif PBXGroupSingle.__contains__('Frameworks'):
                continue
            elif PBXGroupSingle.__contains__('Products'):
                continue

            else:
                UnityGroupString += PBXGroupSingle
        unityDic['PBXGroup'] = UnityGroupString
#获取主分组
    rootobjectPattern = re.compile('rootObject = ([a-zA-Z0-9]*) /\*')
    rootObjectResult = rootobjectPattern.findall(fileContent)
    if rootObjectResult:
        rootObjectString = rootObjectResult[0]

# PBXProject 获取主目录的ID 2D9A4B551EDE903E000D8470
    targetResultString = ''
    PBXProjectString = targetFileDic['PBXProject']
    PBXProjectResult = PBXProjectPattern.findall(PBXProjectString)
    if PBXProjectResult:
        UnityProjectMainGroup = PBXProjectResult[0]
        # print(UnityProjectMainGroup)
    targetFileGroupString = targetFileDic['PBXGroup']
    PBXGroupPattern = re.compile('([.\s\S]*?};)')
    PBXGroupResult = PBXGroupPattern.findall(targetFileGroupString)
    if PBXGroupResult:
        for PBXGroupSingle in PBXGroupResult:
            # print( PBXGroupSingle.split('\n')[2])
            # print('-----') 2D9A4B551EDE903E000D8470
            # print(PBXGroupSingle)
            containMain = PBXGroupSingle.__contains__(UnityProjectMainGroup)
            containLoadAR = not PBXGroupSingle.__contains__('LoadAR')
            if (containMain and containLoadAR):
                # print(UnityMaingroup)
                PBXGroupSingle = PBXGroupSingle.split('children = (')[0] + 'children = (\n' + '\t\t\t\t'+UnityMaingroup+' /* LoadAR */,' + PBXGroupSingle.split('children = (')[1] + '\n' +unityDic['PBXGroup']
                print(PBXGroupSingle)
                targetResultString += PBXGroupSingle
            else:
                targetResultString += PBXGroupSingle
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
