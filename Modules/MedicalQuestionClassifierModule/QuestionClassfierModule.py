import  pickle
from SynonimToolKitModule import SynonimToolKit



class MedicalQuestionClassifier:
    def __init__(self):

        self.FF = SynonimToolKit()
        f = open('data/vectorizer.pickle', 'rb')
        self.vectorizer = pickle.load(f)
        f.close()

        f = open('data/cfier.pickle', 'rb')
        self.cfier = pickle.load(f)
        f.close()

    def predictQuestionType(self,questionString):
        preparedQuestion = self.FF.ReplaceSynonym(questionString,"diseases")
        return  self.cfier.predict(self.vectorizer.transform([preparedQuestion]))

    def predictClassProb(self,questionString):
        preparedQuestion = self.FF.ReplaceSynonym(questionString,"diseases")
        return self.cfier.predict_proba(self.vectorizer.transform([preparedQuestion]))

    def getParam(self):
        return  self.cfier.classes_



