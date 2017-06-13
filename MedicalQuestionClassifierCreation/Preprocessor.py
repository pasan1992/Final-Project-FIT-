from SynonimToolKitModule import SynonimToolKit
import  ClassIdenfitier




def Prepreocess(question):
    FF = SynonimToolKit()
    question = FF.ReplaceSynonym(question,"disease")
    question =ClassIdenfitier.FindClasses(question,4)
    return  question