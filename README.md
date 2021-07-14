# KnowledgeGraph-CarcinogenicityPrediction
Predict the carcinogenicity of cells by the given carciogenesis.owl data and the provided learning problems for algorithm development
# Usage and Installation 
## Prerequisite: 
Python 3.7.1<br/>
**Libraries:** rdflib, ontolearn.
## Installation: 
**rdflib installation:**<br/>
```pip install rdflib``` 

**ontolearn installation:**<br/>
Kindly refer to the [README.md](https://github.com/dice-group/Ontolearn#readme) file of [this git repository](https://github.com/dice-group/Ontolearn) for the installation of Ontolearn. <br/>
*Note:* Please do not use "pip install ontolearn" command to install ontolearn package. Follow the steps to install the package from the github source.

## Usage:
```python test.py```  
generates “output_classification_result<*number*>.ttl” as output. 


# Interfaces and Scope
## Context:

Carcinogenicity prediction for unknown individuals.

- 25 learning problems are provided in the “kg-mini-project-train_v2.ttl” file. Each learning problem consists of carcinogenesis bond names attached with property “excludesResource” or “includesResource”. Carcinogenesis bonds with “excludesResource” are considered to be negative examples and bonds with “includesResource” to be positive.
- An OWL knowledge base is provided in the carcinogenesis.owl file. The chemical structure of each compound and short-term assay’s results is made available as ontology in this carcinogenesis.owl file which contains 142 classes, 19 properties, 22373 instances, and 74567 triples.
- The task is to create and train a model with the provided data mentioned above to predict carcinogenicity by classifying unknown individuals provided in the “kg-mini-project-grading.ttl” file.

## Design decisions:

-	Rdflib is used to parse the “kg-mini-project-train_v2.ttl” file to get the data from the turtle file to divide features and labels of the provided training and validation datasets into their respective variables in the TurtleParser.py module. The name of the carcinogenesis bonds along with the labels and learning problem names are fetched from the file.
-	CELOE model from ontolearn is used for training to learn concepts using the above-mentioned parsed data and the given knowledge base. Once the training is done the prediction is provided on the validation data by the learner.py module using the trained model.
-	rdflib is again used to convert the predicted output to one RDF file in turtle format in output.py module.
- evaluate() funtion in	main.py module is used to evaluate the precision and recall of our predicted output provided by the CELOE model after training.
- main.py is responsible for identifying the unknown individuals from the “kg-mini-project-grading.ttl” file and providing predictions for them.
