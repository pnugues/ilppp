package util;

import format.Pair;
import format.Triple;

import java.util.Map;

/**
 * @author pierre
 */
public class Term {

    Map<String, Integer> posFreqs;
    Map<String, Integer> wordFreqs;
    Map<Pair, Integer> posBigramFreqs;
    Map<Triple, Integer> posTrigramFreqs;
    Map<String, Map<String, Integer>> wordPOSFreqs;
    Map<String, Integer> unkPOSFreqs;
    int tokenCount = 0;

    double lambda1Trigram = 0.1, lambda2Trigram = 0.2, lambda3Trigram = 0.7;
    double lambda1Bigram = 0.2, lambda2Bigram = 0.8;

    public Term(Counts cnt) {
        this.posFreqs = cnt.posFreqs;
        this.wordFreqs = cnt.wordFreqs;
        this.posBigramFreqs = cnt.posBigramFreqs;
        this.posTrigramFreqs = cnt.posTrigramFreqs;
        this.wordPOSFreqs = cnt.wordPOSFreqs;
        this.unkPOSFreqs = cnt.unkPOSFreqs;
        this.tokenCount = cnt.getTokenCount();
    }

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
    }

    // Bigrams: P(w_i | t_i) x P(t_i | t_{i - 1})
    public double compute(String word, String prevPos, String pos) {
        // First term
        double firstTerm;
        int tagFreq = posFreqs.get(pos);
        if (unkPOSFreqs.get(pos) != null) { // to have a prob sum equals to 1.
            tagFreq += unkPOSFreqs.get(pos);
        }
        if (wordPOSFreqs.get(word) == null) { // UNK word
            //firstTerm = 0.02; // This value is not meaningful
            firstTerm = (double) unkPOSFreqs.get(pos) / (double) tagFreq;
        } else {
            int pairFreq = wordPOSFreqs.get(word).get(pos);
            firstTerm = (double) pairFreq / (double) tagFreq;
        }

        // Second term
        double secondTerm;
        int prevTagFreq = posFreqs.get(prevPos);
        Pair tagBigram = new Pair(prevPos, pos);
        int tagBigramFreq;
        if (posBigramFreqs.get(tagBigram) == null) {
            // Backoff
            secondTerm = ((double) tagFreq / (double) tokenCount) * lambda1Bigram;
            //secondTerm = (double) 1.0/(double) prevTagFreq;
        } else {
            tagBigramFreq = posBigramFreqs.get(tagBigram);
            secondTerm = ((double) tagFreq / (double) tokenCount) * lambda1Bigram;
            secondTerm += ((double) tagBigramFreq / (double) prevTagFreq) * lambda2Bigram;
        }

        //System.out.println(pairFreq + "\t" + tagFreq + "\t" + prevTagFreq + "\t" + tagBigramFreq);
        return firstTerm * secondTerm;
    }

    //P(w_i | t_i) x P(t_i | t_{i - 2}, t_{i - 1})
    public double compute(String word, Pair prevPos, String pos) {
        // First term
        double firstTerm;
        int tagFreq = posFreqs.get(pos);
        if (unkPOSFreqs.get(pos) != null) { // to have a prob sum equals to 1.
            tagFreq += unkPOSFreqs.get(pos);
        }
        if (wordPOSFreqs.get(word) == null) { // UNK word
            //firstTerm = 0.02; // This value is not meaningful
            firstTerm = (double) unkPOSFreqs.get(pos) / (double) tagFreq;
        } else {
            int pairFreq = wordPOSFreqs.get(word).get(pos);
            firstTerm = (double) pairFreq / (double) tagFreq;
        }

        // Second term
        double secondTerm;
        Pair tagBigram = new Pair(prevPos.getSecond(), pos);
        Triple tagTrigram = new Triple(prevPos, pos);

        if ((posTrigramFreqs.get(tagTrigram) == null) && (posBigramFreqs.get(tagBigram) == null)) {
            // Backoff
            secondTerm = ((double) tagFreq / (double) tokenCount) * lambda1Trigram;
            //secondTerm = (double) 1.0/(double) prevTagFreq;
        } else if ((posTrigramFreqs.get(tagTrigram) == null) && (posBigramFreqs.get(tagBigram) != null)) {
            secondTerm = ((double) tagFreq / (double) tokenCount) * lambda1Trigram;
            secondTerm += ((double) posBigramFreqs.get(tagBigram) / (double) (posFreqs.get(prevPos.getSecond()))) * lambda2Trigram;
        } else {
            secondTerm = ((double) tagFreq / (double) tokenCount) * lambda1Trigram;
            secondTerm += ((double) posBigramFreqs.get(tagBigram) / (double) (posFreqs.get(prevPos.getSecond()))) * lambda2Trigram;
            secondTerm += ((double) posTrigramFreqs.get(tagTrigram) / (double) (posBigramFreqs.get(prevPos))) * lambda3Trigram;
        }
        //System.out.println(pairFreq + "\t" + tagFreq + "\t" + prevTagFreq + "\t" + tagBigramFreq);
        return firstTerm * secondTerm;
    }

    public void setLambdas(double lambda1, double lambda2) {
        this.lambda1Bigram = lambda1;
        this.lambda2Bigram = lambda2;
    }

    public void setLambdas(double lambda1, double lambda2, double lambda3) {
        this.lambda1Trigram = lambda1;
        this.lambda2Trigram = lambda2;
        this.lambda3Trigram = lambda3;
    }

}
