from rdflib import Graph
from TurtleParser import TurtleParser
from sklearn.model_selection import train_test_split

if __name__ == "__main__":
    test = TurtleParser()
    test.parse_rdf()
    bla = test.get_subjects().pop()
    print(bla)
    data_pos = test.get_labels(bla, 1)
    d = list(data_pos)
    train, val = train_test_split(d, test_size=0.3)
    print (train)
    print (val)