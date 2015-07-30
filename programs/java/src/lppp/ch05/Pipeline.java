package lppp.ch05;

import java.io.IOException;
import java.util.*;


/**
 * Created by Pierre Nugues on 25/07/15.
 */
public class Pipeline {
    // Method borrowed from stack overflow
    public static <K, V extends Comparable<? super V>> Map<K, V> sortByValue(Map<K, V> map) {
        List<Map.Entry<K, V>> list = new LinkedList<>(map.entrySet());
        Collections.sort(list, new Comparator<Map.Entry<K, V>>() {
            public int compare(Map.Entry<K, V> o1, Map.Entry<K, V> o2) {
                return (o1.getValue()).compareTo(o2.getValue());
            }
        });

        Map<K, V> result = new LinkedHashMap<>();
        for (Map.Entry<K, V> entry : list) {
            result.put(entry.getKey(), entry.getValue());
        }
        return result;
    }

    public static void main(String[] args) throws IOException {
        FileReader reader = new FileReader();
        String text = reader.readFile(args[0]);
        //System.out.println(text);
        Tokenizer tokenizer = new Tokenizer();
        String[] words = tokenizer.tokenize(text);

        WordCounter counter = new WordCounter();
        Map<String, Integer> counts = counter.count(words);
        int total = 0;
        for (String word : counts.keySet()) {
            total += counts.get(word);
        }

        Pipeline pipeline = new Pipeline();
        Map<String, Integer> sortedCounts = pipeline.sortByValue(counts);
        for (String word : sortedCounts.keySet()) {
            System.out.println(word + ": " + counts.get(word));
        }
    }
}
