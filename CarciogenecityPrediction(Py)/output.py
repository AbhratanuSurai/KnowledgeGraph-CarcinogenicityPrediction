from rdflib import Graph, Namespace, Literal, URIRef


class ClassificationResult:
    def __init__(self):
        self.g = Graph()
        self.nm = self.g.namespace_manager
        self.ns_carcinogenesis = Namespace("http://dl-learner.org/carcinogenesis#")
        self.ns_resource = Namespace("https://lpbenchgen.org/resource/")
        self.ns_property = Namespace("https://lpbenchgen.org/property/")
        self.pos_predictions = []
        self.neg_predictions = []

    def create_prefixes(self):

        self.nm.bind("carcinogenesis", self.ns_carcinogenesis)
        self.nm.bind("lpres", self.ns_resource)
        self.nm.bind("lpprop", self.ns_property)

    def get_output(self, learning_problem, solution):

        # Storing all the positive and negative predictions in separate variables
        outer_dict = solution.to_dict()
        for i in outer_dict:
            inner_dict = outer_dict[i]
            for j in inner_dict:
                if inner_dict[j] == 1.0:
                    positive = str(j).split(".")
                    self.pos_predictions.append(positive[-1])
                elif inner_dict[j] == 0.0:
                    negative = str(j).split(".")
                    self.neg_predictions.append(negative[-1])

        # for positive predictions
        s1 = self.ns_resource.result_1pos
        p1 = self.ns_property.belongsToLP
        o1 = Literal(True)
        self.g.add((s1, p1, o1))

        p2 = self.ns_property.pertainsTo
        lp_name = str(learning_problem).split("/")
        o2 = lp_name[-1]
        self.g.add((s1, p2, self.ns_resource[o2]))

        for pos_element in self.pos_predictions:
            p3 = self.ns_property.resource
            o3 = pos_element
            self.g.add((s1, p3, self.ns_carcinogenesis[o3]))

        # for negative predictions

        s1 = self.ns_resource.result_1neg
        p1 = self.ns_property.belongsToLP
        o1 = Literal(False)
        self.g.add((s1, p1, o1))

        p2 = self.ns_property.pertainsTo
        lp_name = str(learning_problem).split("/")
        o2 = lp_name[-1]
        self.g.add((s1, p2, self.ns_resource[o2]))

        for neg_element in self.neg_predictions:
            p3 = self.ns_property.resource
            o3 = neg_element
            self.g.add((s1, p3, self.ns_carcinogenesis[o3]))

        self.g.serialize(destination='output_classification_result.ttl', format='turtle')
