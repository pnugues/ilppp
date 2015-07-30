package lppp.ch05;

import java.io.IOException;
import java.util.*;

/**
 * Created by Pierre Nugues on 30/07/15.
 */
public class Pipeline {
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
        Pipeline pipeline = new Pipeline();
        Map<String, Integer> sortedCounts = pipeline.sortByValue(wordCounts);
        for (String word : sortedCounts.keySet()) {
            System.out.println(word + ": " + wordCounts.get(word));
        }
    }

    // Method borrowed from stack overflow
    public static <K, V extends Comparable<? super V>> Map<K, V> sortByValue(Map<K, V> map) {
        List<Map.Entry<K, V>> list = new LinkedList<Map.Entry<K, V>>(map.entrySet());
        Collections.sort(list, new Comparator<Map.Entry<K, V>>() {
            public int compare(Map.Entry<K, V> o1, Map.Entry<K, V> o2) {
                return (o1.getValue()).compareTo(o2.getValue());
            }
        });

        Map<K, V> result = new LinkedHashMap<K, V>();
        for (Map.Entry<K, V> entry : list) {
            result.put(entry.getKey(), entry.getValue());
        }
        return result;
    }

}
