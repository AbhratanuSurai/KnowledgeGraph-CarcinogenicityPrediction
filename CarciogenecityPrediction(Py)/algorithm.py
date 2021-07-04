from rdflib import Graph
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
result = g.parse("kg-mini-project-train_v2.ttl", format="ttl")

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
model.fit(pos=p, neg=n)
hypotheses = model.best_hypotheses(n=3)
predictions = model.predict(individuals=list(p) + list(n), hypotheses=hypotheses)
print(predictions)
print('end')