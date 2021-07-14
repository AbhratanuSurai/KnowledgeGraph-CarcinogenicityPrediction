class Evaluator:

    def evaluate(self, solution, pos, neg):
        # Will calculate the F1-score, based on the the learned classification
        # and the actual positive and negative Classification.
        # Sometimes in line 14/19 the evaluator bugs.
        # It seems like row[solut ... gives out a series in case, instead of a single value, when it bugs.
        tp = 0
        fp = 0
        fn = 0
        tn = 0
        for i, row in solution.iterrows():
            ind = list(str(i))
            ind[14] = "#"
            if row[solution.columns[0]] > 0.5:
                if "http://dl-learner.org/"+"".join(ind) in str(pos):
                    tp += 1
                else:
                    fp += 1
            elif row[solution.columns[0]] < 0.5:
                if "http://dl-learner.org/"+"".join(ind) in str(neg):
                    tn += 1
                else:
                    fn += 1
        accuracy = (tp + tn) / len(pos + neg)
        print("accuracy:", accuracy)
        recall = tp / (tp+fn)
        precision = tp / (tp+fp)
        f1 = 2 / ( (1/precision) + (1/recall) )
        print("recall:", recall)
        print("precision:", precision)
        print("F1-Score:", f1)