from TurtleParser import TurtleParser

if __name__ == "__main__":
    test = TurtleParser()
    test.parse_rdf()
    print(test.get_labels(rdflib.term.URIRef('https://lpbenchgen.org/resource/lp_4'), 1))