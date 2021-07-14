from ontolearn import KnowledgeBase
from ontolearn.concept_learner import CELOE
from sklearn.model_selection import train_test_split

from TurtleParser import TurtleParser
from output import ClassificationResult

"""
Here we tested our work. Is not cleaned up, but still in the repository for transparency.
"""

def get_predictions(pos, neg, unk, kb):
    # returns 3 classifications of the unknown individuals for one particular learning problem,
    # based on the positive and negative examples
    model = CELOE(knowledge_base=kb, max_runtime=50)
    model.fit(pos=pos, neg=neg)
    model.save_best_hypothesis(n=3)
    hypotheses = model.best_hypotheses(n=3)
    return model.predict(individuals=list(unk), hypotheses=hypotheses)

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


if __name__ == "__main__":
    test = TurtleParser()
    cr = ClassificationResult()
    test.parse_rdf("kg-mini-project-train_v2.ttl")
    sub = test.get_subjects()
    solution = {}
    data = {}
    sol_list = []
    for i in sub:
        data_pos = test.get_labels(i, 1)
        data_neg = test.get_labels(i, 0)
        pos_train, pos_val = train_test_split(list(data_pos), test_size=0.2)
        neg_train, neg_val = train_test_split(list(data_neg), test_size=0.2)
        u = pos_val + neg_val
        kb = KnowledgeBase(path='carcinogenesis.owl')
        sol = get_predictions(set(pos_train), set(neg_train), u, kb)
        pos_data = (pos_train, pos_val)
        neg_data = (neg_train, neg_val)
        lp_data = (pos_data, neg_data)
        data[i] = lp_data
        solution[i] = sol
        cr.create_prefixes()
        cr.make_output(sol, i)

    cr.get_output("RERUN")