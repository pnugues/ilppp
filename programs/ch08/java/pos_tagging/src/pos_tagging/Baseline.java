package pos_tagging;

import format.CONLLCorpus;
import format.Constants;
import format.Word;
import util.ConfusionMatrix;
import util.Counts;

import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * @author pierre
 */
public class Baseline implements POSTagger {

    Map<String, Integer> wordFreqs;
    Map<String, Map<String, Integer>> wordPOSFreqs;
    int tokenCount;
    int sentenceCount;

    public Baseline(Counts cnt) {
        this.wordFreqs = cnt.getWordFreqs();
        this.wordPOSFreqs = cnt.getWordPOSFreqs();
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

        Baseline nbest = new Baseline(cnt);

        Tester post = new Tester();
        List<Word> sentence = post.makeSentence("That round table might collapse");
        System.out.println(nbest.tag(sentence));
        /*
         for (List<Word> sent : sentenceList) {
         //System.out.println(sent.size());
         nbest.tag(sent);
         }
         */
//        nbest.computeTerm("That", "<s>", "DT");
        File testSet = new File(Constants.DEV_SET);
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

    // Applies arg max ∏ P(t_i | w_i)
    // Equivalent to arg max ∏ P(w_i | t_i) ∏ P(t_i)
    @Override
    public double tag(List<Word> sentence) {
        double logprob = Math.log10(1.0);
        for (int i = 1; i < sentence.size(); i++) {
            Word word = sentence.get(i);
            Map<String, Integer> posCounts = wordPOSFreqs.get(word.getForm());
            String POS = null;
            if (posCounts == null) {
                POS = "NNP";
            } else {
                Set<String> posTags = posCounts.keySet();
                int freq = 0;
                for (String tag : posTags) {
                    if (freq < posCounts.get(tag)) {
                        freq = posCounts.get(tag);
                        POS = tag;
                    }
                }
                //System.out.println(freq + "\t" + wordCount.get(word.getForm()));
                logprob += Math.log10((double) freq / (double) wordFreqs.get(word.getForm()));
            }
            word.setPpos(POS);
        }
        return logprob;
    }
}
