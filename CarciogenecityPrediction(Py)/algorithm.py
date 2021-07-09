import math
import random
from rdflib import Graph, Namespace, Literal, URIRef
from Ontolearn.ontolearn import KnowledgeBase
from Ontolearn.ontolearn.concept_learner import CELOE

#from Ontolearn.ontolearn.metrics import F1, PredictiveAccuracy, CELOEHeuristic, DLFOILHeuristic

subjects = set()
predicates = set()
eachPositiveLabels = []
eachNegativeLabels = []
allPositiveLabels = []
allNegativeLabels = []

# Initializing a graph and parsing a turtle file in graph structure

g = Graph()
result = g.parse("kg-mini-project-train_v2_mini.ttl", format="ttl")

for s in g.subjects():
    subjects.add(s)
for p in g.predicates():
    predicates.add(p)

for s in list(subjects):
    for p in list(predicates):
        if str(p) == "https://lpbenchgen.org/property/includesResource":
            for o in g.objects(s, p):
                eachPositiveLabels = [s, o]
                allPositiveLabels.append(eachPositiveLabels)
        elif str(p) == "https://lpbenchgen.org/property/excludesResource":
            for o in g.objects(s, p):
                eachNegativeLabels = [s, o]
                allNegativeLabels.append(eachNegativeLabels)


posForOneLP = set()
for eachLabel in allPositiveLabels:
    if str(eachLabel[0]) == "https://lpbenchgen.org/resource/lp_4":
        posForOneLP.add(str(eachLabel[1]))

negForOneLP = set()
for eachLabel in allNegativeLabels:
    if str(eachLabel[0]) == "https://lpbenchgen.org/resource/lp_4":
        negForOneLP.add(str(eachLabel[1]))

#print(posForOneLP)

#print("\n ================ NEGATIVE EXAMPLES FOR LP_4 ===================\n")
#print(negForOneLP)

kb = KnowledgeBase(path='carcinogenesis.owl')

p = posForOneLP
n = negForOneLP



'''model = (knowledge_base=kb,
                             quality_func=F1(),
                             heuristic_func=DLFOILHeuristic(),
                             iter_bound=1,
                             verbose=False)'''

model =CELOE(knowledge_base=kb, max_runtime=10)

list_p = list(p)
len_p = len(list_p)
train_length = math.ceil(len_p*.8)
train_p = random.sample(list_p, train_length)
test_p = []
for item in list_p:
    if item not in train_p:
        test_p.append(item)
train_p = set(train_p)
test_p = set(test_p)

list_n = list(n)
len_n = len(list_n)
train_length = math.ceil(len_n*.8)
train_n = random.sample(list_n, train_length)
test_n = []
for item in list_n:
    if item not in train_n:
        test_n.append(item)
train_n = set(train_n)
test_n = set(test_n)

model.fit(pos=train_p, neg=train_n)
hypotheses = model.best_hypotheses(n=3)
predictions = model.predict(individuals=list(test_p) + list(test_n), hypotheses=hypotheses)
predictions['pred'] = round(predictions.mean(1))

out_g = Graph()
lpres = Namespace("https://lpbenchgen.org/resource/")
lpprop = Namespace("https://lpbenchgen.org/property/")
carcinogenesis= Namespace("http://dl-learner.org/carcinogenesis#")
out_g.bind("carcinogenesis", carcinogenesis)
out_g.bind("lpres", lpres)
out_g.bind("lpprop", lpprop)
result_1pos = URIRef(lpres.result_1pos)
result_1neg = URIRef(lpres.result_1neg)
out_g.add((result_1pos, lpprop.belongsToLP , Literal(True) ))
out_g.add((result_1pos, lpprop.pertainsTo , lpres.lp_4 ))

out_g.add((result_1neg, lpprop.belongsToLP , Literal(False) ))
out_g.add((result_1neg, lpprop.pertainsTo , lpres.lp_4 ))


for item in predictions.index:
    pred = predictions.loc[item]['pred']
    comp = str(item).split('.')[-1]
    if pred > 0.5:
        out_g.add((result_1pos, lpprop.resource , carcinogenesis[comp]) )
    else:
        out_g.add((result_1neg, lpprop.resource, carcinogenesis[comp]))
#print(predictions)
out_g.serialize(destination='prediction_output.ttl', format='turtle')
print('end')
