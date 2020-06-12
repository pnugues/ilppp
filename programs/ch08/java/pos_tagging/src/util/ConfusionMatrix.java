package util;

import format.Word;

import java.util.List;
import java.util.Map;
import java.util.TreeMap;

/**
 * @author pierre
 */
public class ConfusionMatrix {

    List<List<Word>> sentenceList;
    Map<String, Map<String, Integer>> confMat;

    public ConfusionMatrix(List<List<Word>> sentenceList) {
        this.sentenceList = sentenceList;
        confMat = new TreeMap<>();
    }

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
    }

    public float computeAccuracy() {
        int correct = 0, error = 0;
        for (List<Word> sentence : sentenceList) {
            for (int i = 1; i < sentence.size() - 1; i++) { // Skipping the ROOT index
                Word word = sentence.get(i);
                if (word.getPos().equals(word.getPpos())) {
                    correct++;
                } else {
                    error++;
                }
            }
        }
        return (float) correct / (float) (correct + error);
    }

    public Map<String, Map<String, Integer>> computeMatrix() {
        for (List<Word> sentence : sentenceList) {
            for (int i = 1; i < sentence.size() - 1; i++) { // Skipping the ROOT index
                Word word = sentence.get(i);
                if (confMat.get(word.getPos()) != null) {
                    if (confMat.get(word.getPos()).get(word.getPpos()) != null) {
                        int count = confMat.get(word.getPos()).get(word.getPpos());
                        count++;
                        confMat.get(word.getPos()).put(word.getPpos(), count);
                    } else {
                        confMat.get(word.getPos()).put(word.getPpos(), 1);
                    }
                } else {
                    Map<String, Integer> elem = new TreeMap<>();
                    elem.put(word.getPpos(), 1);
                    confMat.put(word.getPos(), elem);
                }
            }
        }
        System.out.println(confMat);
        return confMat;
    }

    public void print() {
        System.out.print("\t");
        for (String pos : confMat.keySet()) {
            System.out.print(pos + "\t");
        }
        System.out.println();
        for (String pos : confMat.keySet()) {
            System.out.print(pos + "\t");
            for (String ppos : confMat.keySet()) {
                if (confMat.get(pos).get(ppos) == null) {
                    System.out.print("0\t");
                } else {
                    System.out.print(confMat.get(pos).get(ppos) + "\t");
                }
            }
            System.out.println();
        }
    }

}
