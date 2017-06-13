from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.stem import  PorterStemmer
# import cPickle

class SynonimToolKit:



    # def __init__(self):
    #     self.lemmatizer = WordNetLemmatizer()
    #     self.listOfWords = ['disease','illness','cancer','contamination','defect','disorder','epidemic','fever','flu','illness','sickness','syndrome']
    #     self.synslist = [str(syn) for w in self.listOfWords  for syn in wn.synsets(w)]
    #     # self.synslist = cPickle.load(open('list.p', 'rb'))
    #     cPickle.dump(self.synslist, open('list.p', 'wb'))
    #     # #list = ['disease','illness','cancer','contamination','defect','disorder','epidemic','illness']
    #     #punch = list(string.punctuation)

    def __init__(self,listOfSynonym = ['disease','illness','cancer','contamination','defect','disorder','epidemic','fever','flu','illness','sickness','syndrome']):
        self.lemmatizer = WordNetLemmatizer()
        self.listOfSyn = listOfSynonym
        self.synslist = [str(syn) for w in self.listOfSyn  for syn in wn.synsets(w)]
        # self.synslist = cPickle.load(open('list.p', 'rb'))
        # cPickle.dump(self.synslist, open('list.p', 'wb'))
        # #list = ['disease','illness','cancer','contamination','defect','disorder','epidemic','illness']

    def Prepare(self,strQuestion):
        disease = False
        strQuestion = strQuestion.lower()
        tokanizedQuestion =word_tokenize(strQuestion)
        tokanizedQuestion =[ self.lemmatizer.lemmatize(w) for w in tokanizedQuestion]
        #tokanizedQuestion = filter(lambda w: not w in punch, tokanizedQuestion)
        tokanizedQuestion.append('diseaseword' if self._DiseaseCheck(tokanizedQuestion) else '')
        tokanizedQuestion = list(filter(lambda w:  not w in self.listOfSyn,tokanizedQuestion))
        #print(tokanizedQuestion)
        return tokanizedQuestion


    def _Prepare(self,strQuestion):
        strQuestion = strQuestion.lower()
        tokanizedQuestion =word_tokenize(strQuestion)
        tokanizedQuestion =[ self.lemmatizer.lemmatize(w) for w in tokanizedQuestion]
        return tokanizedQuestion


    def HasSynonym(self,sentense):
        try:
            return (len(self._FindWords(self._Prepare(sentense)))>0)
        except Exception as e:
            print(str(e))
            return False
    def GetSynonym(self,sentense):
        try:
            return self._FindWords(self._Prepare(sentense))
        except Exception as e:
            print(str(e))
            return []

    # def ReplaceSynonym(self,sentense,ReplaceWord ="REPLACED"):
    #     try:
    #         return self._FindWords(self._Prepare(sentense),True,ReplaceWord)
    #     except Exception as e:
    #         print (str(e))
    #         return []

    def ReplaceSynonym(self,sentense,ReplaceWord ="REPLACED",stringFrom =True):
            ps = PorterStemmer()
            if (stringFrom ==False):
               return self._FindWords(self._Prepare(sentense),True,ReplaceWord)
            else:
                wordListSentense = self._FindWords(self._Prepare(sentense),True,ReplaceWord)
                newWordList =[]
                for word in wordListSentense:
                    newWordList.append(word)

                return self.CreateSentenseFromList(newWordList)

    def CreateSentenseFromList(self,list):
        sentense =''

        for word in list:
            sentense += word + " "

        return  sentense



    def _RemoveBigrams(self,tokanizedQuestion,bigramlist,replaceWord="Defualtreplaced"):
        pre =""
        for idx, word in enumerate(tokanizedQuestion):
            checkingBigram = pre +"_" + word
            if( checkingBigram in bigramlist):
                tokanizedQuestion[idx] =replaceWord
                tokanizedQuestion[idx -1] =""
                pre =""
            else:
                 pre =word

            newtokanizedQuestion = list(filter(lambda w: w !="",tokanizedQuestion))

        return newtokanizedQuestion




        # hypernamepaths =[ str(hyp) for syns in  wn.synsets(word) for hypset in syns.hypernym_paths() for hyp in hypset ]
        # commonTerms = filter(lambda w:  w in self.synslist,hypernamepaths)
        # return len(commonTerms) >0


    def _isSynonym(self, disease):
        hypernamepaths = [str(hyp) for syns in wn.synsets(disease) for hypset in syns.hypernym_paths() for hyp in hypset]
        commonTerms =list( filter(lambda w: w in self.synslist, hypernamepaths))
        return len(commonTerms) > 0

    #replaced
    def _isDiseaseWord(self,disease):
        hypernamepaths =[ str(hyp) for syns in  wn.synsets(disease) for hypset in syns.hypernym_paths() for hyp in hypset ]
        commonTerms = list(filter(lambda w:  w in self.synslist,hypernamepaths))
        return len(commonTerms) >0

    #replaced
    def _DiseaseCheck(self,tokanizedQuestion):
        unigram_diseasesList = list(filter(lambda w:  self._isDiseaseWord(w),tokanizedQuestion))
        bigram_finder = BigramCollocationFinder.from_words(tokanizedQuestion)
        bigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, 20)
        wrd_str = []
        for fst, scnd in bigrams:
            wrd_str.append( fst + '_' + scnd)
        bigrams_diseasesList = list(filter(lambda w:  self._isDiseaseWord(w),wrd_str))
        return  (len(bigrams_diseasesList) >0) or (len(unigram_diseasesList)>0)



    def _FindWords(self, tokanizedQuestion,replace=False,replaceWord ="REPLACED"):
        wordFound =[]
        unigram_List = list(filter(lambda w: self._isSynonym(w), tokanizedQuestion))



        bigram_finder = BigramCollocationFinder.from_words(tokanizedQuestion)
        bigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, 20)
        wrd_str = []
        bigrams_List =[]

        if not replace:

            for fst, scnd in bigrams:
                unifiedBigram =fst + '_' + scnd
                if(self._isSynonym(unifiedBigram)):
                    bigrams_List.extend([fst,scnd])
            allwords = unigram_List + bigrams_List

            return (allwords)
        else:
            for fst, scnd in bigrams:
                unifiedBigram = fst + '_' + scnd
                if (self._isSynonym(unifiedBigram)):
                    bigrams_List.append(unifiedBigram)
                    tokanizedQuestion =self._RemoveBigrams(tokanizedQuestion,bigrams_List,replaceWord)

            newTokanizedQuestion = [ replaceWord if w in unigram_List else w for w in tokanizedQuestion]

            return newTokanizedQuestion


    # print(Prepare("what cause Disease"))
#
# FF = SynonimToolKit()
# print(FF.ReplaceSynonym("can i prevent heart attack  from drinking Beer","diseases"))



# print(FF.Prepare("can i get heart attack from drinking Beer"))

# tokanizedQuestion = ["what","is","heart","attack","caused"]
# bigramlist =["heart_attack"]
# print(FF._RemoveBigrams(tokanizedQuestion,bigramlist))

# print(FF.Prepare('what cause heart attack'))