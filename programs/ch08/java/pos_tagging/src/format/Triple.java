package format;

/**
 * @author pierre
 */
public class Triple implements Comparable<Triple> {

    Pair pair;
    String third;

    public Triple(Pair pair, String third) {
        this.pair = pair;
        this.third = third;
    }

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        Pair pair = new Pair("DT", "JJ");
        Triple triple = new Triple(pair, "NN");
        System.out.println(triple);
    }

    public Pair getPair() {
        return pair;
    }

    public String getThird() {
        return third;
    }

    @Override
    public int compareTo(Triple second) {
        String firstS = this.pair + " " + this.third;
        String secondS = second.getPair() + " " + second.getThird();
        return firstS.compareTo(secondS);
    }

    @Override
    public String toString() {
        return this.pair + " " + this.third;
    }

}
