package pos_tagging;

import format.CONLLCorpus;
import format.Constants;
import format.Word;
import util.ConfusionMatrix;
import util.Counts;
import util.Term;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * @author pierre
 */
public class Tester {

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
        cnt.computeFreqs();
        cnt.printStats();

        File devSet = new File(Constants.DEV_SET);
        CONLLCorpus devCorpus = new CONLLCorpus();
        List<List<Word>> devSentenceList;
        devSentenceList = devCorpus.loadFile(devSet);
        Map<String, Integer> cntPOSUnk = cnt.countUnkPOSFreqs(devSentenceList);

        Tester post = new Tester();
        List<Word> sentence = post.makeSentence("That round table might collapse");

        Baseline baseline = new Baseline(cnt);
        baseline.tag(sentence);
        System.out.println(sentence);

        BestFirst bestfirst = new BestFirst(cnt);
        bestfirst.tag(sentence);
        System.out.println(sentence);

        BeamSearch nbest = new BeamSearch(cnt, 100);
        nbest.tag(sentence);
        System.out.println(sentence);

        Viterbi viterbi = new Viterbi(cnt);
        viterbi.tag(sentence);
        System.out.println(sentence);

        File testSet = new File(Constants.TEST_SET);
        CONLLCorpus testCorpus = new CONLLCorpus();
        List<List<Word>> sentenceTestList;
        sentenceTestList = testCorpus.loadFile(testSet);

