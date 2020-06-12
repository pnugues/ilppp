package pos_tagging;

import format.CONLLCorpus;
import format.Constants;
import format.Pair;
import format.Word;
import util.ConfusionMatrix;
import util.Counts;
import util.POSPath;
import util.Term;

import java.io.File;
import java.io.IOException;
import java.util.*;

/**
 * @author pierre
 */
public class Viterbi implements POSTagger {

    public Map<String, Integer> posFreqs;
    Counts cnt;
    Map<String, Integer> wordFreqs;
    Map<Pair, Integer> posBigramFreqs;
    Map<String, Map<String, Integer>> wordPOSFreqs;
    Map<String, Integer> unkPOSFreqs;
    int tokenCount;
    int sentenceCount;
    boolean trigram = true;

    public Viterbi(Counts cnt) {
        this.cnt = cnt;
        this.posFreqs = cnt.getPOSFreqs();
        this.wordFreqs = cnt.getWordFreqs();
        this.posBigramFreqs = cnt.getPOSBigramFreqs();
        this.wordPOSFreqs = cnt.getWordPOSFreqs();
        this.unkPOSFreqs = cnt.getUnkPOSFreqs();
        this.tokenCount = cnt.getTokenCount();
        this.sentenceCount = cnt.getSentenceCount();
    }

    public static void main(String[] args) throws IOException {
        long start = System.currentTimeMillis();
        File trainingSet = new File(Constants.TRAINING_SET);
        CONLLCorpus trainingCorpus = new CONLLCorpus();
        List<List<Word>> sentenceList;
        sentenceList = trainingCorpus.loadFile(trainingSet);
        long finish = System.currentTimeMillis();
        System.out.println("Loading time = " + (finish - start) + " milliseconds");

        start = System.currentTimeMillis();
        Counts cnt = new Counts(sentenceList);
        cnt.computeFreqs();
        finish = System.currentTimeMillis();
        System.out.println("Counting time = " + (finish - start) + " milliseconds");

        cnt.printStats();
        File devSet = new File(Constants.DEV_SET);
        CONLLCorpus devCorpus = new CONLLCorpus();
        List<List<Word>> devSentenceList;
        devSentenceList = devCorpus.loadFile(devSet);
        Map<String, Integer> cntPOSUnk = cnt.countUnkPOSFreqs(devSentenceList);

        Viterbi viterbi = new Viterbi(cnt);

        Tester post = new Tester();
        List<Word> sentence = post.makeSentence("That round table might collapse");
        viterbi.tag(sentence);

        File testSet = new File(Constants.TEST_SET);
        CONLLCorpus testCorpus = new CONLLCorpus();
        List<List<Word>> sentenceTestList;
        sentenceTestList = testCorpus.loadFile(testSet);

        int i = 0;
        start = System.currentTimeMillis();
        for (List<Word> sent : sentenceTestList) {
            //double prob2 = nbest.tag(sent);
            viterbi.tag(sent);
            i++;
            if ((i % 100) == 0) {
                System.out.print("*");
                System.out.flush();
            }
        }
        finish = System.currentTimeMillis();
        System.out.println("\nTagging time = " + (finish - start) + " milliseconds");

        ConfusionMatrix cmTest = new ConfusionMatrix(sentenceTestList);
        cmTest.computeMatrix();
        cmTest.print();
        System.out.println("Accuracy: " + cmTest.computeAccuracy());
        testCorpus.saveFile(new File("rienx"), sentenceTestList);
    }

    @Override
    public double tag(List<Word> sentence) {
        int rows = posFreqs.size();
        int cols = sentence.size();
        List<POSPath>[][] table = createTable(sentence);
        double max = Double.NEGATIVE_INFINITY;
        int inxMax = 0;
        for (int i = 0; i < rows; i++) {
            Collections.sort(table[i][cols - 1]);
            Collections.reverse(table[i][cols - 1]);
            if (max < (table[i][cols - 1]).get(0).getProb()) {
                max = (table[i][cols - 1]).get(0).getProb();
                inxMax = i;
            }
            //System.out.println(table[i][cols]);
        }
        //printMatrix(sentence, table);
        List<String> posPath = table[inxMax][cols - 1].get(0).getPath();
        //System.out.println(posPath);
        for (int i = 0; i < sentence.size(); i++) {
            sentence.get(i).setPpos(posPath.get(i));
        }
        return table[inxMax][cols - 1].get(0).getProb();
    }

