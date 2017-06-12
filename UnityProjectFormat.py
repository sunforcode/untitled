import re
import string
releaseResultID = ''
date = ''
filePath = '/Users/CharlyZhang/Desktop/XCode/Unity-iPhone.xcodeproj/project.pbxproj'
targetXcodePath = '/Users/CharlyZhang/Desktop/TestPythonUnity/TestPythonUnity.xcodeproj/project.pbxproj'

    #'/Users/CharlyZhang/Desktop/FounderAR518/E-Publishing.xcodeproj/project.pbxproj'

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

# print(targetDic)

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
    PBXProjectPattern = re.compile('mainGroup = ([a-zA-Z0-9]{24})')
    PBXProjectResult = PBXProjectPattern.findall(PBXProjectString)
    if PBXProjectResult:
       ProJectMainGroup = PBXProjectResult[0]
       print('-------')
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
                # print(PBXGroupSingle)
                continue



    # 解析PBXBuildFile
    PBXBuildFileString = dic['PBXBuildFile']
    singlePattern = re.compile('([.\s\S]*?)\n')
    result12 = singlePattern.findall(PBXBuildFileString)

    if result12 :
        frameWorksArray = []
        mFileResource = []
        cppFileResource = []
        otherResource = []
        floderResource = []
        for str in result12 :
            if str.__contains__("Frameworks"):
                frameWorksArray.append(str)
            elif str.__contains__('.m'):
                mFileResource.append(str)
            elif str.__contains__('.cpp'):
                cppFileResource.append(str)
            elif str.__contains__('.png')or str.__contains__('xcassets')or str.__contains__('xib'):
                otherResource.append(str)
                # print(str)
            else:
                # print(str)
                continue
        # print(frameWorksArray)
        # print(mFileResource)
        # print(cppFileResource)
        # print(otherResource)
        # print(floderResource)

        #PBXFileReference 解析
        PBXFileReferenceString = dic['PBXFileReference']
        # print(PBXFileReferenceString)
        fileReferenceResult = singlePattern.findall(PBXFileReferenceString)
        if fileReferenceResult :
            for singLine in fileReferenceResult:
                # print(singLine)
                if singLine.__contains__("lastKnownFileType = folder"): #文件
                    # print(singLine)
                    continue
                elif singLine.__contains__("archive.ar")or singLine.__contains__('.framework'): #框架
                    # print(singLine)
                    continue
                elif singLine.__contains__(".h") or singLine.__contains__(".m")or singLine.__contains__(".cpp"): #资源文件
                    # print(singLine)
                    continue
                else:# 无用的文件
                    # print(singLine)
                    continue

        PBXFrameworkString = dic['PBXFrameworksBuildPhase'] #框架的引用
        # print(PBXFrameworkString)
        frameWokrPattern = re.compile('files = \(([.\s\S]*)\);')
        frameWorkResult = frameWokrPattern.findall(PBXFrameworkString)
        if frameWorkResult:
            frameWrokSinglePattern  = re.compile('(.*)\n')
            frameWorkResultArray = frameWrokSinglePattern.findall(frameWorkResult[0])

            # frameWorkResultArray =  frameWorkResult[0].split(',')
            for frameworkSingleLine in frameWorkResultArray :
                # print(frameworkSingleLine)
                continue




# PBXNativeTarget #warning
    PBXNativeTargetString = dic['PBXNativeTarget']
    PBXNativePattern = re.compile('buildPhases = \(([.\s\S]*?)\);')
    PBXNativePatternResult = PBXNativePattern.findall(PBXNativeTargetString)
    if PBXNativePatternResult:
        PBXNativeSinglePattern = re.compile('(.*,)\n')
        PBXNativeSingleResult = PBXNativeSinglePattern.findall(PBXNativePatternResult[0])
        if PBXNativeSingleResult:
            for PBXNativeSingString in PBXNativeSingleResult:
                continue
                # print(PBXNativeSingString)

    # print(PBXNativePatternResult[0])
    # print(PBXNativeTargetString)


# PBXResourcesBuildPhase 取得没有后缀的文件目录
    PBXResourcesBuildPhaseString = dic['PBXResourcesBuildPhase']
    PBXResourcesBuildPhasePattern = re.compile('files = \(([.\s\S]*?)\);')
    PBXResourcesBuildPhaseResult = PBXResourcesBuildPhasePattern.findall(PBXResourcesBuildPhaseString)
    if PBXResourcesBuildPhaseResult:
        PBXResourcesBuildPhaseSinglePattern = PBXResourcesBuildPhaseSinglePattern = re.compile('(.*,)\n')
        PBXResourcesBuildPhaseSingleResult = PBXResourcesBuildPhaseSinglePattern.findall(PBXResourcesBuildPhaseResult[0])
        if PBXResourcesBuildPhaseSingleResult:
            for PBXResourcesBuildPhaseSingleString in PBXResourcesBuildPhaseSingleResult:
                if not PBXResourcesBuildPhaseSingleString.__contains__("."):
                    continue
                   # print(PBXResourcesBuildPhaseSingleString)

