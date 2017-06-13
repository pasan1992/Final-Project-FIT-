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
import  Preprocessor

#Data set 4
training_data_path = "Data/test6.label"
# training_data_path = "Data/newreduced.label"
testing_data_path = "Data/new.txt"
vocabluary_path= "Data/VectorVocab.label"
# training_data_path = "Data/newreduced.label"

def load_data(filename):
    res = []
    with open(filename, 'r') as f:
        for line in f:
            label, question = line.split(":", 1)
            res.append((label, question))
    return res

def compute_accuracy(predicted, original):
    eq = [z[0] == z[1] for z in zip(predicted, original)]
    return eq.count(True)/float(len(eq))

FF = SynonimToolKit()
train_data = load_data(training_data_path)
test_data = load_data(testing_data_path)
vocabluary_data = load_data(vocabluary_path)

random.shuffle(train_data)


train_questions = [FF.ReplaceSynonym(line[1].lower(),"disease") for line in train_data]
# train_questions = [Preprocessor.Prepreocess(line[1].lower()) for line in train_data]
train_lables = [line[0] for line in train_data]

test_questions = [FF.ReplaceSynonym(line[1].lower(),"disease") for line in test_data]
# test_questions = [Preprocessor.Prepreocess(line[1].lower()) for line in test_data]
test_lables = [line[0] for line in test_data]

vocabluary_vector_data = [FF.ReplaceSynonym(line[1].lower(),"disease") for line in vocabluary_data]
# vocabluary_vector_data = [FF.ReplaceSynonym(line[1].lower(),"disease") for line in vocabluary_data]

# print([line + "\n" for line in train_questions] )
# vectorizer =TfidfVectorizer(min_df=1)
# vectorizer =TfidfVectorizer(min_df=1,ngram_range=(1,4),token_pattern=r'\b\w+\b')
# question_vectors =vectorizer.fit_transform(train_questions)


vectorizer = TfidfVectorizer(min_df=1, ngram_range=(1, 4), token_pattern=r'\b\w+\b')
vectorizer.fit(vocabluary_vector_data)

question_vectors =vectorizer.transform(train_questions)


f = open('vectorizer.pickle', 'wb')
pickle.dump(vectorizer, f,protocol=2)
f.close()

cfier = linear_model.LogisticRegression(multi_class='multinomial',solver='lbfgs')
cfier.fit(question_vectors, train_lables)
print(cfier.predict(vectorizer.transform( [FF.ReplaceSynonym("what causes heart attack","disease")])))


# gnb = GaussianNB()
# y_pred = gnb.fit(question_vectors.toarray(), train_lables)

# print(y_pred.predict(vectorizer.transform( [FF.ReplaceSynonym("what is diabeties","diseases")]).toarray() ))

# clf = MultinomialNB()
# clf.fit(question_vectors.toarray(), train_lables)
# print(clf.predict(vectorizer.transform( [FF.ReplaceSynonym("what is diabeties","diseases")]).toarray() ))
#
# clf2 = BernoulliNB()
# clf2.fit(question_vectors.toarray(), train_lables)
# print(clf2.predict(vectorizer.transform( [FF.ReplaceSynonym("what is diabeties","diseases")]).toarray() ))

# clf3 = RandomForestClassifier(n_estimators=100)
clf3 = LinearSVC()
clf3.fit(question_vectors, train_lables)
print(clf3.predict(vectorizer.transform( [FF.ReplaceSynonym("what causes heart attack","disease")])))


f = open('cfier.pickle', 'wb')
pickle.dump(clf3, f,protocol=2)
f.close()

LogisticRegressiontrain_data_prediction = [  cfier.predict(vectorizer.transform([FF.ReplaceSynonym(line[1].lower(),"disease")] ) )for line in train_data]
# GaussianNBtrain_data_prediction = y_pred.predict(question_vectors.toarray())
# MultinomialNBtrain_data_prediction =clf.predict(question_vectors.toarray())
# BernoulliNBtrain_data_prediction =clf2.predict(question_vectors.toarray())
SVCtrain_data_prediction =clf3.predict(question_vectors.toarray())

testing_question_vectors = vectorizer.transform(test_questions)

Testing_question_predictions = cfier.predict(testing_question_vectors)
SVCTesting_question_predictions = clf3.predict(testing_question_vectors)

logistic_scores = precision_recall_fscore_support(test_lables, Testing_question_predictions, average="weighted")
SVC_scores = precision_recall_fscore_support(test_lables, SVCTesting_question_predictions, average="weighted")


print ("Train accuracy LogisticRegression" + str(compute_accuracy(LogisticRegressiontrain_data_prediction, train_lables)))
# print ("Train accuracy GaussianNB" + str(compute_accuracy(GaussianNBtrain_data_prediction, train_lables)))
# print ("Train accuracy MultinomialNB" + str(compute_accuracy(MultinomialNBtrain_data_prediction, train_lables)))
# print ("Train accuracy BernoulliNB" + str(compute_accuracy(BernoulliNBtrain_data_prediction, train_lables)))
print ("Train accuracy SVC" + str(compute_accuracy(SVCtrain_data_prediction, train_lables)))
print(" LogisticRegression Testing Question Accuarcy " +str(compute_accuracy(Testing_question_predictions,test_lables)))
print(" SVC Testing Question Accuarcy " +str(compute_accuracy(SVCTesting_question_predictions,test_lables)))
print ( cfier.predict(vectorizer.transform( [FF.ReplaceSynonym("how to treat syndrome","diseases")]) )  )
print("logiscti scores" + str(logistic_scores))
print("SVC scores" +str(SVC_scores))
#
# cfier.classes_