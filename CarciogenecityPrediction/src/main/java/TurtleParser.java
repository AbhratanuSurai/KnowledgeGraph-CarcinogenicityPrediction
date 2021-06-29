import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.Iterator;


import org.apache.jena.graph.Node;
import org.apache.jena.graph.NodeVisitor;
import org.apache.jena.rdf.model.*;
import org.apache.jena.riot.RDFDataMgr;

import sun.jvm.hotspot.debugger.linux.sparc.LinuxSPARCThreadContext;


/**
 * Fetch the positive and negative examples
 * from the turtle file
 * Negative examples are tagged with Excludes resource
 * and
 * Positive examples are tagged with Include resource
 *
 * @author Abhratanu Surai
 *
 */

public class TurtleParser {
    public static void main(String[] args) {

        /*
         * Creating a model and load the turtle file in the model
         * */
        Model model = RDFDataMgr.loadModel("./src/main/resources/kg-mini-project-train_v2.ttl");


        Statement stmt;
        Set<Resource> subjects = new HashSet<>();
        Set<Property>  predicates = new HashSet<>();
        ArrayList<String>   eachLearningProblemPositiveLabels = new ArrayList<>();
        ArrayList<String>   eachLearningProblemNegativeLabels = new ArrayList<>();
        List<ArrayList<String>> allLearningProblemPositiveLabels = new ArrayList<ArrayList<String>>();
        List<ArrayList<String>> allLearningProblemNegativeLabels = new ArrayList<ArrayList<String>>();
        StmtIterator iter = model.listStatements();


        /* Iterating over all the statements one by one and
        *  getting subjects, predicate and objects separately.
        *  Using set to store the values to remove duplicates.
        *  */
        while (iter.hasNext()) {
            stmt = iter.nextStatement();
            subjects.add(stmt.getSubject());
            predicates.add(stmt.getPredicate());
        }
        //System.out.print(subjects);
        //System.out.println(predicates);

        /* eachLearningProblemPositiveLabels is a list of positive examples
        *  that contains 2 string items;
        *  1) Name of the learning problem
        *  2) The carcinogenesis bond itself.
        *
        *  allLearningProblemPositiveLabels is a list of lists of above type.
        *
        *  Similar lists also exists for negative examples as well
        *  namely eachLearningProblemNegativeLabels and allLearningProblemPositiveLabels.
        * */
        for(Resource r : subjects){
            for(Property p : predicates){
                if(!p.toString().equals("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")){
                    NodeIterator object = model.listObjectsOfProperty(r, p);
                    if(object.hasNext() && p.toString().equals("https://lpbenchgen.org/property/includesResource")) {
                        eachLearningProblemPositiveLabels.add(r.toString());
                        eachLearningProblemPositiveLabels.add(object.next().toString());
                        allLearningProblemPositiveLabels.add(eachLearningProblemPositiveLabels);
                    }
                    else if (object.hasNext() && p.toString().equals("https://lpbenchgen.org/property/excludesResource")){
                        eachLearningProblemNegativeLabels.add(r.toString());
                        eachLearningProblemNegativeLabels.add(object.next().toString());
                        allLearningProblemNegativeLabels.add(eachLearningProblemNegativeLabels);
                    }
                }
            }
        }


        System.out.println("\n ---List of all positive examples--- \n");
        for(ArrayList<String> eachList : allLearningProblemPositiveLabels){
            for(String s : eachList){
                System.out.println(s);
            }
        }
        System.out.println("\n ---List of all Negative examples--- \n");
        for(ArrayList<String> eachList : allLearningProblemNegativeLabels){
            for(String s : eachList){
                System.out.println(s);
            }
        }

    }

}


