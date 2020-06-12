package util;

import format.*;

import java.io.File;
import java.io.IOException;
import java.util.*;

/**
 * @author pierre
 */
public class Counts {

    Map<String, Integer> posFreqs;
    Map<String, Integer> wordFreqs;
    Map<Pair, Integer> posBigramFreqs;
    Map<Pair, Integer> pposBigramFreqs;
    Map<Triple, Integer> posTrigramFreqs;
    Map<String, Map<String, Integer>> wordPOSFreqs;
    Map<String, Map<String, Integer>> wordPPOSFreqs;
    Map<String, Integer> unkPOSFreqs;
    List<List<Word>> sentenceList;
    int tokenCount = 0;
    int unkWordCnt = 0;
    int sentenceCount;

    public Counts(List<List<Word>> sentenceList) {
        this.sentenceList = sentenceList;
        sentenceCount = sentenceList.size();
    }

    /**
     * @param args the command line arguments
     * @throws java.io.IOException
     */
    public static void main(String[] args) throws IOException {
        File trainingSet = new File(Constants.TRAINING_SET);
        CONLLCorpus trainingCorpus = new CONLLCorpus();
        List<List<Word>> sentenceList;
        sentenceList = trainingCorpus.loadFile(trainingSet);
        ConfusionMatrix cm = new ConfusionMatrix(sentenceList);
        cm.computeMatrix();
        cm.print();
        System.out.println("Accuracy: " + cm.computeAccuracy());
        Counts cnt = new Counts(sentenceList);
        cnt.computeFreqsTime();
        cnt.printStats();

        File devSet = new File(Constants.DEV_SET);
        CONLLCorpus devCorpus = new CONLLCorpus();
        List<List<Word>> devSentenceList;
        devSentenceList = devCorpus.loadFile(devSet);
        Map<String, Integer> cntPOSUnk = cnt.countUnkPOSFreqs(devSentenceList);
        System.out.println("cntPOSUnk: " + cntPOSUnk);
        cnt.printDebug();
    }

    private Map<String, Integer> countWords() {
        wordFreqs = new TreeMap<>();
        tokenCount = 0;
        for (List<Word> sentence : sentenceList) {
            for (int i = 0; i < sentence.size(); i++) { // Skipping the ROOT index
                Word word = sentence.get(i);
                tokenCount++;
                if (wordFreqs.get(word.getForm()) != null) {
                    int cnt = wordFreqs.get(word.getForm());
                    cnt++;
                    wordFreqs.put(word.getForm(), cnt);
                } else {
                    wordFreqs.put(word.getForm(), 1);
                }
            }
        }
        return wordFreqs;
    }

    private void posSet() {
        SortedSet posSet = new TreeSet(), pposSet = new TreeSet();
        for (List<Word> sentence : sentenceList) {
            for (int i = 0; i < sentence.size(); i++) { // Skipping the ROOT index
                Word word = sentence.get(i);
                posSet.add(word.getPos());
                pposSet.add(word.getPpos());
            }
        }
        System.out.println(posSet.toString());
        System.out.println(pposSet.toString());
    }

    private Map<String, Integer> countPOS() {
        posFreqs = new TreeMap<>();
        tokenCount = 0;
        for (List<Word> sentence : sentenceList) {
            for (int i = 0; i < sentence.size(); i++) {
                Word word = sentence.get(i);
                tokenCount++;
                if (posFreqs.get(word.getPos()) != null) {
                    int cnt = posFreqs.get(word.getPos());
                    cnt++;
                    posFreqs.put(word.getPos(), cnt);
                } else {
                    posFreqs.put(word.getPos(), 1);
                }
            }
        }
        return posFreqs;
    }

    private Map<Pair, Integer> countPOSBigrams() {
        posBigramFreqs = new TreeMap<>();
        pposBigramFreqs = new TreeMap<>();
        for (List<Word> sentence : sentenceList) {
            for (int i = 1; i < sentence.size(); i++) {
                Word prevWord = sentence.get(i - 1);
                Word word = sentence.get(i);
                Pair posBigram = new Pair(prevWord.getPos(), word.getPos());
                Pair pposBigram = new Pair(prevWord.getPpos(), word.getPpos());
                if (posBigramFreqs.get(posBigram) != null) {
                    int cnt = posBigramFreqs.get(posBigram);
                    cnt++;
                    posBigramFreqs.put(posBigram, cnt);
                } else {
                    posBigramFreqs.put(posBigram, 1);
                }
                if (pposBigramFreqs.get(pposBigram) != null) {
                    int cnt = pposBigramFreqs.get(pposBigram);
                    cnt++;
                    pposBigramFreqs.put(pposBigram, cnt);
                } else {
                    pposBigramFreqs.put(pposBigram, 1);
                }
            }
        }
        return posBigramFreqs;
    }

