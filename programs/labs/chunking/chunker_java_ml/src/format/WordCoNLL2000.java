package format;

/**
 *
 * @author pierre
 */
public class WordCoNLL2000 {

    String form;    // Word form or punctuation symbol.
    String ppos;    // Predicted POS tag.
    String chunk;   // Chunk (group) tag.

    public WordCoNLL2000(WordCoNLL2000 word) {
        this.form = word.form;
        this.ppos = word.ppos;
        this.chunk = word.chunk;
    }

    public WordCoNLL2000(String form, String ppos, String chunk) {
        this.form = form;
        this.ppos = ppos;
        this.chunk = chunk;
    }

    public WordCoNLL2000(String form, String ppos) {
        this.form = form;
        this.ppos = ppos;
    }

    public String getForm() {
        return form;
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