    public List<POSPath>[][] createTable(List<Word> sentence) {
        int rows = posFreqs.size();
        int cols = sentence.size();
        List<POSPath> cell;
        List<POSPath>[][] table = new List[rows][cols];
        /*
         for (int i = 0; i < cols + 1; i++) {
         System.out.print(table[0][i] + "\t");
         }
         System.out.println();
         */
        Set<String> keyset = posFreqs.keySet();
        List<String> posList = new ArrayList<>(keyset);
        Collections.sort(posList);
        /*
         for (int i = 0; i < rows + 1; i++) {
         System.out.print(table[i][0] + "\t");
         }
         System.out.println();
         */
        // Init col 1
        // We fill the first column: P(<s>) = 1 and P(Other) = 0
        for (int i = 0; i < rows; i++) {
            cell = new ArrayList<>();
            POSPath posPath;
            if (posList.get(i).equals("<s>")) {
                posPath = new POSPath(posList.get(i), 1.0);
                cell.add(posPath);
            } else {
                posPath = new POSPath(posList.get(i), 0.0);
                cell.add(posPath);
            }
            table[i][0] = cell;
        }

        for (int j = 1; j < cols; j++) { // The words after <s>
            String form = sentence.get(j).getForm();
            Map<String, Integer> posTags = wordPOSFreqs.get(form);
            List<String> wordPOSList;
            if (posTags == null) {
                // Unknown words, they are nouns: wordPOSList.add("NN");
                // Unknown words: They can have any POS.
                // wordPOSList = new ArrayList<>(posFreqs.keySet());
                // Unknown words: Observed unknown words in the dev set
                wordPOSList = new ArrayList<>(unkPOSFreqs.keySet());
            } else {
                wordPOSList = new ArrayList<>(posTags.keySet());
            }
            for (int i = 0; i < rows; i++) { // For each word, we fill the current column
                String curPOS = posList.get(i);
                table[i][j] = new ArrayList<>();
                if (wordPOSList.contains(curPOS)) {
                    if (trigram) {
                        fillCellTrigram(table, form, curPOS, i, j);
                    } else {
                        fillCellBigram(table, form, curPOS, i, j);
                    }
                } else {
                    //table[i][j] = 0.0;
                    table[i][j] = new ArrayList<>();
                    POSPath posPath = new POSPath(null, 0.0);
                    table[i][j].add(posPath);
                }
            }
        }
        return table;
    }

    public void fillCellBigram(List<POSPath>[][] table, String form, String curPOS, int i, int j) {
        int rows = posFreqs.size();
        Term term = new Term(cnt);
        for (int k = 0; k < rows; k++) { // For each current word, we scan the previous column (col - 1) to get the bigrams and the probability of the first part of the path.
            List<POSPath> posLastColL = table[k][j - 1];
            POSPath posLastCol = posLastColL.get(0); // Normally one list. This could be expanded to have an NBest search.
            if (posLastCol.getProb() != Double.NEGATIVE_INFINITY) {
                //System.out.println("\tLast col: " + posLastCol);
                POSPath posPath = new POSPath(posLastCol);
                String prevPOS = posPath.getLastPOS();
                double probTerm = term.compute(form, prevPOS, curPOS);
                posPath.addPOS(curPOS);
                posPath.probMult(probTerm);
                table[i][j].add(posPath);
                //System.out.println("\tLast col: " + posPath);
                //System.out.println("\t\t" + ((List<POSPath>) table[i][j]));
            }
        }
        // We take the max of each cell
        Collections.sort(table[i][j]);
        Collections.reverse(table[i][j]);
        //System.err.println("Cell: " + table[i][j]);
        table[i][j] = table[i][j].subList(0, 1);
        //System.err.println("\tMax: " + table[i][j]);
    }

    public void fillCellTrigram(List<POSPath>[][] table, String form, String curPOS, int i, int j) {
        int rows = posFreqs.size();
        Term term = new Term(cnt);
        for (int k = 0; k < rows; k++) { // For each current word, we scan the previous column (col - 1) to get the bigrams and the probability of the first part of the path.
            List<POSPath> posLastColL = table[k][j - 1];
            POSPath posLastCol = posLastColL.get(0); // Normally one list for bigrams and more for trigrams. This could be expanded to have an NBest search.
            if (posLastCol.getProb() != Double.NEGATIVE_INFINITY) {
                //System.out.println("\tLast col: " + posLastCol);
                List<POSPath> posPathTemp = new ArrayList<>();
                for (int l = 0; l < posLastColL.size(); l++) {
                    posPathTemp.add(new POSPath(posLastColL.get(l)));
                    Pair prevBigram = posPathTemp.get(l).getLastPOSBigram();
                    double probTerm = term.compute(form, prevBigram, curPOS);
                    posPathTemp.get(l).addPOS(curPOS);
                    posPathTemp.get(l).probMult(probTerm);
                    // We take the max of each cell
                    Collections.sort(posPathTemp);
                    Collections.reverse(posPathTemp);
                }
                table[i][j].add(posPathTemp.get(0));
                //System.out.println("\tLast col: " + posPath);
                //System.out.println("\t\t" + ((List<POSPath>) table[i][j]));
            }
        }
        //System.out.println("\t" + (List<POSPath>) table[i][j]);
        //System.out.println((List<POSPath>) table[i][j]);
    }

    public void printMatrix(List<Word> sentence, List<POSPath>[][] table) {
        int rows = posFreqs.size();
        int cols = sentence.size();
        for (int i = 0; i < cols; i++) {
            System.out.print(sentence.get(i).getForm() + "\t");
        }
        System.out.println();
        for (int i = 0; i < rows; i++) {
            for (int k = 0; k < cols; k++) {
                System.out.print(table[i][k] + "\t");
            }
            System.out.println();
        }
    }
}
