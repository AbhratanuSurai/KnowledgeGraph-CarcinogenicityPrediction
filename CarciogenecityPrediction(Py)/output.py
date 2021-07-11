from rdflib import Graph, Namespace, Literal


class ClassificationResult:
    def __init__(self):
        self.g = Graph()
        self.nm = self.g.namespace_manager
        self.ns_carcinogenesis = Namespace("http://dl-learner.org/carcinogenesis#")
        self.ns_resource = Namespace("https://lpbenchgen.org/resource/")
        self.ns_property = Namespace("https://lpbenchgen.org/property/")
        self.result_number = 1

    def create_prefixes(self):
        """This method is responsible to create the prefixes for the output turtle file."""

        self.nm.bind("carcinogenesis", self.ns_carcinogenesis)
        self.nm.bind("lpres", self.ns_resource)
        self.nm.bind("lpprop", self.ns_property)

    def make_output(self, predictions, learning_problem):
        """This method is getting the name of a learning problem and
        predictions for that learning problem as input parameters. It is then
        responsible to convert the predictions of all individual learning problems
        to the mentioned turtle RDF format by adding them in a graph.
        """

        predictions['pred'] = round(predictions.mean(1))

        # This block is responsible to create and  add the first two triples
        # for positive predictions of one learning problem in the graph
        # as per the provided output format.

        lpres_pos = "result_" + str(self.result_number) + "pos"
        s1_pos = self.ns_resource[lpres_pos]
        p1_pos = self.ns_property.belongsToLP
        o1_pos = Literal(True)
        self.g.add((s1_pos, p1_pos, o1_pos))

        p2_pos = self.ns_property.pertainsTo
        lp_name = str(learning_problem).split("/")
        o2_pos = lp_name[-1]
        self.g.add((s1_pos, p2_pos, self.ns_resource[o2_pos]))

        # This block is responsible to create and  add the first two triples
        # for negative predictions of one learning problem in the graph
        # as per the provided output format.

        lpres_neg = "result_" + str(self.result_number) + "neg"
        s1_neg = self.ns_resource[lpres_neg]
        p1_neg = self.ns_property.belongsToLP
        o1_neg = Literal(False)
        self.g.add((s1_neg, p1_neg, o1_neg))

        p2_neg = self.ns_property.pertainsTo
        lp_name = str(learning_problem).split("/")
        o2_neg = lp_name[-1]
        self.g.add((s1_neg, p2_neg, self.ns_resource[o2_neg]))

        # Iterating over all the predictions of the carcinogenesis bonds for both
        # positive and negative predictions and adding them into the graph as triple structure.

        for item in predictions.index:
            pred = predictions.loc[item]['pred']
            comp = str(item).split('.')[-1]
            if pred > 0.5:
                self.g.add((s1_pos, self.ns_property.resource, self.ns_carcinogenesis[comp]))
            else:
                self.g.add((s1_neg, self.ns_property.resource, self.ns_carcinogenesis[comp]))

        self.result_number = self.result_number + 1

    def get_output(self,i="0"):
        """"This method is providing the output graph
        which consists of the prediction of all the learning problems
        as the required turtle RDF file.
        """
        self.g.serialize(destination='output_classification_result'+i+'.ttl', format='turtle', encoding="utf-8")