# PBXShellScriptBuildPhase 脚本文件的
    PBXShellScriptBuildPhaseString = dic['PBXShellScriptBuildPhase']
    PBXShellScriptBuildPhasePattern = re.compile('shellScript = (.*);')
    PBXShellScriptBuildPhaseResult = PBXShellScriptBuildPhasePattern.findall(PBXShellScriptBuildPhaseString)
    if PBXShellScriptBuildPhaseResult:
        PBXShellScriptBuildPhasePath = PBXShellScriptBuildPhaseResult[0]
    # print(PBXShellScriptBuildPhaseString)


# PBXSourcesBuildPhase
    PBXSourcesBuildPhaseString = dic['PBXSourcesBuildPhase']
    PBXSourcesBuildPhasePattern = re.compile('files = \(([.\s\S]*?)\);')
    PBXSourcesBuildPhaseResult = PBXSourcesBuildPhasePattern.findall(PBXSourcesBuildPhaseString)
    if PBXSourcesBuildPhaseResult:
        PBXSourcesBuildPhaseSinglePattern = PBXResourcesBuildPhaseSinglePattern = re.compile('(.*,)\n')
        PBXSourcesBuildPhaseSingleResult = PBXSourcesBuildPhaseSinglePattern.findall(PBXSourcesBuildPhaseResult[0])
        if PBXSourcesBuildPhaseSingleResult:
            for PBXSourcesBuildPhaseSingleString in PBXSourcesBuildPhaseSingleResult:
                continue
                # print(PBXSourcesBuildPhaseSingleString)

# XCConfigurationList 获取主要配置文件 ReleaseForRunning
    XCConfigurationListString = dic['XCConfigurationList']
    XCConfigurationListPattern = re.compile('([.\s\S]*?};)')
    XCConfigurationListResult = XCConfigurationListPattern.findall(XCConfigurationListString)
    if XCConfigurationListResult:
       for XCConfigurationListSingleString in XCConfigurationListResult:
           if XCConfigurationListSingleString.__contains__('PBXNativeTarget'):
               # print(XCConfigurationListSingleString)
               releasePattern = re.compile('buildConfigurations = \(([.\s\S]*?)\);')
               releaseResult = releasePattern.findall(XCConfigurationListSingleString)
               if releaseResult :
                 # print(releaseResult[0])
                 releadIdString = releaseResult[0]
                 # releaseIdPattern = re.compile('([0-9a-fA-F]* /\* [a-zA-Z]* \*/,)')
                 releaseIdPattern = re.compile('[0-9a-fA-F]* /\* [a-zA-Z]* \*/')
                 releaseIdResult = releaseIdPattern.findall(releadIdString)
                 if  releaseIdResult:
                     # print(releaseIdResult)
                     for idString in releaseIdResult:
                         if idString.__contains__('ReleaseForRunning'):
                             releaseResultID = idString.strip('/* ReleaseForRunning */')
                             # print(idString)
                             continue
           elif XCConfigurationListSingleString.__contains__('PBXProject'):
               # print(XCConfigurationListSingleString)
               continue

# XCBuildConfiguration
    XCBuildConfigurationString = dic['XCBuildConfiguration']
    XCBuildConfigurationStringPattern = re.compile('[0-9a-fA-F]* /\* [a-zA-Z]* \*/ = {[.\s\S]*?name = [a-zA-Z]*;\n[\t]*};')
    XCBuildConfigurationStringResult = XCBuildConfigurationStringPattern.findall(XCBuildConfigurationString)
    if XCBuildConfigurationStringResult:
       for XCBuildConfigurationStringSignleString in  XCBuildConfigurationStringResult:
           if XCBuildConfigurationStringSignleString.__contains__(releaseResultID):
               # print(XCBuildConfigurationStringSignleString)
               configurationPatter = re.compile('[a-zA-Z]* = [.\s\S]*?;')
               keyResult = configurationPatter.findall(XCBuildConfigurationStringSignleString)
               if keyResult :
                   keyValueDic = {}
                   keyValuePattern = re.compile('([a-zA-Z]*) =([.\s\S]*?);')
                   for key in keyResult:
                       finale = keyValuePattern.findall(key)
                       if finale:
                           sss = finale[0][1]
                           # print(sss)
                           keyValueDic[finale[0][0]] = finale[0][1]

                       # print(key)
                       # print(keyValueDic)
                       continue
    # print(keyValueDic['LDFLAGS'])
    # print(keyValueDic)