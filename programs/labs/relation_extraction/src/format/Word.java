package format;

/**
 *
 * @author Pierre Nugues
 *
 */
/* The word format according to CoNLL X
 */
public class Word {

    int id;         // Token counter, starting at 1 for each new sentence.
    String form;    // Word form or punctuation symbol.
    String lemma;   // Lemma or stem (depending on particular data set) of word form, or an underscore if not available.
    String cpostag; // Coarse-grained part-of-speech tag, where tagset depends on the language.
    String postag;  // Fine-grained part-of-speech tag, where the tagset depends on the language, or identical to the coarse-grained part-of-speech tag if not available.
    String feats;   // Unordered set of syntactic and/or morphological features (depending on the particular language), separated by a vertical bar (|), or an underscore if not available.
    int head;       // Head of the current token, which is either a value of ID or zero ('0'). Note that depending on the original treebank annotation, there may be multiple tokens with an ID of zero.
    String deprel;  // Dependency relation to the HEAD. The set of dependency relations depends on the particular language. Note that depending on the original treebank annotation, the dependency relation may be meaningfull or simply 'ROOT'.
    int phead;      // Projective head of current token, which is either a value of ID or zero ('0'), or an underscore if not available. Note that depending on the original treebank annotation, there may be multiple tokens an with ID of zero. The dependency structure resulting from the PHEAD column is guaranteed to be projective (but is not available for all languages), whereas the structures resulting from the HEAD column will be non-projective for some sentences of some languages (but is always available).
    String pdeprel; // Dependency relation to the PHEAD, or an underscore if not available. The set of dependency relations depends on the particular language. Note that depending on the original treebank annotation, the dependency relation may be meaningfull or simply 'ROOT'.

    Word(Word word) {
        this.id = word.id;
        this.form = word.form;
        this.lemma = word.lemma;
        this.cpostag = word.cpostag;
        this.postag = word.postag;
        this.feats = word.feats;
        this.head = word.head;
        this.deprel = word.deprel;
        this.phead = word.phead;
        this.pdeprel = word.pdeprel;
    }

    Word(String id, String form, String lemma, String cpostag, String postag, String feats) {
        this.id = new Integer(id).intValue();
        this.form = form;
        this.lemma = lemma;
        this.cpostag = cpostag;
        this.postag = postag;
        this.feats = feats;
        this.head = -1;
        this.deprel = "_";
        this.phead = -1;
        this.pdeprel = "_";
    }

    Word(String id, String form, String lemma, String cpostag, String postag, String feats, String head, String deprel, String phead, String pdeprel) {
        this.id = new Integer(id).intValue();
        this.form = form;
        this.lemma = lemma;
        this.cpostag = cpostag;
        this.postag = postag;
        this.feats = feats;
        this.head = new Integer(head).intValue();
        this.deprel = deprel;
        if (!phead.equals("_")) {
            this.phead = new Integer(phead).intValue();
        } else {
            this.phead = -1;
        }
        this.pdeprel = pdeprel;
    }

    public int getId() {
        return id;
    }

    public String getForm() {
        return form;
    }

    public String getLemma() {
        return lemma;
    }

    public String getCpostag() {
        return cpostag;
    }

    public String getPostag() {
        return postag;
    }

    public String getFeats() {
        return feats;
    }

    public int getHead() {
        return head;
    }

    public String getDeprel() {
        return deprel;
    }

    public int getPhead() {
        return phead;
    }

    public String getPdeprel() {
        return pdeprel;
    }

    public void setId(int id) {
        this.id = id;
    }

    public void setHead(int head) {
        this.head = head;
    }

    public void setDeprel(String deprel) {
        this.deprel = deprel;
    }
}
