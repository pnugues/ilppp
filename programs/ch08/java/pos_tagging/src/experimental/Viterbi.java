package experimental;

import format.CONLLCorpus;
import format.Constants;
import format.Pair;
import format.Word;
import pos_tagging.Tester;
import util.Counts;
import util.POSPath;

import java.io.File;
import java.io.IOException;
import java.util.*;

/**
 * @author pierre Here all the parts of speech have a small probability
 */
public class Viterbi {

    public Map<String, Integer> posFreqs;
    Map<String, Integer> wordFreqs;
    Map<Pair, Integer> posBigramFreqs;
    Map<String, Map<String, Integer>> wordPOSFreqs;
    int tokenCount;
    int sentenceCount;

    public Viterbi(Counts cnt) {
        this.posFreqs = cnt.getPOSFreqs();
        this.wordFreqs = cnt.getWordFreqs();
        this.posBigramFreqs = cnt.getPOSBigramFreqs();
        this.wordPOSFreqs = cnt.getWordPOSFreqs();
        this.tokenCount = cnt.getTokenCount();
        this.sentenceCount = cnt.getSentenceCount();
    }

    public static void main(String[] args) throws IOException {
        File trainingSet = new File(Constants.TRAINING_SET);
        CONLLCorpus trainingCorpus = new CONLLCorpus();
        List<List<Word>> sentenceList;
        sentenceList = trainingCorpus.loadFile(trainingSet);

        Counts cnt = new Counts(sentenceList);
        cnt.computeFreqs();
        cnt.printStats();

        Viterbi viterbi = new Viterbi(cnt);

        Tester post = new Tester();
        List<Word> sentence = post.makeSentence("That round table might collapse");
        viterbi.tag(sentence);
    }

    public double tag(List<Word> sentence) {
        int rows = posFreqs.size();
        int cols = sentence.size();
        Object[][] table = createTable(sentence);
        //printMatrix(table, rows, cols);
        double max = Double.NEGATIVE_INFINITY;
        int inxMax = 0;
        for (int i = 1; i < rows + 1; i++) {
            if (max < ((List<POSPath>) table[i][cols]).get(0).getProb()) {
                max = ((List<POSPath>) table[i][cols]).get(0).getProb();
                inxMax = i;
            }
            //System.out.println(table[i][cols]);
        }
        List<String> posPath = ((List<POSPath>) table[inxMax][cols]).get(0).getPath();
        //System.out.println(posPath);
        for (int i = 0; i < sentence.size(); i++) {
            sentence.get(i).setPpos(posPath.get(i));
        }
        return ((List<POSPath>) table[inxMax][cols]).get(0).getProb();
    }

