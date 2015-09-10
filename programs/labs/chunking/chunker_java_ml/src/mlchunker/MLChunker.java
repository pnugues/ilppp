package mlchunker;

import java.io.*;
import java.util.*;
import wekaglue.WekaGlue;
import format.Constants;
import format.ReaderWriterCoNLL2000;
import format.WordCoNLL2000;
import format.Corpus;

/**
 *
 * @author pierre
 */
public class MLChunker extends Corpus {

    WekaGlue wekaGlue;

    public MLChunker() {
    }

    public void writeARFF(String file) throws IOException {
        ReaderWriterCoNLL2000 reader = new ReaderWriterCoNLL2000();
        reader.saveARFF(new File(file), sentenceList);
    }

    public void tag() {
        wekaGlue = new WekaGlue();
        wekaGlue.create(Constants.ARFF_MODEL, Constants.ARFF_DATA);
        for (List<WordCoNLL2000> sent : sentenceList) {
            for (WordCoNLL2000 word : sent) {
                String[] features = new String[1];
                features[0] = word.getPpos();
                word.setChunk(wekaGlue.classify(features));
            }
        }
    }

    public static void main(String[] args) throws IOException {
        MLChunker chunker = new MLChunker();
        if (args.length < 1) {
            System.out.println("Usage: java mlchunker.MLChunker (-train|-tag)");
            System.exit(0);
        }
        if (args[0].equals("-train")) {
            chunker.load(Constants.TRAINING_SET_2000);
            chunker.extractBaselineFeatures();
            chunker.writeARFF(Constants.ARFF_DATA);
        } else if (args[0].equals("-tag")) {
            chunker.load(Constants.TEST_SET_2000);
            chunker.tag();
            chunker.save(Constants.TEST_SET_PREDICTED_2000);
        } else {
            System.out.println("Usage: java mlchunker.MLChunker (-train|-tag)");
        }
    }
}
