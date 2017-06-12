import re
import string
releaseResultID = ''
date = ''
filePath = '/Users/CharlyZhang/Desktop/XCode/Unity-iPhone.xcodeproj/project.pbxproj'
targetXcodePath = '/Users/CharlyZhang/Desktop/TestPythonUnity/TestPythonUnity.xcodeproj/project.pbxproj'


#1.获去分组的信息
with open(filePath, 'r') as f:
    fileContent = f.read()
    sectionPattern = '/\* Begin (.*) section \*/'
    pattersn = re.compile(sectionPattern)
    result = pattersn.findall(fileContent)
    dic = {}
    if result:
        for str in result:
         s = '/\* Begin %s section \*/([.\s\S]*)/\* End %s section \*/'%(str,str)
         pattersn1 =  re.compile(s)
         result1 = pattersn1.findall(fileContent)
         if result1 :
             dic[str] = result1[0]


with open(filePath, 'r+') as targetFile:
    fileContent = targetFile.read()
    sectionPattern = '/\* Begin (.*) section \*/'
    pattersn = re.compile(sectionPattern)
    result = pattersn.findall(fileContent)
    targetDic = {}
    if result:
       for str in result:
          s = '/\* Begin %s section \*/([.\s\S]*)/\* End %s section \*/' % (str, str)
          pattersn1 = re.compile(s)
          result1 = pattersn1.findall(fileContent)
          if result1:
              targetDic[str] = result1[0]
resultString = ''
# PBXProject 获取主目录的ID
PBXProjectString = targetDic['PBXProject']
PBXProjectPattern = re.compile('mainGroup = ([a-zA-Z0-9]{24})')
PBXProjectResult = PBXProjectPattern.findall(PBXProjectString)
if PBXProjectResult:
    ProJectMainGroup = PBXProjectResult[0]

PBXGroupString = targetDic['PBXGroup']
# print(PBXGroupString)
PBXGroupPattern = re.compile('([.\s\S]*?};)')
PBXGroupResult = PBXGroupPattern.findall(PBXGroupString)
PBXGroupResultString = ''
if PBXGroupResult:
    string = ''
    for PBXGroupSingle in PBXGroupResult:
        # print(PBXGroupSingle)
        if PBXGroupSingle.__contains__(ProJectMainGroup):
           # print(PBXGroupSingle)
           # print('\t\t\t\t2D6E82131EAD9F800003D713,/* LoadAR */' + PBXGroupSingle.split('children = (')[1])
           # print(PBXGroupSingle)
           PBXGroupSingle = PBXGroupSingle.split('children = (')[0]+'children = (\n' +'\t\t\t\t2D6E82131EAD9F800003D713 /* LoadAR */,' + PBXGroupSingle.split('children = (')[1] + '\n' +'2D6E82131EAD9F800003D713 /* Supporting Files */ = {\n\tisa = PBXGroup;\n\tchildren = (\n\t);\n\tname = "LoadAR";\n\tsourceTree = "<group>";\n\t};'
           # print(PBXGroupSingle)
        PBXGroupResultString += PBXGroupSingle
            # print(PBXGroupSingle)
        if PBXGroupSingle.__contains__('/* Classes */ = '):
            # print(PBXGroupSingle)
            PBXGroupResultString += PBXGroupSingle
            continue
        # elif PBXGroupSingle.__contains__('CustomTemplate'):
        #     # print(PBXGroupSingle)
        #     continue
        elif PBXGroupSingle.__contains__('/* Data */ = {'):
            # print(PBXGroupSingle)
            PBXGroupResultString += PBXGroupSingle
            continue
        elif PBXGroupSingle.__contains__('/* Unity-iPhone Tests */ = {'):
            # print(PBXGroupSingle)
            PBXGroupResultString += PBXGroupSingle
            continue
        elif PBXGroupSingle.__contains__('/* Frameworks */ = '):
            # print(PBXGroupSingle)
            PBXGroupResultString += PBXGroupSingle
            continue
        elif PBXGroupSingle.__contains__('/* QCAR */ = '):
            # print(PBXGroupSingle)
            PBXGroupResultString += PBXGroupSingle
            continue
        elif PBXGroupSingle.__contains__('/* Vuforia */ = '):
            # print(PBXGroupSingle)
            PBXGroupResultString += PBXGroupSingle
            continue
        elif PBXGroupSingle.__contains__('/* Libraries */ = '):
            # print(PBXGroupSingle)
            PBXGroupResultString += PBXGroupSingle
            continue
        # else:
        #     # print(PBXGroupSingle)
        #     continue
        # if PBXGroupSingle.__contains__(ProJectMainGroup):
        #    print(PBXGroupSingle)
    targetDic['PBXGroup'] = PBXGroupResultString
    print(PBXGroupResultString)

# 将文件的内容重新写入文档

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
