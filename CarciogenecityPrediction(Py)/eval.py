from rdflib import URIRef

class Evaluator:

    def evaluate(self, solution, pos, neg):
        c = 0
        for i, row in solution.iterrows():
            ii = list(str(i))
            ii[14] = "#"
            if row[solution.columns[0]] > 0.5:
                if "http://dl-learner.org/"+"".join(ii) in str(pos):
                    c += 1
            elif row[solution.columns[0]] < 0.5:
                if "http://dl-learner.org/"+"".join(ii) in str(neg):
                    c += 1
        rate = c / len(pos + neg)
        print(rate)