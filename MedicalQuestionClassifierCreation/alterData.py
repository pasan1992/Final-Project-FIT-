# from QuestionClassfierModule import MedicalQuestionClassifier
from nltk import word_tokenize
from SynonimToolKitModule import SynonimToolKit
import random
#
# mqc = MedicalQuestionClassifier()


FF = SynonimToolKit()

def load_data():
    # newfile = open('data/NewTestQuestionList.txt','w')
    # newfile2 = open('data/UnansweredQuestionList.txt', 'w')
    questions = []
    with open('Data/test2.label', 'r') as f:
        for line in f:
            label, question = line.split(":", 1)

            question = FF.ReplaceSynonym(question,"diseases")
            q = label +":" + question
            questions.append(q)

            # if line !="\n" and not CheckForWord(line,words):
            #     newfile.write(line.split(":")[1])
            # else:
            #     if(line!="\n"):
            #         newfile2.write(line.split(":")[1])
    f.close()




    questions = set(questions)
    print(questions)
    newfile = open('Data/newreduced.label', 'w')
    for question in questions:
        newfile.write(question + "\n")

    # newfile.close()
    # newfile2.close()




def suffleData():
    readf = open('Data/new.txt','r')
    writef = open('Data/FinalTestingSet.txt', 'w')
    questions = []



    for line in readf:
        questions.append(line)
        print(line)

    random.shuffle(questions)

    for line in questions:
        writef.write(line)

    readf.close()
    writef.close()


suffleData()





# string = "Are there any treatments or medications that relieve bone cancer pain?"
#
# print(CheckForWord(string,"ss"))

# load_data("data/symptoms.txt")
# print (words)