    private Map<Triple, Integer> countPOSTrigrams() {
        posTrigramFreqs = new TreeMap<>();
        for (List<Word> sentence : sentenceList) {
            for (int i = 1; i < sentence.size() - 1; i++) {
                Word prevWord = sentence.get(i - 1);
                Word word = sentence.get(i);
                Word nextWord = sentence.get(i + 1);
                Pair posBigram = new Pair(prevWord.getPos(), word.getPos());
                Triple posTrigram = new Triple(posBigram, nextWord.getPos());
                if (posBigramFreqs.get(posBigram) == null) { // This should not occur
                    System.err.println("Error in trigram count");
                    return null;
                }
                if (posTrigramFreqs.get(posTrigram) == null) {
                    posTrigramFreqs.put(posTrigram, 1);
                } else {
                    int cnt = posTrigramFreqs.get(posTrigram);
                    cnt++;
                    posTrigramFreqs.put(posTrigram, cnt);
                }
            }
        }
        return posTrigramFreqs;
    }

    private Map<String, Map<String, Integer>> countWordPOS() {
        wordPOSFreqs = new TreeMap<>();
        wordPPOSFreqs = new TreeMap<>();
        for (List<Word> sentence : sentenceList) {
            for (int i = 0; i < sentence.size(); i++) { // Skipping the ROOT index
                Word word = sentence.get(i);
                if (wordPOSFreqs.get(word.getForm()) != null) {
                    Map<String, Integer> pair = wordPOSFreqs.get(word.getForm());
                    if (pair.get(word.getPos()) != null) {
                        int cnt = pair.get(word.getPos());
                        cnt++;
                        pair.put(word.getPos(), cnt);
                        wordPOSFreqs.put(word.getForm(), pair);
                    } else {
                        pair.put(word.getPos(), 1);
                        wordPOSFreqs.put(word.getForm(), pair);
                    }
                } else {
                    Map<String, Integer> pair = new TreeMap<>();
                    pair.put(word.getPos(), 1);
                    wordPOSFreqs.put(word.getForm(), pair);
                }
                if (wordPPOSFreqs.get(word.getForm()) != null) {
                    Map<String, Integer> pair = wordPPOSFreqs.get(word.getForm());
                    if (pair.get(word.getPpos()) != null) {
                        int cnt = pair.get(word.getPpos());
                        cnt++;
                        pair.put(word.getPpos(), cnt);
                        wordPPOSFreqs.put(word.getForm(), pair);
                    } else {
                        pair.put(word.getPpos(), 1);
                        wordPPOSFreqs.put(word.getForm(), pair);
                    }
                } else {
                    Map<String, Integer> pair = new TreeMap<>();
                    pair.put(word.getPpos(), 1);
                    wordPPOSFreqs.put(word.getForm(), pair);
                }
            }
        }
        return wordPOSFreqs;
    }

    public Map<String, Integer> countUnkPOSFreqs(List<List<Word>> devSentenceList) {
        unkPOSFreqs = new TreeMap<>();
        unkWordCnt = 0;
        for (List<Word> sentence : devSentenceList) {
            for (int i = 0; i < sentence.size(); i++) {
                Word word = sentence.get(i);
                if (wordPOSFreqs.get(word.getForm()) == null) { //Unknown word
                    unkWordCnt++;
                    Integer contUnk = unkPOSFreqs.get(word.getPos());
                    if (contUnk != null) {
                        contUnk++;
                        unkPOSFreqs.put(word.getPos(), contUnk);
                    } else {
                        unkPOSFreqs.put(word.getPos(), 1);
                    }
                }
            }
        }
        return unkPOSFreqs;
    }

    public void computeFreqs() {
        posFreqs = this.countPOS();
        wordFreqs = this.countWords();
        wordPOSFreqs = this.countWordPOS();
        posBigramFreqs = this.countPOSBigrams();
        posTrigramFreqs = this.countPOSTrigrams();
    }

