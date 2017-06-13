a=[['coughing', 'large', 'amounts', 'thick', 'mucus', 'every', 'day'], ['breathing', 'difficulties'], ['chest', 'pain'], ['pain', 'bones'], ['weight', 'loss'], ['coughing', 'blood'], ['fatigue'], ['loss', 'appetite'], ['recurring', 'infections']]
b=[['coughing', 'large', 'amounts', 'thick', 'mucus', 'every', 'day'], ['breathing', 'difficulties'], ['chest', 'pain'], ['weight', 'loss'], ['coughing', 'blood'], ['fatigue'], ['loss', 'appetite'], ['recurring', 'infections']]



def findCommon(a,b):
    uncommon_set = []
    for item in a:
        match_found = False
        for item2 in b:
            if(set(item) == set(item2)):
                match_found = True
                break
        if not match_found:
            uncommon_set.append(item)
    return  uncommon_set

print("Items that are in a but not in b"+ str(findCommon(a,b)))



# print("Items that are in b but not in a"+ str(findCommon(b,a)))
#
# f1 = findCommon(a,b)
# f2 =findCommon(b,a)
#
# f3=[]
# f3.extend(f1)
# f3.extend(f2)
# print(f3)
