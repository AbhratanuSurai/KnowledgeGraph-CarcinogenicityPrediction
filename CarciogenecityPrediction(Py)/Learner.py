from ontolearn.concept_learner import CELOE

class Learner:

    def get_predictions(self, pos, neg, unk, kb):
        # returns 3 classifications of the unknown individuals for one particular learning problem,
        # based on the positive and negative examples
        model = CELOE(knowledge_base=kb, max_runtime=50)
        model.fit(pos=pos, neg=neg)
        model.save_best_hypothesis(n=3)
        hypotheses = model.best_hypotheses(n=3)
        return model.predict(individuals=list(unk), hypotheses=hypotheses)