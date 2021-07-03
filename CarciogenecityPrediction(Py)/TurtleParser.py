import rdflib
from rdflib import Graph

subjects = set()
predicates = set()
objects = set()
eachPositiveLabels = []
eachNegativeLabels = []
allPositiveLabels = []
allNegativeLabels = []


g = Graph()
result = g.parse("kg-mini-project-train_v2.ttl", format="ttl")

# print out all the triples in the graph
# print(len(g))
for s in g.subjects():
    subjects.add(s)
for p in g.predicates():
    predicates.add(p)
# print(subjects)
# print(predicates)

# for s in subjects:
#     for p in predicates:
#         for o in g.objects(s, p):
#             objects.add(o)
# print(objects)

# for triple in g.triples( (rdflib.term.URIRef('https://lpbenchgen.org/resource/lp_4'),
#                           rdflib.term.URIRef('https://lpbenchgen.org/property/includesResource'),
#                           None) ):
#     print(triple)

for s in list(subjects):
    for p in list(predicates):
        if str(p) == "https://lpbenchgen.org/property/includesResource":
            for o in g.objects(s, p):
                eachPositiveLabels = [s, p, o]
                allPositiveLabels.append(eachPositiveLabels)
        elif str(p) == "https://lpbenchgen.org/property/excludesResource":
            for o in g.objects(s, p):
                eachNegativeLabels = [s, p, o]
                allNegativeLabels.append(eachNegativeLabels)
print(len(allPositiveLabels))
print(len(allNegativeLabels))


