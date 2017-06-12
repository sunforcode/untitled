import re
import string
releaseResultID = ''
date = ''
filePath = '/Users/CharlyZhang/Desktop/XCode/Unity-iPhone.xcodeproj/project.pbxproj'
targetXcodePath = '/Users/CharlyZhang/Desktop/TestPythonUnity/TestPythonUnity.xcodeproj/project.pbxproj'

with open(targetXcodePath, 'r+') as targetFile:
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


    # PBXProject 获取主目录的ID
    PBXProjectString = dic['PBXProject']
    PBXProjectPattern = re.compile('mainGroup = (.*) \/\*')
    PBXProjectResult = PBXProjectPattern.findall(PBXProjectString)
    if PBXProjectResult:
       ProJectMainGroup = PBXProjectResult[0]
       print(ProJectMainGroup)

    PBXGroupString = dic['PBXGroup']
    # print(PBXGroupString)
    PBXGroupPattern = re.compile('([.\s\S]*?};)')
    PBXGroupResult = PBXGroupPattern.findall(PBXGroupString)
    if PBXGroupResult :
        for PBXGroupSingle in PBXGroupResult:
            if PBXGroupSingle.__contains__('/* Products */ = '):
                # print(PBXGroupSingle)
                continue
            elif PBXGroupSingle.__contains__('CustomTemplate'):
                # print(PBXGroupSingle)
                continue
            elif PBXGroupSingle.__contains__('/* Supporting Files */ = {'):
                # print(PBXGroupSingle)
                continue
            elif PBXGroupSingle.__contains__('/* Unity-iPhone Tests */ = {'):
                # print(PBXGroupSingle)
                continue
            elif PBXGroupSingle.__contains__('/* Frameworks */ = '):
                # print(PBXGroupSingle)
                continue
            else:
                print(PBXGroupSingle)
                continue
