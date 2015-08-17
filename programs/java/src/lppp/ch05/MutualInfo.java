package lppp.ch05;

import java.io.IOException;
import java.util.Map;
import java.util.TreeMap;

/**
 * Created by Pierre Nugues on 29/07/15.
 */
public class MutualInfo {
    public static void main(String[] args) throws IOException {
        FileReader reader = new FileReader();
        String text = reader.readFile(args[0]);
        Tokenizer tokenizer = new Tokenizer();
        String[] words = tokenizer.tokenize(text);
        WordCounter wc = new WordCounter();
        Map<String, Integer> unigramCounts = wc.count(words);
        Map<String, Integer> bigramCounts = wc.countBigrams(words);

        MutualInfo mi = new MutualInfo();
        Map<String, Double> miScores = mi.compute(words.length, unigramCounts, bigramCounts);
        for (String bigram : miScores.keySet()) {
            String[] pair = bigram.split("\t");
            System.out.println(miScores.get(bigram) + "\t" + bigram + "\t" + bigramCounts.get(bigram) + "\t" + unigramCounts.get(pair[0]) + "\t" + unigramCounts.get(pair[1]));
        }
    }

    Map<String, Double> compute(int N, Map<String, Integer> unigramCounts, Map<String, Integer> bigramCounts) {
        Map<String, Double> miScores = new TreeMap<>();

        for (String bigram : bigramCounts.keySet()) {
            String[] pair = bigram.split("\t");
            double mi = Math.log((double) N * bigramCounts.get(bigram) / (unigramCounts.get(pair[0]) * unigramCounts.get(pair[1]))) / Math.log(2.0);
            miScores.put(bigram, mi);
        }
        return miScores;
    }
}
