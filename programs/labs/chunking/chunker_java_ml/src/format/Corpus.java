package format;

import java.io.*;
import java.util.*;
import mlchunker.Features;

/**
 *
 * @author pierre
 */
public class Corpus {

    /**
     * @param args the command line arguments
     */
    protected List<List<WordCoNLL2000>> sentenceList;
    protected List<Features> featureList;

    public Corpus() {
    }

    public void load(String file) throws IOException {
        ReaderWriterCoNLL2000 reader = new ReaderWriterCoNLL2000();
        reader.loadFile(new File(file));
        sentenceList = reader.getSentenceList();
    }

    public void save(String file) throws IOException {
        ReaderWriterCoNLL2000 reader = new ReaderWriterCoNLL2000();
        reader.saveFile(new File(file), sentenceList);
    }

    public void extractBaselineFeatures() {
        featureList = new ArrayList<Features>();
        for (List<WordCoNLL2000> sentence : sentenceList) {
            for (WordCoNLL2000 word : sentence) {
                featureList.add(new Features(word));
            }
        }
    }

    public void printFeatures() {
        System.out.println(featureList.size());
        for (Features features : featureList) {
            System.out.println(features.getPpos() + "\t" + features.getChunk());
        }
    }
}
