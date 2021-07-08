from rdflib import URIRef

class Evaluator:

    def evaluate(self, solution, pos, neg):
        c = 0
        tp = 0
        fp = 0
        fn = 0
        tn = 0
        for i, row in solution.iterrows():
            ii = list(str(i))
            ii[14] = "#"
            if row[solution.columns[0]] > 0.5:
                if "http://dl-learner.org/"+"".join(ii) in str(pos):
                    c += 1
                    tp += 1
                else:
                    fp += 1
            elif row[solution.columns[0]] < 0.5:
                if "http://dl-learner.org/"+"".join(ii) in str(neg):
                    c += 1
                    tn += 1
                else:
                    fn += 1
        accuracy = c / len(pos + neg)
        print("accuracy:", accuracy)
        recall = tp / (tp+fn)
        precision = tp / (tp+fp)
        f1 = 2 / ((1/precision) + (1/recall))
        print("recall:", recall)
        print("precision:", precision)
        print("F1-Score:", f1)
