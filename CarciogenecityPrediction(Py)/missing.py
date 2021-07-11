from TurtleParser import TurtleParser

class missing_individuals():

    def __init__(self):
        parser = TurtleParser()
        parser.parse_rdf()
        bla = parser.get_subjects().pop()
        self.all_individuals = parser.get_labels(bla, 2)

    def get_unknown_individuals(self, known_individuals):
        unknown_inidividuals = self.all_individuals.copy()
        for i in known_individuals:
            unknown_inidividuals.remove(i)
        return unknown_inidividuals