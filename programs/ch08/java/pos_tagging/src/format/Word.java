package format;

/**
 * @author Pierre Nugues
 */
/* The word format according to CoNLL X
 */
public class Word {

    int id;         // Token counter, starting at 1 for each new sentence.
    String form;    // Word form or punctuation symbol.
    String lemma;   // Lemma or stem (depending on particular data set) of word form, or an underscore if not available.
    String plemma;   // perdicted lemma.
    String pos; //  part-of-speech tag, where tagset depends on the language.
    String ppos; // predicted pos.
/*    String feats;   // Unordered set of syntactic and/or morphological features (depending on the particular language), separated by a vertical bar (|), or an underscore if not available.
     String pfeats;   // preicted feats.
     int head;       // Head of the current token, which is either a value of ID or zero ('0'). Note that depending on the original treebank annotation, there may be multiple tokens with an ID of zero.
     String deprel;  // Dependency relation to the HEAD. The set of dependency relations depends on the particular language. Note that depending on the original treebank annotation, the dependency relation may be meaningfull or simply 'ROOT'.
     int phead;      // Projective head of current token, which is either a value of ID or zero ('0'), or an underscore if not available. Note that depending on the original treebank annotation, there may be multiple tokens an with ID of zero. The dependency structure resulting from the PHEAD column is guaranteed to be projective (but is not available for all languages), whereas the structures resulting from the HEAD column will be non-projective for some sentences of some languages (but is always available).
     String pdeprel; // Dependency relation to the PHEAD, or an underscore if not available. The set of dependency relations depends on the particular language. Note that depending on the original treebank annotation, the dependency relation may be meaningfull or simply 'ROOT'.*/

    public Word(Word word) {
        this.id = word.id;
        this.form = word.form;
        this.lemma = word.lemma;
        this.plemma = word.plemma;
        this.pos = word.pos;
        this.ppos = word.ppos;
    }

    public Word(String id, String form, String lemma, String plemma, String pos, String ppos) {
        this.id = Integer.valueOf(id);
        this.form = form;
        this.lemma = lemma;
        this.plemma = plemma;
        this.pos = pos;
        this.ppos = ppos;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getForm() {
        return form;
    }

    public void setForm(String form) {
        this.form = form;
    }

    public String getLemma() {
        return lemma;
    }

    public String getPlemma() {
        return plemma;
    }

    public String getPos() {
        return pos;
    }

    public String getPpos() {
        return ppos;
    }

    public void setPpos(String ppos) {
        this.ppos = ppos;
    }

    @Override
    public String toString() {

        return id + "\t" + form + "\t" + lemma + "\t" + plemma + "\t" + pos + "\t" + ppos;
    }
}
