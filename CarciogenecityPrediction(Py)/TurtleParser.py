import rdflib
from rdflib import Graph

subjects = set()
predicates = set()
eachPositiveLabels = []
eachNegativeLabels = []
allPositiveLabels = []
allNegativeLabels = []

# Initializing a graph and parsing a turtle file in graph structure

g = Graph()
result = g.parse("kg-mini-project-train_v2.ttl", format="ttl")

# Storing distinct subjects and distinct predicates
# in the sets subjects and predicates

for s in g.subjects():
    subjects.add(s)
for p in g.predicates():
    predicates.add(p)

# eachPositiveLabels is a list of positive examples
#     that contains 2 rdflib.term.URIRef items;
#     1) Name of the learning problem
#     2) The carcinogenesis bond itself
#
#     allPositiveLabels is a list of lists of above type
#
# Similar lists also exists for negative examples as well
# namely eachLearningProblemNegativeLabels and allLearningProblemPositiveLabels.

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

print("===== All positive examples ===== \n")
print(allPositiveLabels)
print("\n===== All Negative examples ===== \n")
print(allNegativeLabels)


