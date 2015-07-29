package lppp.ch05;

import java.util.Map;
import java.util.TreeMap;

/**
 * Created by Pierre Nugues on 25/07/15.
 */
public class WordCounter {
    Map<String, Integer> count(String [] words) {
        TreeMap<String, Integer> counts = new TreeMap<>();
        for (String word: words) {
            if (counts.get(word) == null) {
                counts.put(word, 1);
            } else {
                counts.put(word, counts.get(word) + 1);
            }
        }
        return counts;
    }
}
