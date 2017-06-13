from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from SPARQLWrapper import SPARQLWrapper, JSON
stop = set(stopwords.words('english'))
questionwords =['what','when','why','which','who','how','whose','whome','is','can','am','symptom','treatment','symptoms','treatments','causes','cause','prevention','prevent','disease','diseases','risk','risks']
sentense = "what are the Obesity of avoid cartinogens at work diabetes "

def checkDise(phrase):

    queryTop = '''

PREFIX base:<http://test.org/BeyonUpload.owl#>
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
PREFIX  rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX hsp:<http://www.semanticweb.org/gayantha/ontologies/2017/1/untitled-ontology-15#>

SELECT  ?classLabel
WHERE {
   ?Matchinstance rdf:type ?Class.
     ?Matchinstance rdfs:label "'''

    queryBottom='''".
     ?Class rdfs:label ?classLabel.
}
    
    
    '''
    # http: // localhost:3030 / ds / query
    query = queryTop+phrase+queryBottom
    # sparql = SPARQLWrapper("http://67.207.85.162:3030/ds/query")
    sparql = SPARQLWrapper("http://localhost:3030/ds/query")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    value =[]
    for result in results["results"]["bindings"]:
        value =(result["classLabel"]['value']).encode('utf-8')

    if(len(value) == 0):
        return False,value
    else:
        return True,value

    # if phrase =="daily_cough_be":
    #  return  True
    # else:
    #  return  False
def FindClasses(sentense,n_gram =3):
    tokenized_sentense = word_tokenize(sentense.lower())

    n_gram_value = n_gram
    for pointer_index, word in enumerate(tokenized_sentense):
        if tokenized_sentense[pointer_index] == "":
            continue
        else:
            current_n_gram = n_gram_value

            while (current_n_gram >= 0):
                phrase = tokenized_sentense[pointer_index]
                loop_index = 1
                while (loop_index <= current_n_gram and len(tokenized_sentense) > pointer_index + loop_index):
                    current_word = tokenized_sentense[pointer_index + loop_index]
                    if (current_word != ""):
                        phrase = phrase + "_" + current_word
                    loop_index += 1
                found = False
                if (phrase != "" and phrase not in stop):
                    discheck = checkDise(phrase)
                else:
                    discheck = [False, "nop"]

                if phrase != "" and discheck[0] and phrase not in stop and phrase not in questionwords:
                    tokenized_sentense[pointer_index] = discheck[1]
                    erase_index = pointer_index + 1
                    while (erase_index <= current_n_gram + pointer_index):
                        if (erase_index < len(tokenized_sentense)):
                            tokenized_sentense[erase_index] = ""
                        erase_index += 1
                    found = True
                if found:
                    break
                current_n_gram -= 1

    full_sentense =""

    for word in tokenized_sentense:
        if word !="":
            full_sentense +=word +" "


    return full_sentense


# print(FindClasses(sentense,4))