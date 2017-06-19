import  re
import  string
import  os
import shutil

isMakeUpOrRevoke = False

targetFilePath = '/Users/CharlyZhang/Desktop/TestPythonUnity/TestPythonUnity.xcodeproj'
def makeBackUpFile(targetFilePath):
    targetProjectPath = targetFilePath + '/project.pbxproj'
    targetBackUpPath = targetFilePath + '/backUp'
    if not os.path.exists(targetBackUpPath):
        os.makedirs(targetBackUpPath)
    shutil.copyfile(targetProjectPath,targetBackUpPath +'/project.pbxproj')

def revokeBackUpFile(targetFilePath):
    targetProjectPath = targetFilePath + '/project.pbxproj'
    targetBackUpPath = targetFilePath + '/backUp'
    shutil.copyfile(targetBackUpPath +'/project.pbxproj',targetProjectPath)


if isMakeUpOrRevoke:
    makeBackUpFile(targetFilePath)
else:
    revokeBackUpFile(targetFilePath)
