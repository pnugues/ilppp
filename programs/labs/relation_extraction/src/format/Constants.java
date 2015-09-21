package format;

/**
 *
 * @author pierre
 */
public class Constants {

    public final static String NIVRE_HOME = "/Users/pierre/Documents/Cours/EDAN20/corpus/conllx/sv/";
    //public final static String NIVRE_HOME = "";
    public final static String TRAINING_SET = NIVRE_HOME + "swedish_talbanken05_train.conll";
    public final static String TEST_SET = NIVRE_HOME + "swedish_talbanken05_test_blind.conll";
    public final static String TEST_SET_PARSED = NIVRE_HOME + "result_output.conll";
    public final static String ARFF_FILE = NIVRE_HOME + "simple4.arff";
    public final static String ARFF_MODEL = NIVRE_HOME + "simple4.model";

    public final static String UTB_HOME = "/Users/pierre/Documents/Cours/EDAN20/corpus/universal_treebanks_v1.0/";
    public final static String TRAINING_SET_FR = UTB_HOME + "fr/fr-universal-train.conll";
    public final static String TRAINING_SET_ES = UTB_HOME + "es/es-universal-train.conll";

    public final static String SUBJECT = "SS";
    public final static String OBJECT = "OO";

    //public final static String SUBJECT = "nsubj";
    //public final static String OBJECT = "dobj";
    public static void main(String[] args) {
        // TODO code application logic here
    }
}
