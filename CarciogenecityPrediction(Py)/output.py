import rdflib
from rdflib.namespace import RDF
import algorithm as alg


class ClassificationResult:
    def __init__(self):
        self.g = rdflib.Graph()
        self.nm = self.g.namespace_manager
        self.ns_carcinogenesis = rdflib.Namespace()
        self.ns_resource = rdflib.Namespace()
        self.ns_property = rdflib.Namespace()
        self.pos_predictions = []
        self.neg_predictions = []
    def create_prefixes(self):
        # g = rdflib.Graph()

        carcinogenesis_uri = "http://dl-learner.org/carcinogenesis#"
        resource_uri = "https://lpbenchgen.org/resource/"
        property_uri = "https://lpbenchgen.org/property/"

        self.ns_carcinogenesis = rdflib.Namespace(carcinogenesis_uri)
        self.ns_resource = rdflib.Namespace(resource_uri)
        self.ns_property = rdflib.Namespace(property_uri)

        prefix = "carcinogenesis"
        self.nm.bind(prefix, ns_carcinogenesis)
        prefix = "lpres"
        self.nm.bind(prefix, ns_resource)
        prefix = "lpprop"
        self.nm.bind(prefix, ns_property)


    def get_output(self, learning_problem):

        outer_dict = alg.predictions.to_dict()
        for i in outer_dict:
            inner_dict = outer_dict[i]
            for j in inner_dict:
                if inner_dict[j] == 1.0:
                    positive = str(j).split(".")
                    self.pos_predictions.append(positive[-1])
                elif inner_dict[j] == 0.0:
                    negative = str(j).split(".")
                    self.neg_predictions.append(negative[-1])

        s1 = self.ns_resource.result_1pos
        p1 = self.ns_property.belongsToLP
        o1 = "true"
        self.g.add((s1, p1, o1,))

        p2 = self.ns_property.pertainsTo
        lp_name = str(learning_problem).split("/")
        o2 = self.ns_resource.lp_name[-1]
        self.g.add((s1, p2, o2,))

        for pos_element in self.pos_predictions:
            p3 = self.ns_property.resource
            o3 = pos_element
            self.g.add((s1, p3, o3,))


        # for negative resources

        s1 = self.ns_resource.result_1neg
        p1 = self.ns_property.belongsToLP
        o1 = "false"
        self.g.add((s1, p1, o1,))

        p2 = self.ns_property.pertainsTo
        lp_name = str(learning_problem).split("/")
        o2 = self.ns_resource.lp_name[-1]
        self.g.add((s1, p2, o2,))

        for neg_element in self.neg_predictions:
            p3 = self.ns_property.resource
            o3 = neg_element
            self.g.add((s1, p3, o3,))


