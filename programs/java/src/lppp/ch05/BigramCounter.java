package lppp.ch05;

import java.io.IOException;
import java.util.Map;
import java.util.TreeMap;

/**
 * Created by Pierre Nugues on 25/07/15.
 */
public class BigramCounter {
    Map<String, Integer> count(String[] words) {
        Map<String, Integer> counts = new TreeMap<>();
        for (int i = 0; i < words.length - 1; i++) {
            String bigram = words[i] + "\t" + words[i + 1];
            if (counts.get(bigram) == null) {
                counts.put(bigram, 1);
            } else {
                counts.put(bigram, counts.get(bigram) + 1);
            }
        }
        return counts;
    }

    public static void main(String[] args) throws IOException {
        FileReader reader = new FileReader();
        String text = reader.readFile(args[0]);
        Tokenizer tokenizer = new Tokenizer();
        String[] words = tokenizer.tokenize(text);
        BigramCounter bigramCounter = new BigramCounter();
        Map<String, Integer> bigramCounts = bigramCounter.count(words);
        for (String bigramCount: bigramCounts.keySet()) {
            System.out.println(bigramCounts.get(bigramCount) + "\t" + bigramCount);
        }
    }
}
