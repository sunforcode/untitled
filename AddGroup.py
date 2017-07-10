import re
import string
import tkinter.filedialog
import Setting

unityFilePath = Setting.unityFilePath
targetFilePath = Setting.targetFilePath

# target的变量
targetFileDic = {}
unityDic = {}
rootObjectString = ''
UnityProjectMainGroup = ''
TargetMaingroup = ''

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
    if UnityResult:
        for str in UnityResult:
            s = '/\* Begin %s section \*/([.\s\S]*)/\* End %s section \*/' % (str, str)
            pattersn1 = re.compile(s)
            result1 = pattersn1.findall(UnityFileContent)
            if result1:
                unityDic[str] = result1[0]


#处理unityProject
    # unity的主分组
    PBXProjectPattern = re.compile('mainGroup = ([A-F0-9]{24})')
    UnityMaingroup = ''
    UnityGroupString = ''
    # print(UnityFileContent)
    UnityMainGroupResult = PBXProjectPattern.findall(UnityFileContent)
    if UnityMainGroupResult:
        UnityMaingroup = UnityMainGroupResult[0]


    # PBXProjectString = targetFileDic['PBXProject']
    PBXGroupString = unityDic['PBXGroup']
    PBXChildPattern = re.compile('children = (\([.\s\S]*?)\);')
    PBXGroupPattern = re.compile('([.\s\S]*?};)')
    PBXGroupResult = PBXGroupPattern.findall(PBXGroupString)
    # print(UnityMaingroup)
    if PBXGroupResult:
        for PBXGroupSingle in PBXGroupResult:
            if PBXGroupSingle.__contains__(UnityMaingroup):
                # print(PBXGroupSingle)
                PBXGroupSingle = PBXGroupSingle.replace("name = CustomTemplate;","name = LoadAR;")
                handleString = ''
                for single in  PBXChildPattern.findall(PBXGroupSingle)[0].split(','):
                    # print(single)
                    if single.__contains__('/* libiconv.2.dylib */') or single.__contains__('/* Frameworks */') or single.__contains__('.xcassets') or single.__contains__('Unity-iPhone Tests') or single.__contains__('Products') or single.__contains__('Info.plist')or single.__contains__('.xib') or single.__contains__('.png'):

                        pass
                    elif single.__contains__('/* libiconv.2.dylib */') or single.__contains__(
                            '/* Security.framework */'):
                        # 存储记录下来的框架
                        pass
                    else:
                        if single.strip() != '':
                           handleString += single + ','
                PBXGroupSingle = PBXGroupSingle.split('children = (')[0] + 'children = ' + handleString+'\n\t\t\t)' +PBXGroupSingle.split(');')[1]

                UnityGroupString += PBXGroupSingle
            elif PBXGroupSingle.__contains__('Unity-iPhone Tests'):
                continue
            elif PBXGroupSingle.__contains__('/* Libraries */ = {'):
                PBXGroupSingle = PBXGroupSingle.replace('path = Libraries;','path = LoadAR/Libraries;\n\t\t\t\tname = Libraries;\n')
                UnityGroupString += PBXGroupSingle
                pass
            elif PBXGroupSingle.__contains__('/* Classes */ = {'):
                PBXGroupSingle = PBXGroupSingle.replace('path = Classes;','path = LoadAR/Classes;\n\t\t\t\tname = Classes;\n')
                # print(PBXGroupSingle)
                UnityGroupString += PBXGroupSingle
                pass
            elif PBXGroupSingle.__contains__('/* Classes */ = {'):
                PBXGroupSingle = PBXGroupSingle.replace('path = Classes;','path = LoadAR/Classes;\n\t\t\t\tname = Classes;\n')
                # print(PBXGroupSingle)
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
    loadArPattern = re.compile('([A-F0-9]{24} /\* LoadAR \*/,)')
    PBXGroupResult = PBXGroupPattern.findall(targetFileGroupString)
    if PBXGroupResult:
        for PBXGroupSingle in PBXGroupResult:
            containMain = PBXGroupSingle.__contains__(TargetMaingroup)
            containLoadAR =  PBXGroupSingle.__contains__('LoadAR')
            if containMain:
                if containLoadAR:
                    PBXGroupSingle = PBXGroupSingle.replace('loadArPattern.findall(PBXGroupSingle)[0]','')#将LoadAR删除掉
                    pass
                PBXGroupSingle = PBXGroupSingle.split('children = (')[0] + 'children = (\n' + '\t\t\t\t'+UnityMaingroup+' /* LoadAR */,' + PBXGroupSingle.split('children = (')[1] + '\n' +unityDic['PBXGroup']
                targetResultString += PBXGroupSingle
            else:
                targetResultString += PBXGroupSingle
                pass
        targetResultString =  targetResultString.replace('SOURCE_ROOT','\"<group>\"')
        targetFileDic['PBXGroup'] = targetResultString
        # print(targetFileDic['PBXGroup'])

# 重新写入文件中
resultString = ''
for key in targetFileDic:
    begin = "/* Begin %s section */"%key
    end =  "/* End %s section */\n"%key
    content = targetFileDic[key]
    resultString =resultString + begin + content + end

resultString = "// !$*UTF8*$!\n{\n\t\tarchiveVersion = 1;\n\tclasses = {\n\t};\n\tobjectVersion = 46;\n\tobjects = {"+resultString + "};\nrootObject = "+'2D8467DE1F0C77B80048CE96'+" /* Project object */;\n}"
with open(targetFilePath, "r+") as testProject:
    # testProject.truncate()
    # testProject.write(resultString)
    print('success')
