package blchunker;

import java.util.*;
import format.Corpus;
import mlchunker.Features;
import format.WordCoNLL2000;
import format.Constants;
import java.io.IOException;

/**
 *
 * @author pierre
 */
public class BLChunkerIncomplete extends Corpus {

    Map<String, Integer> posCnt;
    Map<String, Integer> chunkCnt;
    Map<Features, Integer> associationFreq;
    Map<String, String> bestAssociations;
    Set<String> uniquePosTags;
    Set<String> uniqueChunkTags;

    // This method counts the associations (POS, Chunk). It uses a hashmap.
    public void countAssoc() {
        associationFreq = new HashMap<Features, Integer>();
        // Complete code here.
    }

    public void printAssocCounts() {
        Set<Features> feats = new HashSet<Features>(associationFreq.keySet());
        for (Features feat : feats) {
            System.out.println(feat.getPpos() + "\t" + feat.getChunk() + "\t" + associationFreq.get(feat));
        }
    }

    public void printBestAssoc() {
        Set<String> pposs = new HashSet<String>(bestAssociations.keySet());
        for (String ppos : pposs) {
            System.out.println(ppos + "\t\t" + bestAssociations.get(ppos));
        }
    }

    public void getUniqueTags() {
        uniquePosTags = new HashSet<String>();
        uniqueChunkTags = new HashSet<String>();
        for (Features feat : featureList) {
            uniquePosTags.add(feat.getPpos());
            uniqueChunkTags.add(feat.getChunk());
        }
    }

    // This method selects the best (most frequent) association: POS--Chunk
    public void selectBestAssoc() {
        bestAssociations = new HashMap<String, String>();
        System.out.println(uniquePosTags.size() + " POS tags\t" + uniqueChunkTags.size() + " chunk tags");
        // Complete code here.
    }

    // This method tags the words with their chunk.
    public void tag() {
        for (List<WordCoNLL2000> sent : sentenceList) {
            // Modify code here.
            for (WordCoNLL2000 word : sent) {
                word.setChunk("");
            }
        }
    }

    public static void main(String[] args) throws IOException {
        BLChunkerIncomplete chunker = new BLChunkerIncomplete();
        chunker.load(Constants.TRAINING_SET_2000);
        chunker.extractBaselineFeatures();
        chunker.getUniqueTags();
        chunker.countAssoc(); // This method counts the associations (POS, Chunk). It uses a hashmap.
        //chunker.printAssocCounts();
        chunker.selectBestAssoc(); // This method selects the best (most frequent) association: POS--Chunk
        chunker.printBestAssoc();
        chunker.load(Constants.TEST_SET_2000);
        chunker.tag(); // This method tags the words with their chunk.
        chunker.save(Constants.TEST_SET_PREDICTED_2000);
        //chunker.printFeatures();
    }
}
