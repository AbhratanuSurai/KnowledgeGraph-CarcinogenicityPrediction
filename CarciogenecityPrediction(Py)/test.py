from ontolearn import KnowledgeBase

from sklearn.model_selection import train_test_split

from Learner import Learner
from TurtleParser import TurtleParser
from output import ClassificationResult
if __name__ == "__main__":
    test = TurtleParser()
    cr = ClassificationResult()
    test.parse_rdf()
    bla = test.get_subjects()
    solution = {}
    data = {}
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
        cr.create_prefixes()
        cr.get_output(i, sol)
