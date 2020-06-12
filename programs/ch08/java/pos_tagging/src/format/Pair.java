package format;

/**
 * @author pierre
 */
public class Pair implements Comparable<Pair> {

    String first;
    String second;

    public Pair(String first, String second) {
        this.first = first;
        this.second = second;
    }

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
    }

    public String getFirst() {
        return first;
    }

    public void setFirst(String first) {
        this.first = first;
    }

    public String getSecond() {
        return second;
    }

    public void setSecond(String second) {
        this.second = second;
    }

    @Override
    public int hashCode() {
        return (this.first.hashCode() ^ this.second.hashCode());
    }

    @Override
    public boolean equals(Object secondO) {
        if (!(secondO instanceof Pair)) {
            return false;
        }
        Pair second = (Pair) secondO;
        String firstS = this.first + " " + this.second;
        String secondS = second.getFirst() + " " + second.getSecond();
        return firstS.equals(secondS);
    }

    @Override
    public int compareTo(Pair second) {
        String firstS = this.first + " " + this.second;
        String secondS = second.getFirst() + " " + second.getSecond();
        return firstS.compareTo(secondS);
    }

    @Override
    public String toString() {
        return this.first + " " + this.second;
    }
}
