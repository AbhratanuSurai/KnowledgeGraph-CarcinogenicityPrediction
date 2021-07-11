from ontolearn import KnowledgeBase
from sklearn.model_selection import train_test_split

from Learner import Learner
from TurtleParser import TurtleParser
from output import ClassificationResult
from eval import Evaluator
from missing import missing_individuals

def evaluate(solution, pos, neg):
    # Will calculate the F1-score, based on the the learned classification
    # and the actual positive and negative Classification.
    tp = 0
    fp = 0
    fn = 0
    tn = 0
    for i, row in solution.iterrows():
        ind = list(str(i))
        ind[14] = "#"
        if row[solution.columns[0]] > 0.5:
            if "http://dl-learner.org/" + "".join(ind) in str(pos):
                tp += 1
            else:
                fp += 1
        elif row[solution.columns[0]] < 0.5:
            if "http://dl-learner.org/" + "".join(ind) in str(neg):
                tn += 1
            else:
                fn += 1
    accuracy = (tp + tn) / len(pos + neg)
    print("accuracy:", accuracy)
    recall = tp / (tp + fn)
    precision = tp / (tp + fp)
    f1 = 2 / ((1 / precision) + (1 / recall))
    print("recall:", recall)
    print("precision:", precision)
    print("F1-Score:", f1)

"""
if __name__ == "__main__":
    test = TurtleParser()
    cr = ClassificationResult()
    test.parse_rdf()
    bla = test.get_subjects()
    solution = {}
    data = {}
    sol_list = []
    for i in bla:
        data_pos = test.get_labels(i, 1)
        data_neg = test.get_labels(i, 0)
        pos_train, pos_val = train_test_split(list(data_pos), test_size=0.2)
        neg_train, neg_val = train_test_split(list(data_neg), test_size=0.2)
        u = pos_val + neg_val
        l = Learner()
        kb = KnowledgeBase(path='carcinogenesis.owl')
        sol = l.get_predictions(set(pos_train), set(neg_train), u, kb)
        pos_data = (pos_train, pos_val)
        neg_data = (neg_train, neg_val)
        lp_data = (pos_data, neg_data)
        data[i] = lp_data
        solution[i] = sol
        #print("Learning Problem:", i)
        #evaluate(sol, pos_val, neg_val)
        cr.create_prefixes()
        cr.make_output(sol, i)

    cr.get_output()
"""

if __name__ == "__main__":
    test = TurtleParser()
    cr = ClassificationResult()
    test.parse_rdf("kg-mini-project-grading.ttl")
    bla = test.get_subjects()
    solution = {}
    data = {}
    sol_list = []
    unknown = missing_individuals()
    for i in bla:
        data_pos = test.get_labels(i, 1)
        data_neg = test.get_labels(i, 0)
        u = unknown.get_unknown_individuals(set(test.get_labels(i, 2)))
        l = Learner()
        kb = KnowledgeBase(path='carcinogenesis.owl')
        sol = l.get_predictions(set(data_pos), set(data_neg), set(u), kb)
        lp_data = (data_pos, data_neg, u)
        data[i] = lp_data
        solution[i] = sol
        print(sol)
        # print("Learning Problem:", i)
        # evaluate(sol, pos_val, neg_val)
        cr.create_prefixes()
        cr.make_output(sol, i)
    cr.get_output()
    print("finish")
