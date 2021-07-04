#from ontolearn import KnowledgeBase,base_concept_learner
from ontolearn import KnowledgeBase
from ontolearn.concept_learner import CELOE

"""
if __name__ == '__main__':
    kb = KnowledgeBase(path='carcinogenesis.owl')
    model = base_concept_learner
    c = 'http://dl-learner.org/carcinogenesis#'
    p = {c+  'd28', c+ 'd79', c+ 'd27'}
    n = {c+ 'bond961', c+ 'non_ar_6c_ring-557', c+ 'bond7937', c+ 'd4_14', c+ 'bond3490', c+ 'sulfide-2081', c+ 'd95_9',
         c+ 'bond9053', c+ 'bond6346'}

    model.predict(pos=p, neg=n)
    model.show_best_predictions(top_n=10)
    """

if __name__ == '__main__':
    kb = KnowledgeBase(path='carcinogenesis.owl')
    model = CELOE(knowledge_base=kb, max_runtime=1)
    c = 'http://dl-learner.org/carcinogenesis#'
    p = {c + 'd28', c + 'd79', c + 'd27'}
    n = {c + 'bond961', c + 'non_ar_6c_ring-557', c + 'bond7937', c + 'd4_14', c + 'bond3490', c + 'sulfide-2081',
         c + 'd95_9',
         c + 'bond9053', c + 'bond6346'}
    model.fit(pos=p, neg=n)
    model.save_best_hypothesis(n=3)
    # Get Top n hypotheses
    hypotheses = model.best_hypotheses(n=3)
    # Use hypotheses as binary function to label individuals.
    predictions = model.predict(individuals=list(p) + list(n), hypotheses=hypotheses)
    print(predictions)

