package format;

/**
 *
 * @author pierre
 */
public class Constants {

    public final static String CHUNKER_HOME = "/Users/pierre/Documents/Cours/EDAN20/";
    public final static String TRAINING_SET_2000 = CHUNKER_HOME + "corpus/conll2000/train.txt";
    public final static String TEST_SET_2000 = CHUNKER_HOME + "corpus/conll2000/test.txt";
    public final static String TEST_SET_PREDICTED_2000 = CHUNKER_HOME + "corpus/conll2000/test_pred.txt";
    public final static String ARFF_DATA = Constants.CHUNKER_HOME + "corpus/conll2000/chunker.arff";
    public final static String ARFF_MODEL = Constants.CHUNKER_HOME + "corpus/conll2000/chunker.model";
    public final static String ARFF_HEADER = "@relation chunk\n\n"
            + "@attribute pos {#, $, \"''\", (, ), \",\", ., :, CC, CD, DT, EX, FW, IN, JJ, JJR, JJS, MD, NN, NNP, NNPS, NNS, PDT, POS, PRP, PRP$, RB, RBR, RBS, RP, SYM, TO, UH, VB, VBD, VBG, VBN, VBP, VBZ, WDT, WP, WP$, WRB, ``}\n"
            + "@attribute chunk {B-ADJP, B-ADVP, B-CONJP, B-INTJ, B-LST, B-NP, B-PP, B-PRT, B-SBAR, B-UCP, B-VP, I-ADJP, I-ADVP, I-CONJP, I-INTJ, I-NP, I-PP, I-PRT, I-SBAR, I-UCP, I-VP, O}\n\n"
            + "@data\n";

    public static void main(String[] args) {
        // TODO code application logic here
    }
}
