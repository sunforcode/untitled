import re
import string
import  os
import shutil

unityPath = '/Users/CharlyZhang/Desktop/FounderARDemo0706/Unity-iPhone.xcodeproj'
targetPath = '/Users/CharlyZhang/Desktop/OrangeCube/E-Publishing.xcodeproj'
targetFilePath = targetPath + '/project.pbxproj'


targetName = 'FounderReader'

targetFileDic = {}
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

#获取主分组
PBXProjectPattern = re.compile('mainGroup = ([A-F0-9]{24})')
PBXProjectString = targetFileDic['PBXProject']
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
        containLoadAR =  PBXGroupSingle.__contains__('/* LoadAR */,')
        if containMain:
            # print(PBXGroupSingle)
            pass
        else:
            pass

        if PBXGroupSingle.__contains__('/* UnityClasses */ = {') or PBXGroupSingle.__contains__('/* UnityAds */ = {') or PBXGroupSingle.__contains__('/* PluginBase */ = {') \
                or PBXGroupSingle.__contains__('/* UI */ = {') or PBXGroupSingle.__contains__('/* Unity */ = {') \
                or PBXGroupSingle.__contains__('/* Native */ = {') or PBXGroupSingle.__contains__('/* Libraries */ = {') or PBXGroupSingle.__contains__('/* Plugins */ = {')\
                or PBXGroupSingle.__contains__('/* iOS */ = {'):
            print(PBXGroupSingle)
