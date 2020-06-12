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
public class BeamSearch implements POSTagger {

    public Map<String, Integer> posFreqs;
    Counts cnt;
    Map<String, Integer> wordFreqs;
    Map<Pair, Integer> posBigramFreqs;
    Map<String, Map<String, Integer>> wordPOSFreqs;
    Map<String, Integer> unkPOSFreqs;
    int tokenCount;
    int sentenceCount;
    int beamSize;
    boolean trigram = true;

    public BeamSearch(Counts cnt, int beamSize) {
        this.cnt = cnt;
        this.posFreqs = cnt.getPOSFreqs();
        this.wordFreqs = cnt.getWordFreqs();
        this.posBigramFreqs = cnt.getPOSBigramFreqs();
        this.wordPOSFreqs = cnt.getWordPOSFreqs();
        this.unkPOSFreqs = cnt.getUnkPOSFreqs();
        this.tokenCount = cnt.getTokenCount();
        this.sentenceCount = cnt.getSentenceCount();
        this.beamSize = beamSize;
    }

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

        BeamSearch nbest = new BeamSearch(cnt, 4);

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
        List<POSPath> paths = generatePaths(sentence);
        for (int i = 1; i < sentence.size(); i++) {
            sentence.get(i).setPpos(paths.get(0).getPath().get(i));
        }
        return paths.get(0).getProb();
    }

    public long countPath(List<Word> sentence) {
        long pathCnt = 1;
        for (Word word : sentence) {
            if (wordPOSFreqs.get(word.getForm()) == null) {
                pathCnt *= 1.0;
            } else {
                pathCnt *= wordPOSFreqs.get(word.getForm()).size();
            }
        }
        System.out.println(pathCnt);
        return pathCnt;
    }

    public List<POSPath> generatePaths(List<Word> sentence) {
        List<POSPath> pathList = new ArrayList<>();

        POSPath start = new POSPath("<s>", 1.0);
        pathList.add(start);
        for (int i = 1; i < sentence.size(); i++) {
            Word word = sentence.get(i);
            String form = word.getForm();

            //System.out.println(form + "\t" + pairs);
            pathList = expandPaths(pathList, form);
            Collections.sort(pathList);
            Collections.reverse(pathList);
            int max = beamSize;
            if (beamSize > pathList.size()) {
                max = pathList.size();
            }
            pathList = pathList.subList(0, max);
        }
        //System.out.println(pathList.size() + ":\t" + pathList);
        return pathList;
    }

    public List<POSPath> expandPaths(List<POSPath> posPaths, String form) {
        Map<String, Integer> wordPOSCount = wordPOSFreqs.get(form);
        Set<String> posSet;
        Term term = new Term(cnt);
        if (wordPOSCount == null) {
            // Unknown words: either NN or all the possible POS
            // The latter has better results with beamSize large.
            //posSet = posFreqs.keySet();
            // Only observed unknown POS are possible
            posSet = unkPOSFreqs.keySet();
        } else {
            posSet = wordPOSCount.keySet();
        }
        List<String> posList = new ArrayList<>(posSet);
        List<POSPath> newPOSPaths = new ArrayList<>();
        for (POSPath path : posPaths) {
            for (String pos : posList) {
                POSPath newPath = new POSPath(path);
                double probTerm;
                if (trigram) {
                    probTerm = term.compute(form, newPath.getLastPOSBigram(), pos);
                } else {
                    probTerm = term.compute(form, newPath.getLastPOS(), pos);
                }
                newPath.addPOS(pos);
                newPath.probMult(probTerm);
                newPOSPaths.add(newPath);
            }
        }
        return newPOSPaths;
    }
}
