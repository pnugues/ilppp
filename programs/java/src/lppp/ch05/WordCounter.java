package lppp.ch05;

import java.io.IOException;
import java.util.Map;
import java.util.TreeMap;

/**
 * Created by Pierre Nugues on 25/07/15.
 */
public class WordCounter {
    public static void main(String[] args) throws IOException {
        FileReader reader = new FileReader();
        String text = reader.readFile(args[0]);
        Tokenizer tokenizer = new Tokenizer();
        String[] words = tokenizer.tokenize(text);
        WordCounter wordCounter = new WordCounter();
        Map<String, Integer> wordCounts = wordCounter.count(words);
        for (String wordCount : wordCounts.keySet()) {
            System.out.println(wordCounts.get(wordCount) + "\t" + wordCount);
        }
    }

    Map<String, Integer> count(String[] words) {
        Map<String, Integer> counts = new TreeMap<>();
        for (String word : words) {
            if (counts.get(word) == null) {
                counts.put(word, 1);
            } else {
                counts.put(word, counts.get(word) + 1);
            }
        }
        return counts;
    }
}
