package mlchunker;

import format.WordCoNLL2000;

/**
 *
 * @author pierre
 */
// This class extracts the baseline feature: the part of speech and the class, the chunk tag. 
public class Features {

    String ppos;
    String chunk;

    public Features(WordCoNLL2000 word) {
        ppos = word.getPpos();
        chunk = word.getChunk();
    }

    public Features(String ppos, String chunk) {
        this.ppos = ppos;
        this.chunk = chunk;
    }

    public boolean equals(Object features) {
        String signature1 = getPpos() + getChunk();
        String signature2 = ((Features) features).getPpos() + ((Features) features).getChunk();
        return signature1.equals(signature2);
    }

    public int hashCode() {
        return (getPpos() + getChunk()).hashCode();
    }

    public String getPpos() {
        return ppos;
    }

    public String getChunk() {
        return chunk;
    }

    public void setChunk(String chunk) {
        this.chunk = chunk;
    }
}
