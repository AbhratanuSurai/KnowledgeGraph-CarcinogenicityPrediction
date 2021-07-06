from TurtleParser import TurtleParser

if __name__ == "__main__":
    test = TurtleParser()
    test.parse_rdf()
    bla = test.get_subjects().pop()
    print(bla)
    print(test.get_labels(bla, 1))