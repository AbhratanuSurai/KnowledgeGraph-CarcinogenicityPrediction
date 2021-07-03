from ontolearn import KnowledgeBase,SampleConceptLearner
from ontolearn.metrics import F1, PredictiveAccuracy, CELOEHeuristic,DLFOILHeuristic

if __name__ == '__main__':
    kb = KnowledgeBase(path='carcinogenesis.owl')
    model = SampleConceptLearner(knowledge_base=kb,
                                 quality_func=F1(),
                                 terminate_on_goal=True,
                                 heuristic_func=DLFOILHeuristic(),
                                 iter_bound=100,
                                 verbose=False)
    c = "http://dl-learner.org/carcinogenesis#"
    p = {c+ "d28", c+ "d79", c+ "d27"}
    n = {c+ "bond961", c+ "non_ar_6c_ring-557", c+ "bond7937", c+ "d4_14", c+ "bond3490", c+ "sulfide-2081", c+ "d95_9",
         c+ "bond9053", c+ "bond6346"}
    model.predict(pos=p, neg=n)
    model.show_best_predictions(top_n=10)

