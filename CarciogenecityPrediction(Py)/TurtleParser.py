from rdflib import Graph


class TurtleParser:

    def __init__(self):
        self.graph = Graph()
        self.subjects = set()
        self.predicates = set()

    def parse_rdf(self, path="kg-mini-project-train_v2.ttl"):

        self.graph.parse(path, format="ttl")

        """
        Storing distinct subjects and distinct predicates
        in the sets subjects and predicates
        """
        for s in self.graph.subjects():
            self.subjects.add(s)
        for p in self.graph.predicates():
            self.predicates.add(p)

    """
    storing all carcinigenesis bond of given learning problems 
    with positive and negative labels in separate variables
    """

    def get_subjects(self):
        return self.subjects

    def get_labels(self, learning_problem, pos):
        pos_for_one_lp = set()
        neg_for_one_lp = set()
        all_for_one_lp = set()

        if pos == 1:
            for p in list(self.predicates):
                if str(p) == "https://lpbenchgen.org/property/includesResource":
                    for o in self.graph.objects(learning_problem, p):
                        pos_for_one_lp.add(str(o))
            return pos_for_one_lp
        elif pos == 0:
            for p in list(self.predicates):
                if str(p) == "https://lpbenchgen.org/property/excludesResource":
                    for o in self.graph.objects(learning_problem, p):
                        neg_for_one_lp.add(str(o))
            return neg_for_one_lp
        else:
            for p in list(self.predicates):
                if str(p) == "https://lpbenchgen.org/property/includesResource" or str(p) == "https://lpbenchgen.org/property/excludesResource":
                    for o in self.graph.objects(learning_problem, p):
                        all_for_one_lp.add(str(o))
            return all_for_one_lp