    public Object[][] createTable(List<Word> sentence) {
        List<POSPath> cell;
        Object[][] table;
        int rows = posFreqs.size();
        int cols = sentence.size();
        table = new Object[rows + 1][cols + 1];
        for (int i = 1; i < cols + 1; i++) {
            table[0][i] = sentence.get(i - 1).getForm();
        }
        /*
         for (int i = 0; i < cols + 1; i++) {
         System.out.print(table[0][i] + "\t");
         }
         System.out.println();
         */
        Set keyset = posFreqs.keySet();
        List posList = new ArrayList(keyset);
        Collections.sort(posList);
        for (int i = 1; i < rows + 1; i++) {
            table[i][0] = posList.get(i - 1);
        }
        /*
         for (int i = 0; i < rows + 1; i++) {
         System.out.print(table[i][0] + "\t");
         }
         System.out.println();
         */
        // Init col 1
        for (int i = 1; i < rows + 1; i++) {
            List<String> path = new ArrayList<>();
            path.add((String) table[i][0]);
            cell = new ArrayList<>();
            POSPath posPath;
            if (table[i][0].equals("<s>")) {
                posPath = new POSPath((String) table[i][0], 1.0);
                cell.add(posPath);
            } else {
                posPath = new POSPath((String) table[i][0], 0.0);
                cell.add(posPath);
            }
            table[i][1] = cell;
        }

        for (int j = 2; j < cols + 1; j++) { // The words (rows)
            String form = sentence.get(j - 1).getForm();
            Map<String, Integer> posTags = wordPOSFreqs.get(form);
            List<String> wordPOSList;
            if (posTags == null) {
                wordPOSList = new ArrayList<>(posFreqs.keySet());
                //wordPOSList = new ArrayList<>();
                //wordPOSList.add("NN");
            } else {
                wordPOSList = new ArrayList<>(posTags.keySet());
            }
            for (int i = 1; i < rows + 1; i++) { // For each word, we fill the current column
                String curPOS = (String) table[i][0];
                table[i][j] = new ArrayList<>();

                for (int k = 1; k < rows + 1; k++) { // For each current word, we scan the previous column (col - 1) to get the bigrams and the probability of the first part of the path.
                    List<POSPath> posLastColL = (List<POSPath>) table[k][j - 1];
                    POSPath posLastCol = posLastColL.get(0); // Normally one list. This could be expanded to have an NBest search.
                    if (posLastCol.getProb() != Double.NEGATIVE_INFINITY) {
                        //System.out.println("\tLast col: " + posLastCol);
                        POSPath posPath = new POSPath(posLastCol);
                        String prevPOS = posLastCol.getLastPOS();
                        posPath.addPOS(curPOS);
                        double term = computeTerm(form, prevPOS, curPOS);
                        posPath.probMult(term);
                        ((List<POSPath>) table[i][j]).add(posPath);
                        //System.out.println("\tLast col: " + posPath);
                        //System.out.println("\t\t" + ((List<POSPath>) table[i][j]));
                    }
                }
                // We take the max of each cell
                Collections.sort(((List<POSPath>) table[i][j]));
                Collections.reverse(((List<POSPath>) table[i][j]));
                //System.out.println("\t" + (List<POSPath>) table[i][j]);
                table[i][j] = ((List<POSPath>) table[i][j]).subList(0, 1);
                //System.out.println((List<POSPath>) table[i][j]);

            }
        }
        return table;
    }

    //P(w_i | t_i) x P(t_i | t_{i - 1})
    public double computeTerm(String word, String prevPos, String pos) {
        // First term
        double firstTerm;
        double pairFreq;
        int tagFreq = posFreqs.get(pos);
        if (wordPOSFreqs.get(word) == null) {
            //pairFreq = 1e-4;
            firstTerm = 5e-7;
        } else if (wordPOSFreqs.get(word).get(pos) == null) {
            //pairFreq = 1e-4;
            firstTerm = 5e-7;
        } else {
            pairFreq = (double) wordPOSFreqs.get(word).get(pos);
            firstTerm = (double) pairFreq / (double) tagFreq;
        }

        // Second term
        double secondTerm;
        int prevTagFreq = posFreqs.get(prevPos);
        Pair tagbigram = new Pair(prevPos, pos);
        int tagBigramFreq;
        if (posBigramFreqs.get(tagbigram) == null) {
            // Backoff
            secondTerm = ((double) tagFreq / (double) tokenCount) * 0.25;
            //secondTerm = (double) 1.0/(double) prevTagFreq;
        } else {
            tagBigramFreq = posBigramFreqs.get(tagbigram);
            secondTerm = (double) tagBigramFreq / (double) prevTagFreq;
        }

        //System.out.println(pairFreq + "\t" + tagFreq + "\t" + prevTagFreq + "\t" + tagBigramFreq);
        return firstTerm * secondTerm;
    }

    public void printMatrix(Object[][] table, int rows, int cols) {
        for (int i = 0; i < rows + 1; i++) {
            for (int k = 0; k < cols + 1; k++) {
                System.out.print(table[i][k] + "\t");
            }
            System.out.println();
        }
    }
}
