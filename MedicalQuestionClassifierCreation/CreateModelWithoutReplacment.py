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

training_data_path = "Data/test.label"

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

train_data = load_data(training_data_path)

random.shuffle(train_data)

train_questions = [line[1].lower() for line in train_data]
train_lables = [line[0] for line in train_data]



# print([line + "\n" for line in train_questions] )
# vectorizer =TfidfVectorizer(min_df=1)
vectorizer =TfidfVectorizer(min_df=1,ngram_range=(1,2),token_pattern=r'\b\w+\b')
question_vectors =vectorizer.fit_transform(train_questions)



f = open('vectorizer.pickle', 'wb')
pickle.dump(vectorizer, f,protocol=2)
f.close()

cfier = linear_model.LogisticRegression(multi_class='multinomial',solver='lbfgs')
cfier.fit(question_vectors, train_lables)
f = open('cfier.pickle', 'wb')
pickle.dump(cfier, f,protocol=2)
f.close()


gnb = GaussianNB()
y_pred = gnb.fit(question_vectors.toarray(), train_lables)

print(y_pred.predict(vectorizer.transform( ["what is diabeties"]).toarray() ))

clf = MultinomialNB()
clf.fit(question_vectors.toarray(), train_lables)
print(clf.predict(vectorizer.transform( ["what is diabeties"]).toarray() ))

clf2 = BernoulliNB()
clf2.fit(question_vectors.toarray(), train_lables)
print(clf2.predict(vectorizer.transform( ["what is diabeties"]).toarray() ))

# clf3 = RandomForestClassifier(n_estimators=100)
clf3 = LinearSVC()
clf3.fit(question_vectors, train_lables)
print(clf3.predict(vectorizer.transform( ["what is diabeties"]).toarray() ))


LogisticRegressiontrain_data_prediction = [  cfier.predict(vectorizer.transform([line[1].lower() ]))for line in train_data]
GaussianNBtrain_data_prediction = y_pred.predict(question_vectors.toarray())
MultinomialNBtrain_data_prediction =clf.predict(question_vectors.toarray())
BernoulliNBtrain_data_prediction =clf2.predict(question_vectors.toarray())
SVCtrain_data_prediction =clf3.predict(question_vectors.toarray())

print ("Train accuracy LogisticRegression" + str(compute_accuracy(LogisticRegressiontrain_data_prediction, train_lables)))
print ("Train accuracy GaussianNB" + str(compute_accuracy(GaussianNBtrain_data_prediction, train_lables)))
print ("Train accuracy MultinomialNB" + str(compute_accuracy(MultinomialNBtrain_data_prediction, train_lables)))
print ("Train accuracy BernoulliNB" + str(compute_accuracy(BernoulliNBtrain_data_prediction, train_lables)))
print ("Train accuracy SVC" + str(compute_accuracy(SVCtrain_data_prediction, train_lables)))



#
# cfier.classes_