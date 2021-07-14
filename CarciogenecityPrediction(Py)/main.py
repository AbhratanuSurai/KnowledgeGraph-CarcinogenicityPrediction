from ontolearn import KnowledgeBase
from ontolearn.concept_learner import CELOE

from TurtleParser import TurtleParser

from output import ClassificationResult

from missing import missing_individuals

def get_predictions(pos, neg, unk, kb):
    # returns 3 classifications of the unknown individuals for one particular learning problem,
    # based on the positive and negative examples
    model = CELOE(knowledge_base=kb, max_runtime=50)
    model.fit(pos=pos, neg=neg)
    model.save_best_hypothesis(n=1)
    hypotheses = model.best_hypotheses(n=1)
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
    # print("accuracy:", accuracy)
    recall = tp / (tp + fn)
    precision = tp / (tp + fp)
    f1 = 2 / ((1 / precision) + (1 / recall))
    # print("recall:", recall)
    # print("precision:", precision)
    # print("F1-score:", f1)
    return f1

if __name__ == "__main__":
    p = TurtleParser()
    cr = ClassificationResult()
    cr.create_prefixes()
    p.parse_rdf("kg-mini-project-grading.ttl")
    sub = p.get_subjects()
    unknown = missing_individuals()
    for i in sub:
        data_pos = p.get_labels(i, 1)
        data_neg = p.get_labels(i, 0)
        u = unknown.get_unknown_individuals(set(p.get_labels(i, 2)))
        kb = KnowledgeBase(path='carcinogenesis.owl')
        sol = get_predictions(set(data_pos), set(data_neg), set(u), kb)
        print(sol)
        cr.make_output(sol, i)
    cr.get_output("_final")