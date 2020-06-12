package perceptron;

import format.CONLLCorpus;
import format.Constants;
import format.Pair;
import format.Word;
import pos_tagging.POSTagger;
import util.ConfusionMatrix;
import util.Counts;
import util.POSPathPerceptron;
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
    boolean trigram = false;
    Perceptron perceptron;

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
        int epochMax = 3;
        if (args.length == 1) {
            epochMax = Integer.valueOf(args[0]);
        }
        File trainingSet = new File(Constants.TRAINING_SET);
        File devSet = new File(Constants.DEV_SET);
        File testSet = new File(Constants.TEST_SET);
        CONLLCorpus trainingCorpus = new CONLLCorpus();
        CONLLCorpus devCorpus = new CONLLCorpus();
        CONLLCorpus testCorpus = new CONLLCorpus();

        List<List<Word>> sentenceList, sentenceDevList, sentenceTestList;
        sentenceList = trainingCorpus.loadFile(trainingSet);
        sentenceDevList = devCorpus.loadFile(devSet);
        sentenceTestList = testCorpus.loadFile(testSet);

        Counts cnt = new Counts(sentenceList);
        cnt.computeFreqs();
        //cnt.printStats();

        BeamSearch nbest = new BeamSearch(cnt, 32);
        // We set here all the words that are unseen in the training set to ukn
        nbest.setUnknow(sentenceDevList, cnt);
        nbest.setUnknow(sentenceTestList, cnt);
        // And we append dev set to the training set
        sentenceList.addAll(sentenceDevList);
        // We need to recount the frequencies
        cnt = new Counts(sentenceList);
        cnt.computeFreqs();
        // And to reinitialize the beam search. This is a bad design
        // This should be done in one step and needs a refactoring
        nbest = new BeamSearch(cnt, 32);

        Perceptron perceptron = new Perceptron(cnt);
        perceptron.initPOSBigramWeights();
        perceptron.initWordPOSBigrams();
        nbest.setPerceptron(perceptron);
        int updates = 1;
        int epoch = 0;
        long iter = 0;
        while (epoch < epochMax) {
            updates = 0;
            epoch++;
            int i = 0;
            int[] shuffleInx = nbest.shuffleInx(sentenceList.size());
            for (int j = 0; j < sentenceList.size(); j++) {
                //for (List<Word> sentence : sentenceList) {
                List<Word> sentence = sentenceList.get(shuffleInx[j]);
                iter++;
                if (i % 1000 == 0) {
                    System.out.print(".");
                    System.out.flush();
                }
                i++;
                //System.out.println("Ambiguity: " + nbest.countPath(sentence));
                List<POSPathPerceptron> listS;
                listS = nbest.generatePaths(sentence);
                Collections.sort(listS);
                Collections.reverse(listS);
                //for (POSPathPerceptron s : listS) {
                //  System.out.println(s);
                //}
                POSPathPerceptron bestPOSPath = listS.get(0);
                nbest.assignPOS(sentence, bestPOSPath);
                perceptron.updateBigramWeights(sentence, iter);
                updates += perceptron.updateWordPOSWeights(sentence, iter);
            }
            ConfusionMatrix cmTest = new ConfusionMatrix(sentenceList);
            System.out.println("Accuracy: " + cmTest.computeAccuracy());
            System.out.println("Epoch: " + epoch + "\tUpdates: " + updates);
        }
        perceptron.computeBigramWeightsAve(iter);
        perceptron.computeWordPOSWeightsAve(iter);

        Map<String, Integer> cntPOSUnk = cnt.countUnkPOSFreqs(sentenceDevList);
        nbest.setUnk(cntPOSUnk);

        sentenceDevList = nbest.tagCorpus(sentenceDevList);
        ConfusionMatrix cmTest = new ConfusionMatrix(sentenceDevList);
        System.out.println("Accuracy dev set: " + cmTest.computeAccuracy());

        sentenceTestList = nbest.tagCorpus(sentenceTestList);
        cmTest = new ConfusionMatrix(sentenceTestList);
        System.out.println("Accuracy test set: " + cmTest.computeAccuracy());

        /*
         Tester post = new Tester();
         List<Word> sentence = post.makeTheSentence();
         List<List<Word>> corpus = new ArrayList<>();
         corpus.add(sentence);
         System.out.println(nbest.countPath(sentence));
         List<POSPathPerceptron> listS;
         int updates = 1;
         while (updates != 0) {
         listS = nbest.generatePaths(sentence);
         Collections.sort(listS);
         Collections.reverse(listS);
         for (POSPathPerceptron s : listS) {
         System.out.println(s);
         }
         POSPathPerceptron bestPOSPath = listS.get(0);
         nbest.assignPOS(sentence, bestPOSPath);
         perceptron.updateBigramWeights(sentence);
         updates = perceptron.updateWordPOSWeights(sentence);
         }
         System.out.println(sentence);*/
        /*
         Counts cnt1 = new Counts(corpus);
         cnt1.computeFreqs();
         System.out.println(sentence);
         System.out.println(cnt1.getPOSBigramFreqs());
         System.out.println(cnt1.getPPOSBigramFreqs());
         System.out.println(cnt1.getWordPOSFreqs());
         System.out.println(cnt1.getWordPPOSFreqs());

         Map<Pair, Double> weights = perceptron.getPOSBigramWeights();
         Set<Pair> pairs = weights.keySet();
         for (Pair pair : pairs) {
         if (weights.get(pair) != 0.0) {
         System.out.println(pair + "\t" + weights.get(pair));
         }
         }
         //System.out.println(nbest.tag(sentence));
         */
    }

    @Override
    public double tag(List<Word> sentence) {
        List<POSPathPerceptron> paths = generatePaths(sentence);
        for (int i = 1; i < sentence.size(); i++) {
            sentence.get(i).setPpos(paths.get(0).getPath().get(i));
        }
        return paths.get(0).getProb();
    }

    public long countPath(List<Word> sentence) {
        long pathCnt = 1;
        for (Word word : sentence) {
            //System.out.println(word);
            if (wordPOSFreqs.get(word.getForm()) == null) {
                pathCnt *= 1.0;
            } else {
                pathCnt *= wordPOSFreqs.get(word.getForm()).size();
                //System.out.println(wordPOSFreqs.get(word.getForm()).size() + "\t" + pathCnt);
            }
        }
        //System.out.println(sentence);
        //System.out.println(pathCnt);
        return pathCnt;
    }

    public List<POSPathPerceptron> generatePaths(List<Word> sentence) {
        List<POSPathPerceptron> pathList = new ArrayList<>();

        POSPathPerceptron start = new POSPathPerceptron("<s>", 0.0);
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

    public List<POSPathPerceptron> expandPaths(List<POSPathPerceptron> posPaths, String form) {
        Map<String, Integer> wordPOSCount = wordPOSFreqs.get(form);
        Set<String> posSet = new TreeSet<>();
        Term term = new Term(cnt);
        if (wordPOSCount == null) {
            // Unknown words: either NNP or all the possible POS
            // The latter has better results with beamSize large.
            //posSet = posFreqs.keySet();
            // Only observed unknown POS are possible
            //posSet = unkPOSFreqs.keySet();
            posSet.add("NNP");
        } else {
            posSet = wordPOSCount.keySet();
        }
        List<String> posList = new ArrayList<>(posSet);
        List<POSPathPerceptron> newPOSPaths = new ArrayList<>();
        for (POSPathPerceptron path : posPaths) {
            for (String pos : posList) {
                POSPathPerceptron newPath = new POSPathPerceptron(path);
                double probTerm;
                if (trigram) {
                    probTerm = term.compute(form, newPath.getLastPOSBigram(), pos);
                } else {
                    //probTerm = term.compute(form, newPath.getLastPOS(), pos);
                    Pair posBigram = new Pair(newPath.getLastPOS(), pos);
                    //System.err.println(posBigram);
                    probTerm = perceptron.getPOSBigramWeights().get(posBigram);
                    if (perceptron.getWordPOSWeights().get(form) != null) {
                        probTerm += perceptron.getWordPOSWeights().get(form).get(pos);
                    }
                }
                newPath.addPOS(pos);
                newPath.probAdd(probTerm);
                newPOSPaths.add(newPath);
            }
        }
        return newPOSPaths;
    }

    public List<POSPathPerceptron> generatePathsAndTag(List<Word> sentence) {
        List<POSPathPerceptron> pathList = new ArrayList<>();

        POSPathPerceptron start = new POSPathPerceptron("<s>", 0.0);
        pathList.add(start);
        for (int i = 1; i < sentence.size(); i++) {
            Word word = sentence.get(i);
            String form = word.getForm();

            //System.out.println(form + "\t" + pairs);
            pathList = expandPathsandTag(pathList, form);
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

    public List<POSPathPerceptron> expandPathsandTag(List<POSPathPerceptron> posPaths, String form) {
        Map<String, Integer> wordPOSCount = wordPOSFreqs.get(form);
        Set<String> posSet = new TreeSet<>();
        Term term = new Term(cnt);
        if (wordPOSCount == null) {
            // Unknown words: either NNP or all the possible POS
            // The latter has better results with beamSize large.
            //posSet = posFreqs.keySet();
            // Only observed unknown POS are possible
            //posSet = unkPOSFreqs.keySet();
            posSet.add("NNP");
        } else {
            posSet = wordPOSCount.keySet();
        }
        List<String> posList = new ArrayList<>(posSet);
        List<POSPathPerceptron> newPOSPaths = new ArrayList<>();
        for (POSPathPerceptron path : posPaths) {
            for (String pos : posList) {
                POSPathPerceptron newPath = new POSPathPerceptron(path);
                double probTerm;
                if (trigram) {
                    probTerm = term.compute(form, newPath.getLastPOSBigram(), pos);
                } else {
                    //probTerm = term.compute(form, newPath.getLastPOS(), pos);
                    Pair posBigram = new Pair(newPath.getLastPOS(), pos);
                    //System.err.println(posBigram);
                    probTerm = perceptron.getPOSBigramWeightsAverage().get(posBigram);
                    if (perceptron.getWordPOSWeights().get(form) != null) {
                        probTerm += perceptron.getWordPOSWeightsAverage().get(form).get(pos);
                    }
                }
                newPath.addPOS(pos);
                newPath.probAdd(probTerm);
                newPOSPaths.add(newPath);
            }
        }
        return newPOSPaths;
    }

    public void setPerceptron(Perceptron perceptron) {
        this.perceptron = perceptron;
    }

    public void setUnknow(List<List<Word>> sentenceList, Counts cnt) {
        Map<String, Integer> wordFreqs = cnt.getWordFreqs();
        for (List<Word> sentence : sentenceList) {
            for (Word word : sentence) {
                if (wordFreqs.get(word.getForm()) == null) {
                    word.setForm("UKN");
                }
            }

        }
    }

    public void assignPOS(List<Word> sentence, POSPathPerceptron bestPath) {
        List<String> posPath = bestPath.getPath();
        if (sentence.size() != posPath.size()) {
            System.err.println("POS path and sentence of different size");
        }
        int i = 0;
        for (Word word : sentence) {
            word.setPpos(posPath.get(i));
            i++;
        }
    }

    public void setUnk(Map<String, Integer> unkPOSFreqs) {
        this.unkPOSFreqs = unkPOSFreqs;
    }

    public List<List<Word>> tagCorpus(List<List<Word>> sentenceList) {
        int i = 0;
        for (List<Word> sentence : sentenceList) {
            if (i % 1000 == 0) {
                System.out.print(".");
                System.out.flush();
            }
            i++;
            //System.out.println("Ambiguity: " + nbest.countPath(sentence));
            List<POSPathPerceptron> listS;
            listS = generatePathsAndTag(sentence);
            Collections.sort(listS);
            Collections.reverse(listS);
            //for (POSPathPerceptron s : listS) {
            //  System.out.println(s);
            //}
            POSPathPerceptron bestPOSPath = listS.get(0);
            assignPOS(sentence, bestPOSPath);
        }
        return sentenceList;
    }

    public int[] shuffleInx(int size) {
        int[] shuffledInx = new int[size];
        Random random = new Random();
        List<Integer> shuffledList = new ArrayList<Integer>();
        for (int i = 0; i < size; i++) {
            shuffledList.add(i);
        }
        for (int i = 0; i < size; i++) {
            int inx = random.nextInt(shuffledList.size());
            shuffledInx[i] = shuffledList.get(inx);
            shuffledList.remove(inx);
        }
        return shuffledInx;
    }
    // Resultats: TEST
    // perceptron bigrammes, inconnus: NNP, beam = 16, epochs: 7, 94,42
    // perceptron bigrammes, inconnus: NNP, beam = 16, epochs: 6, 0,9447604
    // perceptron moyenné bigrammes, inconnus: NNP, beam = 4,epoch: 3, 0.9588217
    // perceptron moyenné bigrammes, inconnus: NNP, beam = 8,epoch: 4, Accuracy test set: 0.9594459
    // perceptron moyenné bigrammes, inconnus: NNP, beam = 16,epoch: 5, Accuracy test set: 0.9594805
    // perceptron moyenné bigrammes, inconnus: NNP, beam = 32,epoch: 6, Accuracy test set: 0.9597233
    // Beam 32, moyenné, bigrammes:
    // Epochs = 2, Accuracy dev set: 0.95534647, Accuracy test set: 0.9597233
    // Epochs = 3, Accuracy dev set: 0.95486695, Accuracy test set: 0.959914
    // Epochs = 4, Accuracy dev set: 0.9549868, Accuracy test set: 0.9597233
    // Epochs = 5, Accuracy dev set: 0.95483696, Accuracy test set: 0.95967126
    // Epochs = 6, Accuracy dev set: 0.9549568, Accuracy test set: 0.9597233
    // Epochs = 7, Accuracy dev set: 0.9547171, Accuracy test set: 0.9596192
    // Epochs = 8, Accuracy dev set: 0.9547471, Accuracy test set: 0.9596886
    // Epochs = 9, Accuracy dev set: 0.9545373, Accuracy test set: 0.95953256
    // Epochs = 10, Accuracy dev set: 0.9545373, Accuracy test set: 0.95956725
    // Epochs = 11, Accuracy dev set: 0.9544474, Accuracy test set: 0.9596539
    // Epochs = 12, Accuracy dev set: 0.9546272, Accuracy test set: 0.9596192

    // Nouvelle méthodes pour les mots inconnus, marqués UKN s'il ne sont pas vu
    // dans l'ensemble d'apprentissage
    // Epochs 2, Accuracy dev set: 0.96149004, Accuracy test set: 0.96152645
    // Epochs 3, Accuracy dev set: 0.96155, Accuracy test set: 0.96152645
    // Epochs 4, Accuracy dev set: 0.96199954, Accuracy test set: 0.9614744
    // Epochs 5, Accuracy dev set: 0.96253896, Accuracy test set: 0.9613704
    // Epochs 6, Accuracy dev set: 0.962479, Accuracy test set: 0.9613704
    // Epochs 7, Accuracy dev set: 0.96304846, Accuracy test set: 0.96138775
    // Epochs 8, Accuracy dev set: 0.96286863, Accuracy test set: 0.9615438
    // Avec les indices des phrases tirés au sort:
    // Beam 32, epochs 5: Accuracy dev set: 0.9646068, Accuracy test set: 0.9620986
    // À faire :
    // 1. optimiser le calcul de la moyenne, comme expliqué dans Hal Daumé, Course in machine learning (CIML) ch. 3 ou Grzegorz Chrupała, Dietrich Klakow (LREC)
    // 2. Tirer au sort les indices de la mise à jour
    // 3. Introduire Viterbi
    // 4. Voir comment traiter les mots inconnus
    // 5. Passer au trigrammes
    // 6. Optimiser les époques avec l'ensemble de développement. S'arrêter quand
    // il n'y a plus d'amélioration
    // 7. Faire l'apprentissage sur l'ensemble d'entraînement et de développement où
    // les mots inconnus sont marqué UKN
    // Voir si ça ne marche pas avec Markov aussi
}
