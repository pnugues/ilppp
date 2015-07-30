package lppp.ch05;

import java.io.IOException;
import java.util.*;


/**
 * Created by Pierre Nugues on 25/07/15.
 */
public class LanguageModel {

    public static void main(String[] args) throws IOException {
        String sentence = "<s> det var en gång en katt som hette nils </s>";
        FileReader reader = new FileReader();
        String text = reader.readFile(args[0]);
        //System.out.println(text);
        Tokenizer tokenizer = new Tokenizer();
        Splitter splitter = new Splitter(tokenizer);
        String[] sentences = splitter.split(text);

        StringBuffer textBuffer = new StringBuffer();
        for (String sent : sentences) {
            textBuffer.append(sent + " ");
        }
        String tokenizedText = textBuffer.toString().trim();
        //System.out.println(tokenizedText);
        String[] words = tokenizedText.split("( |\n)+");
        WordCounter counter = new WordCounter();
        Map<String, Integer> counts = counter.count(words);
        int total = 0;
        for (String word : counts.keySet()) {
            total += counts.get(word);
        }
        BigramCounter bigramCounter = new BigramCounter();
        Map<String, Integer> bigramCounts = bigramCounter.count(words);
        LanguageModel pipeline = new LanguageModel();
        String[] swords = sentence.split("\\s");
        System.out.println("============================================");
        System.out.println("wi" + "\t" + "C(wi)" + "\t" + "#words" + "\t" + "P(wi)");
        System.out.println("============================================");
        double probability = 1.0;
        for (int i = 1; i < swords.length; i++) {
            System.out.println(swords[i] + "\t" + counts.get(swords[i]) + "\t" + total + "\t" + (float) counts.get(swords[i]) / (float) total);
            probability *= (float) counts.get(swords[i]) / (float) total;
        }
        System.out.println("============================================");
        double entropy = -Math.log(probability) / Math.log(2.0) / (float) (swords.length - 1);
        double perplexity = Math.pow(2.0, entropy);
        System.out.println("Probability: " + probability + "\tEntropy rate: " + entropy + "\tPerplexity: " + perplexity + "\n\n");

        System.out.println("============================================");
        System.out.println("wi" + "\t" + "wi+1" + "\t" + "Ci,i+1" + "\t" + "C(i)" + "\t" + "P(wi+1|wi)");
        System.out.println("============================================");
        double probabilityBig = 1.0;

        for (int i = 0; i < swords.length - 1; i++) {
            if (bigramCounts.get(swords[i] + "\t" + swords[i + 1]) != null) {
                System.out.println(swords[i] + "\t" + swords[i + 1] + "\t" + bigramCounts.get(swords[i] + "\t" + swords[i + 1]) + "\t" + counts.get(swords[i]) + "\t" + (float) bigramCounts.get(swords[i] + "\t" + swords[i + 1]) / (float) counts.get(swords[i]));
                probabilityBig *= (float) bigramCounts.get(swords[i] + "\t" + swords[i + 1]) / (float) counts.get(swords[i]);
            } else {
                System.out.println(swords[i] + "\t" + swords[i + 1] + "\t" + 0 + "\t" + counts.get(swords[i]) + "\t*back-off: " + (float) counts.get(swords[i + 1]) / (float) total);
                probabilityBig *= (float) counts.get(swords[i + 1]) / (float) total;
            }

        }
        System.out.println("============================================");
        double entropyBig = -Math.log(probabilityBig) / Math.log(2.0) / (float) (swords.length - 1);
        double perplexityBig = Math.pow(2.0, entropyBig);
        System.out.println("Probabilty: " + probabilityBig + "\tEntropy rate: " + entropyBig + "\tPerplexity: " + perplexityBig + "\n\n");
    }
}
