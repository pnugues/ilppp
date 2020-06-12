package pos_tagging;

import format.CONLLCorpus;
import format.Constants;
import format.Pair;
import format.Word;
import util.ConfusionMatrix;
import util.Counts;
import util.Term;

import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * @author pierre
 */
public class BestFirst implements POSTagger {

    public Map<String, Integer> posFreqs;
    Counts cnt;
    Map<String, Integer> wordFreqs;
    Map<Pair, Integer> posBigramFreqs;
    Map<String, Map<String, Integer>> wordPOSFreqs;
    Map<String, Integer> unkPOSFreqs;
    int tokenCount;
    int sentenceCount;
    boolean trigram = true;

    public BestFirst(Counts cnt) {
        this.cnt = cnt;
        this.posFreqs = cnt.getPOSFreqs();
        this.wordFreqs = cnt.getWordFreqs();
        this.posBigramFreqs = cnt.getPOSBigramFreqs();
        this.wordPOSFreqs = cnt.getWordPOSFreqs();
        this.unkPOSFreqs = cnt.getUnkPOSFreqs();
        this.tokenCount = cnt.getTokenCount();
        this.sentenceCount = cnt.getSentenceCount();
    }

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws IOException {
        File trainingSet = new File(Constants.TRAINING_SET);
        CONLLCorpus trainingCorpus = new CONLLCorpus();
        List<List<Word>> sentenceList;
        sentenceList = trainingCorpus.loadFile(trainingSet);

        Counts cnt = new Counts(sentenceList);
        cnt.computeFreqs();
        cnt.printStats();

        File devSet = new File(Constants.DEV_SET);
        CONLLCorpus devCorpus = new CONLLCorpus();
        List<List<Word>> devSentenceList;
        devSentenceList = devCorpus.loadFile(devSet);
        Map<String, Integer> cntPOSUnk = cnt.countUnkPOSFreqs(devSentenceList);

        BestFirst nbest = new BestFirst(cnt);

        File testSet = new File(Constants.TEST_SET);
        CONLLCorpus testCorpus = new CONLLCorpus();
        List<List<Word>> sentenceTestList;
        sentenceTestList = testCorpus.loadFile(testSet);

        int i = 0;
        long start = System.currentTimeMillis();
        for (List<Word> sent : sentenceTestList) {
            //double prob2 = nbest.tag(sent);
            nbest.tag(sent);
            i++;
            if ((i % 100) == 0) {
                System.out.print("*");
                System.out.flush();
            }
        }
        long finish = System.currentTimeMillis();
        System.out.println("\nTagging time = " + (finish - start) + " milliseconds");

        ConfusionMatrix cmTest = new ConfusionMatrix(sentenceTestList);
        cmTest.computeMatrix();
        cmTest.print();
        System.out.println("Accuracy: " + cmTest.computeAccuracy());
    }

    @Override
    public double tag(List<Word> sentence) {
        double logprob = Math.log10(1.0);
        String prevPrevPOS = "<s>";
        String prevPOS = "<s>";
        Term term = new Term(cnt);
        for (int i = 1; i < sentence.size(); i++) {
            Word word = sentence.get(i);
            Map<String, Integer> posFreqsForWord = wordPOSFreqs.get(word.getForm());
            String CurPOS = null;
            Set<String> posTags = null;
            if (posFreqsForWord == null) {
                //CurPOS = "NN";
                // New version: all the POS are possible:
                //posTags = posFreqs.keySet();
                // Only observed unknown POS are possible
                posTags = unkPOSFreqs.keySet();
            } else {
                posTags = posFreqsForWord.keySet();
            }
            double probTermMax = 0.0, probTerm;
            Pair prevBigram = new Pair(prevPrevPOS, prevPOS);
            for (String POS : posTags) {
                if (trigram) {
                    probTerm = term.compute(word.getForm(), prevBigram, POS);
                } else {
                    probTerm = term.compute(word.getForm(), prevPOS, POS);
                }
                if (probTermMax < probTerm) {
                    probTermMax = probTerm;
                    CurPOS = POS;
                }
                //System.out.println("\t" + POS);
                //System.out.println(freq + "\t" + wordCount.get(word.getForm()));
            }
            logprob += Math.log10(probTermMax);
            word.setPpos(CurPOS);
            prevPrevPOS = prevPOS;
            prevPOS = CurPOS;
        }
        return logprob;
    }
}
