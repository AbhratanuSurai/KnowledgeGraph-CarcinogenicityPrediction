import rdflib
from rdflib import Graph
from ontolearn import KnowledgeBase, SampleConceptLearner
from ontolearn.metrics import F1, PredictiveAccuracy, CELOEHeuristic, DLFOILHeuristic
from Ontolearn.ontolearn.concept_learner import CELOE

graph = Graph()
subjects = set()
predicates = set()
each_positive_labels = []
each_negative_labels = []
all_positive_labels = []
all_negative_labels = []
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
        eachPositiveLabels is a list of positive examples
            that contains 2 rdflib.term.URIRef items;
            1) Name of the learning problem
            2) The carcinogenesis bond itself

            allPositiveLabels is a list of lists of above type

        Similar lists also exists for negative examples as well
        namely eachLearningProblemNegativeLabels and allLearningProblemPositiveLabels.
        """

        for s in list(subjects):
            for p in list(predicates):
                if str(p) == "https://lpbenchgen.org/property/includesResource":
                    for o in graph.objects(s, p):
                        each_positive_labels = [s, o]
                        all_positive_labels.append(each_positive_labels)
                elif str(p) == "https://lpbenchgen.org/property/excludesResource":
                    for o in graph.objects(s, p):
                        each_negative_labels = [s, o]
                        all_negative_labels.append(each_negative_labels)

    """
    storing all carcinigenesis bond of given learning problems 
    with positive and negative labels in separate variables
    """

    def get_labels(self, learning_problem):
        pos_for_one_lp.clear(), neg_for_one_lp.clear()

        for each_label in all_positive_labels:
            if str(each_label[0]) == str(learning_problem):
                pos_for_one_lp.add(str(each_label[1]))

        for each_label in each_negative_labels:
            if str(each_label[0]) == str(learning_problem):
                neg_for_one_lp.add(str(each_label[1]))


"""
Creating a model and train the model with the data,
that has been fetched from the given kg-mini-project-train_v2.ttl file
"""
parser = TurtleParser()
parser.parse_rdf()
kb = KnowledgeBase(path='carcinogenesis.owl')
model = CELOE(knowledge_base=kb, max_runtime=10)

for sub in subjects:
    parser.get_labels(sub)
    p = pos_for_one_lp
    n = neg_for_one_lp
    model.fit(pos=p, neg=n)
    hypotheses = model.best_hypotheses(n=3)
    predictions = model.predict(individuals=list(p) + list(n), hypotheses=hypotheses)
    print(predictions)
    print('end')
