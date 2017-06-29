import re
import string
releaseResultID = ''
date = ''
filePath = '/Users/CharlyZhang/Desktop/062702autoOrientetion062901/Unity-iPhone.xcodeproj/project.pbxproj'
targetXcodePath = '/Users/CharlyZhang/Desktop/FounderAR606cao/E-Publishing.xcodeproj/project.pbxproj'
arcXocdepath = '/Users/CharlyZhang/Git/OrangeCube/E-Publishing.xcodeproj/project.pbxproj'
allMFileNames = []

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
    # 解析PBXBuildFile
    PBXBuildFileString = targetDic['PBXBuildFile']
    singlePattern = re.compile('([.\s\S]*?)\n')
    result12 = singlePattern.findall(PBXBuildFileString)

    fileNamePattern = re.compile('/\* ([a-zA-Z\._+]*) in Sources \*/')

    if result12 :
        frameWorksArray = []
        mFileResource = []
        cppFileResource = []
        otherResource = []
        floderResource = []
        for str in result12 :
            # print(str)
            # print('------')
            if str.__contains__("Frameworks"):
                frameWorksArray.append(str)
            elif str.__contains__('.m'):
                filenameResult =  fileNamePattern.findall(str)
                if filenameResult:
                   # print(filenameResult[0])
                   mFileResource.append(filenameResult[0])
                   allMFileNames = mFileResource
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



with open(arcXocdepath, 'r+') as targetFile:
    ArcFileContent = targetFile.read()
    sectionPattern = '/\* Begin (.*) section \*/'
    ArcPattersn = re.compile(sectionPattern)
    Arcresult = ArcPattersn.findall(ArcFileContent)
    targetDic = {}
    if Arcresult:
       for str in Arcresult:
          s = '/\* Begin %s section \*/([.\s\S]*)/\* End %s section \*/' % (str, str)
          ArcPattersn1 = re.compile(s)
          result1 = ArcPattersn1.findall(ArcFileContent)
          if result1:
              targetDic[str] = result1[0]
    # 解析PBXBuildFile
    PBXBuildFileString = targetDic['PBXBuildFile']
    singlePattern = re.compile('([.\s\S]*?)\n')
    result12 = singlePattern.findall(PBXBuildFileString)

    fileNamePattern = re.compile('/\* ([a-zA-Z\._+]*) in Sources \*/')

    if result12 :
        frameWorksArray = []
        mFileResource = []
        cppFileResource = []
        otherResource = []
        floderResource = []
        finalString = '';
        # print(targetDic['PBXBuildFile'])
        # print('------------------------')
        for str in result12 :
            if str.__contains__('.m') :
                filenameResult =  fileNamePattern.findall(str)
                if filenameResult:
                    for strName in allMFileNames:
                        # print(strName)
                        a = filenameResult[0].__eq__(strName)
                        b = filenameResult[0].find('-fobjc-arc') == -1
                        # print(b)
                        if a and b:
                            str = str[:-3]+" settings = {COMPILER_FLAGS = \"-fobjc-arc\"; };"+ str[-3:] + '\n'
                            print(str)
                            continue
                # print(str)
                finalString += str
                   # print(filenameResult[0])
                   # mFileResource.append(filenameResult[0])
                   # allMFileNames = mFileResource
            # elif str.__contains__('.cpp'):
            #     cppFileResource.append(str)
            # elif str.__contains__('.png')or str.__contains__('xcassets')or str.__contains__('xib'):
            #     otherResource.append(str)
            #     # print(str)
            # else:
            #     # print(str)
            #     continue
            else:
                str = str + '\n'
                finalString += str

            targetDic['PBXBuildFile'] = finalString

resultString = ''

for key in targetDic:
    begin = "/* Begin %s section */"%key
    end =  "/* End %s section */\n"%key
    content = targetDic[key]
    resultString =resultString + begin + content + end

resultString = "// !$*UTF8*$!\n{\n\t\tarchiveVersion = 1;\n\tclasses = {\n\t};objectVersion = 46;\n\tobjects = {\n\t"+resultString + "};\nrootObject = 29B97313FDCFA39411CA2CEA /* Project object */;\n}"
with open(arcXocdepath, "r+") as testProject:
    print(resultString)
    testProject.truncate()
    testProject.write(resultString)
    print('success')