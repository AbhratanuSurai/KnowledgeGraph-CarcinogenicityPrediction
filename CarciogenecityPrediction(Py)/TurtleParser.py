import rdflib
from rdflib import Graph
# from ontolearn import KnowledgeBase, SampleConceptLearner
# from ontolearn.metrics import F1, PredictiveAccuracy, CELOEHeuristic, DLFOILHeuristic
# from Ontolearn.ontolearn.concept_learner import CELOE

graph = Graph()
subjects = set()
predicates = set()
pos_for_one_lp = set()
neg_for_one_lp = set()


class TurtleParser():

    def parse_rdf(self):

        graph.parse("kg-mini-project-train_v2.ttl", format="ttl")

        """
        Storing distinct subjects and distinct predicates
        in the sets subjects and predicates
        """
        for s in graph.subjects():
            subjects.add(s)
        for p in graph.predicates():
            predicates.add(p)

    """
    storing all carcinigenesis bond of given learning problems 
    with positive and negative labels in separate variables
    """

    def get_labels(self, learning_problem, pos):
        pos_for_one_lp.clear(), neg_for_one_lp.clear()

        if(pos == true):
            for p in list(predicates):
                if str(p) == "https://lpbenchgen.org/property/includesResource":
                    for o in graph.objects(learning_problem, p):
                        pos_for_one_lp.add(str(o))
            return pos_for_one_lp
        else:
            for p in list(predicates):
                if str(p) == "https://lpbenchgen.org/property/excludesResource":
                    for o in graph.objects(learning_problem, p):
                        neg_for_one_lp.add(str(o))
                return neg_for_one_lp



parser = TurtleParser()
parser.parse_rdf()
parser.get_labels(list(subjects)[2])
print(pos_for_one_lp)
print(list(subjects)[2])
print(subjects)
