package format;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

/**
 * @author Pierre Nugues
 */
// The class to load a CONLL corpus 2006 and 2007 and store it into a list.
public class CONLLCorpus {

    private List<List<Word>> sentenceList;

    public static void main(String[] args) throws IOException {
        File trainingSet = new File(Constants.TRAINING_SET);
        CONLLCorpus trainingCorpus = new CONLLCorpus();
        List<List<Word>> sentenceList;
        sentenceList = trainingCorpus.loadFile(trainingSet);
        trainingCorpus.printFile(sentenceList);
    }

    public List<List<Word>> loadFile(File file) throws IOException {
        sentenceList = new ArrayList<>();
        List<Word> sentence = new ArrayList<>();
        Word root = new Word("0", "<s>", "<s>", "<s>", "<s>", "<s>");
        Word eos = new Word("0", "</s>", "</s>", "</s>", "</s>", "</s>");

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
                int sizeS = sentence.size();
                Word newEos = new Word(eos);
                newEos.setId(sizeS);
                sentence.add(newEos);
                sentenceList.add(sentence);
                sentence = new ArrayList<>();
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
            for (int j = 1; j < (sentenceList.get(i)).size() - 1; j++) {
                writer.write((sentenceList.get(i)).get(j).getId() + "\t");
                writer.write((sentenceList.get(i)).get(j).getForm() + "\t");
                writer.write((sentenceList.get(i)).get(j).getLemma() + "\t");
                writer.write((sentenceList.get(i)).get(j).getPlemma() + "\t");
                writer.write((sentenceList.get(i)).get(j).getPos() + "\t");
                writer.write((sentenceList.get(i)).get(j).getPpos() + "\n");
            }
            if (i != sentenceList.size()) {
                writer.write("\n");
            }
        }
        writer.close();
    }
}
