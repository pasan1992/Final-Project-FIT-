from SynonimToolKitModule import SynonimToolKit
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import linear_model
import  pickle
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import RandomForestClassifier
import nltk
from sklearn.svm import LinearSVC
from sklearn.metrics import precision_recall_fscore_support

training_data_path = "Data/QuestionSet.label"
testing_data_path = "Data/TestingSet.txt"
vocabluary_path= "Data/VectorVocab.label"
# training_data_path = "Data/newreduced.label"

def load_data(filename):
    res = []
    with open(filename, 'r') as f:
        for line in f:
            label, question = line.split(":", 1)
            res.append((label, question))
    return res



FF = SynonimToolKit()

train_data = load_data(training_data_path)
vocabluary_data = load_data(vocabluary_path)
testing_data = load_data(testing_data_path)

# test_data = load_data(testing_data_path)
random.shuffle(train_data)
train_questions = [FF.ReplaceSynonym(line[1].lower(),"diseases") for line in train_data]
train_lables = [line[0] for line in train_data]


testing_questions = [FF.ReplaceSynonym(line[1].lower(),"diseases") for line in testing_data]
testing_lables = [line[0] for line in testing_data]

vector_data = [FF.ReplaceSynonym(line[1].lower(),"diseases") for line in vocabluary_data]




# test_questions = [FF.ReplaceSynonym(line[1].lower(),"diseases") for line in test_data]
# test_lables = [line[0] for line in test_data]


total_questions = len(train_lables)




print("start")
BatchNo =1

F1_Scores =[]
BatchSize = 40

vectorizer = TfidfVectorizer(min_df=1, ngram_range=(1, 3), token_pattern=r'\b\w+\b')
vectorizer.fit(vector_data)


while BatchNo*BatchSize < total_questions:

    Train_question_batch = train_questions[:BatchNo*BatchSize]
    Train_label_batch = train_lables[:BatchNo*BatchSize]




    # testing_question_vectors = vectorizer.transform(train_questions)
    train_question_batch_vectors = vectorizer.transform(Train_question_batch)

    # cfier = linear_model.LogisticRegression(multi_class='multinomial',solver='lbfgs')
    # cfier.fit(train_question_batch_vectors, Train_label_batch)
    # LogisticRegression_train_data_prediction =cfier.predict((test_vector.toarray()))



    clf3 = LinearSVC()
    clf3.fit(train_question_batch_vectors, Train_label_batch)


    #TRANING SET
    # test_vector = vectorizer.transform(testing_questions)
    # SVCtrain_data_prediction =clf3.predict(test_vector.toarray())

    SVCtrain_data_prediction = clf3.predict(train_question_batch_vectors.toarray())


    # Testing_question_predictions = cfier.predict(testing_question_vectors)
    # SVCTesting_question_predictions = clf3.predict(testing_question_vectors)
    # logistic_scores = precision_recall_fscore_support(testing_lables, LogisticRegression_train_data_prediction, average="micro")
    SVC_scores = precision_recall_fscore_support(Train_label_batch, SVCtrain_data_prediction, average="micro")

    F1_Scores.append( [BatchNo, SVC_scores[2]])
    BatchNo +=1


print(F1_Scores)

# print(F1_Scores)
# print("logiscti scores" + str(logistic_scores))
# print("SVC scores" +str(SVC_scores))
#
# cfier.classes_