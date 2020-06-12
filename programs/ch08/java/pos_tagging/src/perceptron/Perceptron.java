package perceptron;

import format.Pair;
import format.Word;
import util.Counts;

import java.util.*;

/**
 * @author pierre
 */
public class Perceptron {

    public Map<String, Integer> posFreqs;
    Counts cnt;
    Map<String, Integer> wordFreqs;
    Map<Pair, Integer> posBigramFreqs;
    Map<String, Map<String, Integer>> wordPOSFreqs;
    Map<Pair, Double> posBigramWeights;
    Map<String, Map<String, Double>> wordPOSWeights;
    Map<Pair, Double> posBigramWeightsAverage;
    Map<String, Map<String, Double>> wordPOSWeightsAverage;
    int tokenCount;
    int sentenceCount;
    boolean trigram = true;

    public Perceptron(Counts cnt) {
        this.cnt = cnt;
        this.posFreqs = cnt.getPOSFreqs();
        this.wordFreqs = cnt.getWordFreqs();
        this.posBigramFreqs = cnt.getPOSBigramFreqs();
        this.wordPOSFreqs = cnt.getWordPOSFreqs();
        this.tokenCount = cnt.getTokenCount();
        this.sentenceCount = cnt.getSentenceCount();
        this.posBigramWeights = new TreeMap<>();
        this.wordPOSWeights = new TreeMap<>();
        this.posBigramWeightsAverage = new TreeMap<>();
        this.wordPOSWeightsAverage = new TreeMap<>();
    }

    public void initPOSBigramWeights() {
        /*List<Pair> posBigram = new ArrayList<>(posBigramFreqs.keySet());
         for (Pair bigram : posBigram) {
         posBigramWeights.put(bigram, 0.0);
         }*/
        Set<String> posList = posFreqs.keySet();
        for (String pos1 : posList) {
            for (String pos2 : posList) {
                posBigramWeights.put(new Pair(pos1, pos2), 0.0);
                posBigramWeightsAverage.put(new Pair(pos1, pos2), 0.0);
            }
        }
    }
    /*
     public void subPOSBigramWeights(Map<Pair, Integer> pposBigrams) {
     List<Pair> posBigramL = new ArrayList<>(pposBigrams.keySet());
     for (Pair bigram : posBigramL) {
     Double val = posBigramWeights.get(bigram);
     Integer newVal = pposBigrams.get(bigram);
     if (val == null) {
     posBigramWeights.put(bigram, -new Double(newVal));
     } else {
     posBigramWeights.put(bigram, val - new Double(newVal));
     }
     }
     }
     */

    public void initWordPOSBigrams() {
        List<String> wordList = new ArrayList<>(wordPOSFreqs.keySet());
        for (String word : wordList) {
            Map<String, Integer> posMap = wordPOSFreqs.get(word);
            Map<String, Double> posWeights = new HashMap<>();
            Map<String, Double> posWeightsAverage = new HashMap<>();
            List<String> posList = new ArrayList<>(posMap.keySet());
            for (String pos : posList) {
                posWeights.put(pos, 0.0);
                posWeightsAverage.put(pos, 0.0);
            }
            wordPOSWeights.put(word, posWeights);
            wordPOSWeightsAverage.put(word, posWeightsAverage);
        }
    }

    Map<Pair, Double> getPOSBigramWeights() {
        return posBigramWeights;
    }

    Map<Pair, Double> getPOSBigramWeightsAverage() {
        return posBigramWeightsAverage;
    }

    Map<String, Map<String, Double>> getWordPOSWeights() {
        return wordPOSWeights;
    }

    Map<String, Map<String, Double>> getWordPOSWeightsAverage() {
        return wordPOSWeightsAverage;
    }

    public void updateBigramWeights(List<Word> sentence, long iter) {
        for (int i = 1; i < sentence.size(); i++) {
            Pair posBigram = new Pair(sentence.get(i - 1).getPos(), sentence.get(i).getPos());
            Pair pposBigram = new Pair(sentence.get(i - 1).getPpos(), sentence.get(i).getPpos());
            Double weight = posBigramWeights.get(posBigram);
            Double weightAve = posBigramWeightsAverage.get(posBigram);
            posBigramWeights.put(posBigram, weight + 1.0);
            posBigramWeightsAverage.put(posBigram, weightAve + iter);
            weight = posBigramWeights.get(pposBigram);
            weightAve = posBigramWeightsAverage.get(pposBigram);
            posBigramWeights.put(pposBigram, weight - 1.0);
            posBigramWeightsAverage.put(pposBigram, weightAve - iter);
        }
/*        Set<Pair> bigrams = posBigramWeights.keySet();
        for (Pair bigram : bigrams) {
            Double val1 = posBigramWeights.get(bigram);
            Double val2 = posBigramWeightsAverage.get(bigram);
            posBigramWeightsAverage.put(bigram, val1 + val2);
        }*/
    }

    public void computeBigramWeightsAve(long iter) {
        Set<Pair> bigrams = posBigramWeights.keySet();
        for (Pair bigram : bigrams) {
            Double val1 = posBigramWeights.get(bigram);
            Double val2 = posBigramWeightsAverage.get(bigram);
            posBigramWeightsAverage.put(bigram, val1 - val2 / (double) iter);
        }
    }

    public int updateWordPOSWeights(List<Word> sentence, long iter) {
        int count = 0;
        for (int i = 1; i < sentence.size() - 1; i++) {
            String form = sentence.get(i).getForm();
            Map<String, Double> weightPOS = wordPOSWeights.get(form);
            Map<String, Double> weightPOSAve = wordPOSWeightsAverage.get(form);
            if (!sentence.get(i).getPos().equals(sentence.get(i).getPpos())) {
                Double weight = weightPOS.get(sentence.get(i).getPos());
                Double weightAve = weightPOSAve.get(sentence.get(i).getPos());
                weightPOS.put(sentence.get(i).getPos(), weight + 1.0);
                weightPOSAve.put(sentence.get(i).getPos(), weightAve + iter);
                weight = weightPOS.get(sentence.get(i).getPpos());
                weightAve = weightPOSAve.get(sentence.get(i).getPpos());
                weightPOS.put(sentence.get(i).getPpos(), weight - 1.0);
                weightPOSAve.put(sentence.get(i).getPpos(), weightAve - iter);
                count++;
            }
        }
/*        Set<String> forms = wordPOSWeights.keySet();
        for (String form : forms) {
            Map<String, Double> weightPOS = wordPOSWeights.get(form);
            Map<String, Double> weightPOSAve = wordPOSWeightsAverage.get(form);
            Set<String> POSS = weightPOS.keySet();
            for (String POS : POSS) {
                Double val1 = weightPOS.get(POS);
                Double val2 = weightPOSAve.get(POS);
                weightPOSAve.put(POS, val1 + val2);
            }
        }*/
        return count;
    }

    public void computeWordPOSWeightsAve(long iter) {
        Set<String> forms = wordPOSWeights.keySet();
        for (String form : forms) {
            Map<String, Double> weightPOS = wordPOSWeights.get(form);
            Map<String, Double> weightPOSAve = wordPOSWeightsAverage.get(form);
            Set<String> POSS = weightPOS.keySet();
            for (String POS : POSS) {
                Double val1 = weightPOS.get(POS);
                Double val2 = weightPOSAve.get(POS);
                weightPOSAve.put(POS, val1 - val2 / (double) iter);
            }
        }
    }

}