    public void computeFreqsTime() {
        long start = System.currentTimeMillis();
        posFreqs = this.countPOS();
        long finish1 = System.currentTimeMillis();
        System.out.println("Counting POS (milliseconds): " + (finish1 - start));
        wordFreqs = this.countWords();
        long finish2 = System.currentTimeMillis();
        System.out.println("Counting word freqs (milliseconds): " + (finish2 - finish1));
        wordPOSFreqs = this.countWordPOS();
        long finish3 = System.currentTimeMillis();
        System.out.println("Counting word-POS freqs (milliseconds): " + (finish3 - finish2));
        posBigramFreqs = this.countPOSBigrams();
        long finish4 = System.currentTimeMillis();
        System.out.println("Counting POS bigrams (milliseconds): " + (finish4 - finish3));
        posTrigramFreqs = this.countPOSTrigrams();
        long finish5 = System.currentTimeMillis();
        System.out.println("Counting POS trigrams (milliseconds): " + (finish5 - finish4));
    }

    public void printStats() {
        System.out.println("Token count:\t" + tokenCount + "\tSentence count:\t" + sentenceCount);
        System.out.println("\tUnique tokens:\t" + wordFreqs.size());
        System.out.println("\t" + wordFreqs);

        System.out.println("\tUnique POS:\t" + posFreqs.size());
        System.out.println("\t" + posFreqs);

        System.out.println("\tUnique word/POS pairs:\t" + wordPOSFreqs.size());
        System.out.println("\t" + wordPOSFreqs);

        System.out.println("\tUnique POS bigrams:\t" + posBigramFreqs.size());
        System.out.println("\t" + posBigramFreqs);

        System.out.println("\tUnique POS trigrams:\t" + posTrigramFreqs.size());
        System.out.println("\t" + posTrigramFreqs);
    }

    public void printDebug() {
        System.out.println("That round table might collapse");
        System.out.print("wordPOSFreqs <s>: " + wordPOSFreqs.get("<s>") + "\t");
        System.out.print("wordPOSFreqs That: " + wordPOSFreqs.get("That") + "\t");
        System.out.print("wordPOSFreqs round: " + wordPOSFreqs.get("round") + "\t");
        System.out.print("wordPOSFreqs table: " + wordPOSFreqs.get("table") + "\t");
        System.out.print("wordPOSFreqs might: " + wordPOSFreqs.get("might") + "\t");
        System.out.print("wordPOSFreqs collapse: " + wordPOSFreqs.get("collapse") + "\t");
        System.out.println("wordPOSFreqs sssss: " + wordPOSFreqs.get("sssss"));
        System.out.println("wordPOSFreqs </s>: " + wordPOSFreqs.get("</s>") + "\t");
        System.out.println("Bigram <s> DT: " + posBigramFreqs.get(new Pair("<s>", "DT")));
        System.out.println("Bigram DT JJ: " + posBigramFreqs.get(new Pair("DT", "JJ")));
        System.out.println("Bigram VB </s>: " + posBigramFreqs.get(new Pair("VB", "</s>")));
        System.out.println("Bigram NNP NIL: " + posBigramFreqs.get(new Pair("NNP", "NIL")));
        System.out.println("Trigram <s> DT NN: " + posTrigramFreqs.get(new Triple(new Pair("<s>", "DT"), "NN")));
        Term term = new Term(this);
        System.out.println("Term: " + term.compute("tabl", new Pair("<s>", "DT"), "NN"));
        // tabl is UKN.It can only have a possible POS: NN, NNS, NNP, etc, not DT
    }

    public Map<String, Integer> getPOSFreqs() {
        return posFreqs;
    }

    public Map<String, Integer> getWordFreqs() {
        return wordFreqs;
    }

    public Map<Pair, Integer> getPOSBigramFreqs() {
        return posBigramFreqs;
    }

    public Map<Pair, Integer> getPPOSBigramFreqs() {
        return pposBigramFreqs;
    }

    public Map<Triple, Integer> getPOSTrigramFreqs() {
        return posTrigramFreqs;
    }

    public Map<String, Map<String, Integer>> getWordPOSFreqs() {
        return wordPOSFreqs;
    }

    public Map<String, Map<String, Integer>> getWordPPOSFreqs() {
        return wordPPOSFreqs;
    }

    public Map<String, Integer> getUnkPOSFreqs() {
        return unkPOSFreqs;
    }

    public int getTokenCount() {
        return tokenCount;
    }

    public int getSentenceCount() {
        return sentenceCount;
    }
}
