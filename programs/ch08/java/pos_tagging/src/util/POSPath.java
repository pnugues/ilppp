package util;

import format.Pair;

import java.util.ArrayList;
import java.util.List;

/**
 * @author pierre
 */
public class POSPath implements Comparable<POSPath> {

    List<String> path;
    double logprob;

    public POSPath(String start, double prob) {
        path = new ArrayList<>();
        path.add(start);
        this.logprob = Math.log10(prob);
    }

    public POSPath(POSPath path) {
        this.path = new ArrayList<>(path.getPath());
        this.logprob = path.getProb();
    }

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
    }

    public List<String> getPath() {
        return path;
    }

    public double getProb() {
        return logprob;
    }

    public void addPOS(String pos) {
        path.add(pos);
    }

    public String getLastPOS() {
        return path.get(path.size() - 1);
    }

    public Pair getLastPOSBigram() {
        if (path.size() >= 2) {
            return new Pair(path.get(path.size() - 2), path.get(path.size() - 1));
        } else {
            return new Pair("<s>", path.get(path.size() - 1));
        }
    }

    public void probMult(double term) {
        logprob += Math.log10(term);
    }

    @Override
    public int compareTo(POSPath path) {
        Double probD = logprob;
        return probD.compareTo(path.getProb());
    }

    @Override
    public String toString() {
        return path.toString() + " " + logprob;
    }

}
