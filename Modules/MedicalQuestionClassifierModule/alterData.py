# from QuestionClassfierModule import MedicalQuestionClassifier
from nltk import word_tokenize
#
# mqc = MedicalQuestionClassifier()

words = []

def load_data():
    newfile = open('data/NewTestQuestionList.txt','w')
    newfile2 = open('data/UnansweredQuestionList.txt', 'w')
    words = ['treatments','treatment','treatments?','treatment?','treat','treated?','treated',"Is" ,"risk","risks","drugs","effects"]
    with open('data/new.txt', 'r') as f:
        for line in f:
            if line !="\n" and not CheckForWord(line,words):
                newfile.write(line.split(":")[1])
            else:
                if(line!="\n"):
                    newfile2.write(line.split(":")[1])
    f.close()
    newfile.close()
    newfile2.close()



def CheckForWord(sentense,word):
    tokanizedSentense = word_tokenize(sentense)
    for w in tokanizedSentense:
        for sim in word:
            if sim == w:
                return True

    return  False
load_data()



# string = "Are there any treatments or medications that relieve bone cancer pain?"
#
# print(CheckForWord(string,"ss"))

# load_data("data/symptoms.txt")
# print (words)