        // Michele BANKO and Robert C. MOORE, Part of Speech Tagging in Context, 2004
        // Test set: Baseline: 92.19, trigrammes: 95.87 // Mon meilleur score: 96.01
        // baseline, dev: 0.92582715, test: 0.9289826
        // OLD VERSIONS:
        // N = 1: 0.9359566 (BestFirst direct)
        // N = 1: 0.9359566 (avec BeamSearch, même calculs que BestFirst)
        // N = 1: 0.9362563 // 0.9344282 (BeamSearch avec un facteur de backoff)
        // N = 2: 0.9405119
        // N = 3: 0.9410213
        // N = 4: 0.94129103 // 0.9408415
        // N = 10: 0.94117117 //0.94141096
        // N = 20: 0.9412611
        // N = 30: 0.9412611
        // N = 200: 0.9412611 //0.94290936
        // Viterbi: 0.9412611
        // Avec </s>
        // N = 4: 0.941321
        // Viterbi: 0.94129103
        // NEW VERSIONS:
        // Viterbi, bigrammes: 0.9497123 Mots inconnus peuvent avoir n'importe quelle partie du discours, toutes avec une probabilité de 1
        // Viterbi, bigrammes: 0.9507612 Interpolation linéaire des n-grammes de parties du discours
        // BestFirst, bigrammes: 0.94231, trigrammes: 0.94428796
        // N = 1, bigrammes: 0.94231, trigrammes: 0.94428796
        // N = 2, bigrammes: 0.94851357, trigrammes: 0.9524395
        // N = 3, bigrammes: 0.94995207, trigrammes: 0.9548969
        // N = 4, bigrammes: 0.9504315, trigrammes: 0.954777
        // N = 20, bigrammes: 0.9507612, trigrammes: 0.9558859
        // N = 100, bigrammes: 0.9507612, trigrammes, dev: 0.9560657, test: 0.9578854441642761
        // N = 500, trigrammes, dev: 0.9561256170272827, test: 0.9578680992126465
        // Viterbi, bigrammes, dev: 0.9507612, test: 0.953915
        // Viterbi trigrammes, dev: 0.9561256170272827, test: 0.9578680992126465
        // Avec toutes les valeurs de PDD observées dans le dev:
        // Résultats sur test set:
        // Best First, bigrammes 0.94741315, trigrammes: 0.95022196
        // BeamSearch, N = 1 bigrammes: 0.94741315, trigrammes 0.95022196
        // BeamSearch, N = 2 bigrammes: 0.95452183, trigrammes 0.95809346
        // BeamSearch, N = 4 bigrammes: 0.95623827, trigrammes 0.95987934
        // BeamSearch, N = 20, trigrammes 0.9601914
        // BeamSearch, N = 200, trigrammes 0.96012205
        // Viterbi, bigrammes test: 0.9562903, trigrammes, test: 0.96012205
        // Viterbi pour le test set: Max: 0.9581975340843201	 with Lambda1: 0.1	Lambda2: 0.25	Lambda2: 0.65
        //post.searchBigramWeights(cnt, viterbi1, sentenceTestList);
        post.tag(cnt, viterbi, sentenceTestList);
        ConfusionMatrix cmTest = new ConfusionMatrix(sentenceTestList);
        cmTest.computeMatrix();
        //cmTest.print();
        double accuracy = cmTest.computeAccuracy();
        System.out.println("Accuracy: " + accuracy);
        //testCorpus.saveFile(new File("rienx"), sentenceTestList);
    }

    public List<Word> makeSentence(String words) {
        List<Word> sentence = new ArrayList<>();
        sentence.add(new Word("0", "<s>", "<s>", "<s>", "<s>", "<s>"));
        String[] wordL = words.split(" ");
        Integer inx = 0;
        for (int i = 0; i < wordL.length; i++) {
            inx = i + 1;
            sentence.add(new Word(inx.toString(), wordL[i], null, null, null, null));
        }
        inx++;
        sentence.add(new Word(inx.toString(), "</s>", "</s>", "</s>", "</s>", "</s>"));
        return sentence;
    }

    public List<Word> makeSentence(String words, String defaultPOS) {
        List<Word> sentence = new ArrayList<>();
        sentence.add(new Word("0", "<s>", "<s>", "<s>", "<s>", "<s>"));
        String[] wordL = words.split(" ");
        Integer inx = 0;
        for (int i = 0; i < wordL.length; i++) {
            inx = i + 1;
            sentence.add(new Word(inx.toString(), wordL[i], null, null, null, "NN"));
        }
        inx++;
        sentence.add(new Word(inx.toString(), "</s>", "</s>", "</s>", "</s>", "</s>"));
        return sentence;
    }

    public List<Word> makeTheSentence() {
        List<Word> sentence = new ArrayList<>();
        sentence.add(new Word("0", "<s>", "<s>", "<s>", "<s>", "<s>"));
        sentence.add(new Word("1", "That", "that", "that", "DT", "DT"));
        sentence.add(new Word("2", "round", "round", "round", "JJ", "NN"));
        sentence.add(new Word("3", "table", "table", "table", "NN", "NN"));
        sentence.add(new Word("4", "might", "might", "might", "MD", "MD"));
        sentence.add(new Word("5", "collapse", "collapse", "collapse", "VB", "NN"));
        sentence.add(new Word("6", "</s>", "</s>", "</s>", "</s>", "</s>"));
        return sentence;
    }

    public void searchBigramWeights(Term term, POSTagger tagger, List<List<Word>> sentenceList) {
        double accMax = 0.0, lambda1Max = 0.0, lambda2Max = 0.0;
        for (double lambda1 = 0.025; lambda1 < 1.0; lambda1 += 0.025) {
            double lambda2 = 1.0 - lambda1;
            term.setLambdas(lambda1, lambda2);
            System.out.println("Lambda1: " + lambda1 + "\tLambda2: " + lambda2);
            int i = 0;
            for (List<Word> sent : sentenceList) {
                double prob2 = tagger.tag(sent);
                i++;
                if ((i % 100) == 0) {
                    System.out.print("*");
                    System.out.flush();
                }
            }
            ConfusionMatrix cmTest = new ConfusionMatrix(sentenceList);
            //cmTest.computeMatrix();
            //cmTest.print();
            double accuracy = cmTest.computeAccuracy();
            if (accuracy > accMax) {
                accMax = accuracy;
                lambda1Max = lambda1;
                lambda2Max = lambda2;
            }
            System.out.println("Accuracy: " + accuracy);
            System.out.println("Max: " + accMax + "\t with Lambda1: " + lambda1Max + "\tLambda2: " + lambda2Max);
        }
    }

    public void searchTrigramWeights(Term term, POSTagger tagger, List<List<Word>> sentenceList) {
        double accMax = 0.0, lambda1Max = 0.0, lambda2Max = 0.0, lambda3Max = 0.0;
        for (double lambda1 = 0.025; lambda1 < 1.0; lambda1 += 0.025) {
            for (double lambda2 = 0.025; lambda2 < (1.0 - lambda1); lambda2 += 0.025) {
                double lambda3 = 1.0 - lambda1 - lambda2;
                term.setLambdas(lambda1, lambda2, lambda3);
                System.out.println("Lambda1: " + lambda1 + "\tLambda2: " + lambda2 + "\tLambda3: " + lambda3);
                int i = 0;
                for (List<Word> sent : sentenceList) {
                    double prob2 = tagger.tag(sent);
                    i++;
                    if ((i % 100) == 0) {
                        System.out.print("*");
                        System.out.flush();
                    }
                }
                ConfusionMatrix cmTest = new ConfusionMatrix(sentenceList);
                //cmTest.computeMatrix();
                //cmTest.print();
                double accuracy = cmTest.computeAccuracy();
                if (accuracy > accMax) {
                    accMax = accuracy;
                    lambda1Max = lambda1;
                    lambda2Max = lambda2;
                    lambda3Max = lambda3;
                }
                System.out.println("Accuracy: " + accuracy);
                System.out.println("Max: " + accMax + "\t with Lambda1: " + lambda1Max + "\tLambda2: " + lambda2Max + "\tLambda3: " + lambda3Max);
            }
        }
    }

    public List<List<Word>> tag(Counts cnt, POSTagger tagger, List<List<Word>> sentenceList) {
        int i = 0;
        for (List<Word> sent : sentenceList) {
            //baseline.tag(sent);
            //double prob1 = bestfirst.tag(sent);
            //String sent1 = sent.toString();

            double prob2 = tagger.tag(sent);
            //String sent2 = sent.toString();

            //double prob3 = viterbi.tag(sent);
           /* String sent3 = sent.toString();

             if (prob2 != prob3) {
             System.out.println("Diff");
             System.out.println(prob2 + "\t" + prob3);
             }
             if (!sent2.equals(sent3)) {
             System.out.println("Diff: " + prob2 + "\t" + sent2);
             System.out.println("Diff: " + prob3 + "\t" + sent3);
             }
             */
            i++;
            if ((i % 100) == 0) {
                System.out.print("*");
                System.out.flush();
            }
        }
        return sentenceList;
    }
}
