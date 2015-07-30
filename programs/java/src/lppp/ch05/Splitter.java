package lppp.ch05;

import java.io.IOException;

/**
 * Created by Pierre Nugues on 29/07/15.
 */
public class Splitter {
    Tokenizer tokenizer;

    public Splitter(Tokenizer tokenizer) {
        this.tokenizer = tokenizer;
    }

    public static void main(String[] args) throws IOException {
        FileReader reader = new FileReader();
        String text = reader.readFile(args[0]);
        Tokenizer tokenizer = new Tokenizer();
        Splitter splitter = new Splitter(tokenizer);
        String[] sentences = splitter.split(text);
        for (int i = 0; i < sentences.length; i++) {
            System.out.println(sentences[i]);
        }

    }

    String[] split(String text) {
        // One line
        text = text.replaceAll("\\s+", " ");
        //Clean up everything that is not a letter or end of sentence
        text = text.replaceAll("[^\\p{L}.;:?!]+", " ");
        // A sentence starts with a capital letter and end with a punctuation
        text = text.replaceAll("[.;:?!] +([A-ZÅÀÂÄÆÇÉÈÊËÎÏÔÖŒÙÛÜŸ])", "\n$1");
        String[] sentences = text.split("\\n");
        for (int i = 0; i < sentences.length; i++) {
            sentences[i] = "<s> " + tokenizer.tokenize2(sentences[i]) + " </s>";
            sentences[i] = sentences[i].replaceAll(" +", " ").toLowerCase();
        }
        return sentences;
    }

}
