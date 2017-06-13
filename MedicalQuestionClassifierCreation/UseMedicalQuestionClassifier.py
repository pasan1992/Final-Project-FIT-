from QuestionClassfierModule import MedicalQuestionClassifier


mqc = MedicalQuestionClassifier()

print(mqc.predictQuestionType("how to treat syndrome"))


def load_data():
    newfile = open('Data/new.txt','w')
    with open('Data/data.txt', 'r') as f:
        for line in f:
            # str =   line.strip('\r\n') + " is a symptom \n"
            str = mqc.predictQuestionType(line.strip('\n'))[0] +":" + line
            newfile.writelines(str)
    f.close()
    newfile.close()

load_data()