package parser;

import java.util.*;
import java.io.File;
import format.CONLLCorpus;
import format.Constants;
import format.Word;
import guide.Guide;
import guide.Guide4;
import java.io.IOException;
import wekaglue.WekaGlue;

/**
 *
 * @author Pierre Nugues
 */
public class Parser {

    ParserState parserState;
    Guide oracle;

    Parser(ParserState parserState, Guide oracle) {
        this.parserState = parserState;
        this.oracle = oracle;
    }

    public List<Word> parse() {
        String transition;

        while (!parserState.queue.isEmpty()) {
            transition = oracle.predict();
            // Executes the predicted transition. If not possible, then shift
            // COMPLETE THE CODE HERE
        }

        // We empty the stack. When words have no head, we set it to root
        while (parserState.stack.size() > 1) {
            if (parserState.canReduce()) {
                parserState.doReduce();
            } else {
                parserState.doReduceAndSetRoot();
            }
        }
        // In the end, we build the word list
        // All the words must have a head
        // otherwise, the graph would not be connected.
        // Only the root in the stack should have no head
        for (int i = 0; i < parserState.wordList.size(); i++) {
            boolean hasHead = false;
            for (int j = 0; j < parserState.depGraph.size(); j++) {
                if (parserState.wordList.get(i).getId() == parserState.depGraph.get(j).getId()) {
                    parserState.wordList.get(i).setHead(parserState.depGraph.get(j).getHead());
                    hasHead = true;
                    break;
                }
            }
            if (!hasHead) {
                parserState.wordList.get(i).setHead(0);
            }
        }

        boolean printGraph = false;
        if (printGraph) {
            for (int i = 0; i < parserState.wordList.size(); i++) {
                System.out.print(parserState.wordList.get(i).getForm() + " ");
            }
            System.out.println();
            for (int i = 0; i < parserState.transitionList.size(); i++) {
                System.out.print(parserState.transitionList.get(i) + " ");
            }
            System.out.println();
            for (int i = 0; i < parserState.depGraph.size(); i++) {
                System.out.print(parserState.depGraph.get(i).getId() + ", " + parserState.depGraph.get(i).getHead() + " " + parserState.depGraph.get(i).getForm() + " ");
            }
            System.out.println();
        }

        parserState.wordList.remove(0);
        return parserState.wordList;
    }

    public static void main(String[] args) throws IOException {
        File testSet = new File(Constants.TEST_SET);
        File testSetParsed = new File(Constants.TEST_SET_PARSED);
        CONLLCorpus testCorpus = new CONLLCorpus();
        WekaGlue wekaModel = new WekaGlue();

        List<List<Word>> sentenceList;
        List<List<Word>> parsedList = new ArrayList<List<Word>>();

        Parser parser;
        ParserState parserState;
        Guide oracle;
        List<Word> graph;

        if (testSet.exists()) {
            System.out.println("Loading file...");
        } else {
            System.out.println("File does not exist, exiting...");
            return;
        }
        sentenceList = testCorpus.loadFile(testSet);
        wekaModel.create(Constants.ARFF_MODEL, Constants.ARFF_FILE);

        System.out.println("Parsing the sentences...");
        for (int i = 0; i < sentenceList.size(); i++) {
            parserState = new ParserState(sentenceList.get(i));
            oracle = new Guide4(wekaModel, parserState);
            parser = new Parser(parserState, oracle);
            graph = parser.parse();
            parsedList.add(graph);
        }
        testCorpus.saveFile(testSetParsed, parsedList);
    }
}
