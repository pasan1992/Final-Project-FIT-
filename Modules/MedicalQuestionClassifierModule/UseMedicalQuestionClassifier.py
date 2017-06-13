from QuestionClassfierModule import MedicalQuestionClassifier


mqc = MedicalQuestionClassifier()

question ="is there a cure for alargies"
print(mqc.predictQuestionType(question))

# print(mqc.predictClassProb(question))

print(mqc.getParam())