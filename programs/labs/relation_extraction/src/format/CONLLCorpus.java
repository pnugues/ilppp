package format;

import java.io.*;
import java.util.*;

/**
 *
 * @author Pierre Nugues
 */
// The class to load a CONLL corpus 2006 and 2007 and store it into a list.
public class CONLLCorpus {

    private List<List<Word>> sentenceList;

    public List<List<Word>> loadFile(File file) throws IOException {
        sentenceList = new ArrayList<List<Word>>();
        List<Word> sentence = new ArrayList<Word>();
        Word root = new Word("0", "ROOT", "ROOT", "ROOT", "ROOT", "ROOT", "0", "ROOT", "0", "ROOT");

        Word curWord;

        sentence.add(root);

        int sentenceCount = 0;
        int lineCount = 0;
        BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(file), "UTF-8"));
        String line = null;
        while ((line = reader.readLine()) != null) {
            lineCount++;
            curWord = makeWord(line);
            if (curWord != null) { // A word
                sentence.add(curWord);
            } else { // An empty line denoting a new sentence
                sentenceList.add(sentence);
                sentence = new ArrayList<Word>();
                sentence.add(new Word(root));
                sentenceCount++;
            }
            if ((lineCount % 10000) == 0) {
                System.out.println("Read: " + lineCount + " lines, " + sentenceCount + " sentences.");
            }
        }
        reader.close();
        return sentenceList;
    }

    private Word makeWord(String line) {
        String[] wordD = line.split("\t");
        Word word = null;
        // Test set
        if (wordD.length == 6) {
            word = new Word(wordD[0], wordD[1], wordD[2], wordD[3], wordD[4], wordD[5]);
        }
        // Training set
        if (wordD.length == 10) {
            word = new Word(wordD[0], wordD[1], wordD[2], wordD[3], wordD[4], wordD[5], wordD[6], wordD[7], wordD[8], wordD[9]);
        }
        return word;
    }

    public void printFile(List<List<Word>> sentenceList) {
        for (int i = 0; i < sentenceList.size(); i++) {
            for (int j = 0; j < (sentenceList.get(i)).size(); j++) {
                System.out.print((sentenceList.get(i)).get(j).getForm() + " ");
            }
            System.out.println("");
        }
    }

    public void saveFile(File file, List<List<Word>> sentenceList) throws IOException {
        BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(file), "UTF-8"));

        for (int i = 0; i < sentenceList.size(); i++) {
            for (int j = 0; j < (sentenceList.get(i)).size(); j++) {
                writer.write((sentenceList.get(i)).get(j).getId() + "\t");
                writer.write((sentenceList.get(i)).get(j).getForm() + "\t");
                writer.write((sentenceList.get(i)).get(j).getLemma() + "\t");
                writer.write((sentenceList.get(i)).get(j).getCpostag() + "\t");
                writer.write((sentenceList.get(i)).get(j).getPostag() + "\t");
                writer.write((sentenceList.get(i)).get(j).getFeats() + "\t");
                writer.write((sentenceList.get(i)).get(j).getHead() + "\t");
                writer.write((sentenceList.get(i)).get(j).getDeprel() + "\t");
                writer.write((sentenceList.get(i)).get(j).getPhead() + "\t");
                writer.write((sentenceList.get(i)).get(j).getPdeprel() + "\n");
            }
            if (i != sentenceList.size()) {
                writer.write("\n");
            }
        }
        writer.close();
    }

    public static void main(String[] args) throws IOException {
        File trainingSet = new File(Constants.TRAINING_SET);
        CONLLCorpus trainingCorpus = new CONLLCorpus();
        List<List<Word>> sentenceList;
        sentenceList = trainingCorpus.loadFile(trainingSet);
    }
}
