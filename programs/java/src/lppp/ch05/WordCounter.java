package lppp.ch05;

import java.io.IOException;
import java.util.Arrays;
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
        Map<String, Integer> bigramCounts = wordCounter.countBigrams(words);
        for (String bigramCount : bigramCounts.keySet()) {
            System.out.println(bigramCounts.get(bigramCount) + "\t" + bigramCount);
        }
        Map<String, Integer> nCounts = wordCounter.countNgrams(words, 7);
        for (String nCount : nCounts.keySet()) {
            System.out.println(nCounts.get(nCount) + "\t" + nCount);
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

    Map<String, Integer> countBigrams(String[] words) {
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

    Map<String, Integer> countNgrams(String[] words, int n) {
        Map<String, Integer> counts = new TreeMap<>();
        for (int i = 0; i < words.length - n + 1; i++) {
            String ngram = String.join("\t", Arrays.asList(Arrays.copyOfRange(words, i, i + n)));
            if (counts.get(ngram) == null) {
                counts.put(ngram, 1);
            } else {
                counts.put(ngram, counts.get(ngram) + 1);
            }
        }
        return counts;
    }
}
