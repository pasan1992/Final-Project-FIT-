import  pickley

f = open('vectorizer.pickle', 'rb')
vectorizer = pickle.load(f)
f.close()

f = open('cfier.pickle', 'rb')
cfier = pickle.load(f)
f.close()

testquestion = ["What is the symptom of diabeties"]
print(cfier.predict(vectorizer.transform(testquestion).toarray()))



