package lppp.ch05;

import java.io.IOException;

/**
 * Created by Pierre Nugues on 25/07/15.
 */
public class Tokenizer {

    String[] tokenize(String text) {
        //String [] words = text.split("[\\s\\-,;:!?.’\'«»()–...&‘’“”*—]+");
        //String [] words = text.split("[^a-zåàâäæçéèêëîïôöœßùûüÿA-ZÅÀÂÄÆÇÉÈÊËÎÏÔÖŒÙÛÜŸ’\\-]+");
        //String [] words = text.split("\\W+"); // Not unicode friendly
        String[] words = text.split("[^\\p{L}]+");
        return words;
    }

    public static void main(String[] args) throws IOException {
        FileReader reader = new FileReader();
        String text = reader.readFile(args[0]);
        Tokenizer tokenizer = new Tokenizer();
        String[] words = tokenizer.tokenize(text);
        for (int i = 0; i < words.length; i++) {
            System.out.println(words[i]);
        }
    }
}
