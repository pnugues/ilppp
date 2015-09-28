package guide;

/**
 *
 * @author Pierre Nugues
 */
// This class stores the features of the parser state
public class Features {

    String topPostagStack;
    String secondPostagStack;
    String firstPostagQueue;
    String secondPostagQueue;
    boolean canLA;
    boolean canRE;

    public Features(String topPostagStack, String firstPostagQueue) {
        this.topPostagStack = topPostagStack;
        this.firstPostagQueue = firstPostagQueue;
    }

    public Features(String topPostagStack, String firstPostagQueue, boolean canLA, boolean canRE) {
        this.topPostagStack = topPostagStack;
        this.firstPostagQueue = firstPostagQueue;
        this.canLA = canLA;
        this.canRE = canRE;
    }

    public Features(String topPostagStack, String secondPostagStack, String firstPostagQueue, String secondPostagQueue, boolean canLA, boolean canRE) {
        this.topPostagStack = topPostagStack;
        this.secondPostagStack = secondPostagStack;
        this.firstPostagQueue = firstPostagQueue;
        this.secondPostagQueue = secondPostagQueue;
        this.canLA = canLA;
        this.canRE = canRE;
    }

    public String getTopPostagStack() {
        return topPostagStack;
    }

    public String getSecondPostagStack() {
        return secondPostagStack;
    }

    public void setTopPostagStack(String topPostagStack) {
        this.topPostagStack = topPostagStack;
    }

    public String getFirstPostagQueue() {
        return firstPostagQueue;
    }

    public String getSecondPostagQueue() {
        return secondPostagQueue;
    }

    public void setFirstPostagQueue(String firstPostagQueue) {
        this.firstPostagQueue = firstPostagQueue;
    }

    public boolean getCanLA() {
        return canLA;
    }

    public void setCanLA(boolean canLA) {
        this.canLA = canLA;
    }

    public boolean getCanRE() {
        return canRE;
    }

    public void setCanRE(boolean canRE) {
        this.canRE = canRE;
    }
}
