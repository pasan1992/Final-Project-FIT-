import  pickle
from SynonimToolKitModule import SynonimToolKit



class MedicalQuestionClassifier:
    def __init__(self):

        self.FF = SynonimToolKit()
        f = open('vectorizer.pickle', 'rb')
        self.vectorizer = pickle.load(f)
        f.close()

        f = open('cfier.pickle', 'rb')
        self.cfier = pickle.load(f)
        f.close()

    def predictQuestionType(self,questionString):
        preparedQuestion = self.FF.ReplaceSynonym(questionString,"diseases")
        return  self.cfier.predict(self.vectorizer.transform([preparedQuestion]))




