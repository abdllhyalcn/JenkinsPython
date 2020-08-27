import re
import glob


def findJenkinsFiles(variableName, directory):
    jenkins_files = glob.glob(directory + "/**/*JenkinsFile", recursive=True)
    if(len(jenkins_files) == 0):
        print('JenkinsFile adında dosya/dosyalar bulunamadı.')
    for file_path in jenkins_files:
        processFile(variableName, file_path)


def processFile(variableName, filePath):
    newText = None
    with open(filePath, 'r') as file_object:
        fileData = file_object.read()
        print('Dosya okundu.', filePath)
        newText = findAndSwitchVar(variableName, fileData)
    if newText == None:
        print(variableName, 'bulunmadı.')
        return
    else:
        with open(filePath, 'w') as file_object:
            file_object.write(newText)
        print('Değişiklikler uygulandı.')


def findAndSwitchVar(variableName, fileText):
    print('Değişkenler aranıyor...')
    # '\\s' argument is for backlash in string, actual regex is '\s'
    pattern = "(?:def\\s)(" + variableName + ")(?:\\s|)=(?:\\s|)(true|false)"

    if re.search(pattern, fileText) == None:
        return None

    newFileText = ''
    while True:
        currMatch = re.search(pattern, fileText)
        if(currMatch == None):
            break

        boolFlag = currMatch.groups()[1]
        if currMatch.groups()[1] == 'true':
            boolFlag = 'false'
        else:
            boolFlag = 'true'

        newFileText = newFileText + \
            fileText[:currMatch.start()] + \
            'def '+currMatch.groups()[0]+' = '+boolFlag
        fileText = fileText[currMatch.end():]

    newFileText = newFileText+fileText
    return newFileText


if __name__ == "__main__":
    path = input("Lütfen JenkinsFile'ların bulunduğu yolu giriniz: ")
    variableName = input("Lütfen değiştirilecek değişken adını giriniz(def \033[1mname\033[0m = boolean): ")
    confirm = input(
        "Bulunan tüm dosyalar üstünde işlem başlatılsın mı? [Enter]")
    if confirm == "":
        findJenkinsFiles(variableName, path)
        print('İşlem tamamlandı.')
