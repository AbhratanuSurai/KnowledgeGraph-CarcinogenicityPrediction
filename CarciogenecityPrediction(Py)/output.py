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
        self.learning_problems = []

    def create_prefixes(self):

        self.nm.bind("carcinogenesis", self.ns_carcinogenesis)
        self.nm.bind("lpres", self.ns_resource)
        self.nm.bind("lpprop", self.ns_property)

    def make_output(self, predictions):

        for lp in predictions.keys():
            self.learning_problems.append(str(lp))
            # print(lp)
            # print('CHECKING', self.learning_problems)
        i = 0
        for each_prediction in predictions.values():
            each_prediction['pred'] = round(each_prediction.mean(1))



            # for pos_element in self.pos_predictions:
            #     p3 = self.ns_property.resource
            #     o3 = pos_element
            #     self.g.add((s1, p3, self.ns_carcinogenesis[o3]))



            # for neg_element in self.neg_predictions:
            #     p3 = self.ns_property.resource
            #     o3 = neg_element
            #     self.g.add((s1, p3, self.ns_carcinogenesis[o3]))

            for item in each_prediction.index:
                pred = each_prediction.loc[item]['pred']
                comp = str(item).split('.')[-1]
                if pred > 0.5:
                    # for positive predictions
                    s1 = self.ns_resource.result_1pos
                    p1 = self.ns_property.belongsToLP
                    o1 = Literal(True)
                    self.g.add((s1, p1, o1))

                    p2 = self.ns_property.pertainsTo
                    lp_name = str(self.learning_problems[i]).split("/")
                    o2 = lp_name[-1]
                    self.g.add((s1, p2, self.ns_resource[o2]))
                    self.g.add((self.ns_resource.result_1pos, self.ns_property.resource, self.ns_carcinogenesis[comp]))
                else:
                    # for negative predictions

                    s1 = self.ns_resource.result_1neg
                    p1 = self.ns_property.belongsToLP
                    o1 = Literal(False)
                    self.g.add((s1, p1, o1))

                    p2 = self.ns_property.pertainsTo
                    lp_name = str(self.learning_problems[i]).split("/")
                    o2 = lp_name[-1]
                    self.g.add((s1, p2, self.ns_resource[o2]))
                    self.g.add((self.ns_resource.result_1neg, self.ns_property.resource, self.ns_carcinogenesis[comp]))

            i = i + 1
        # Storing all the positive and negative predictions in separate variables
        # outer_dict = solution.to_dict()
        # for i in outer_dict:
        #     inner_dict = outer_dict[i]
        #     for j in inner_dict:
        #         if inner_dict[j] == 1.0:
        #             positive = str(j).split(".")
        #             self.pos_predictions.append(positive[-1])
        #         elif inner_dict[j] == 0.0:
        #             negative = str(j).split(".")
        #             self.neg_predictions.append(negative[-1])

        # predictions['pred'] = round(predictions.mean(1))

        # self.g.serialize(destination='output_classification_result.ttl', format='turtle')

    def get_output(self):
        self.g.serialize(destination='output_classification_result.ttl', format='turtle', encoding="utf-8")
        # print(self.g.serialize(format='n3'))

