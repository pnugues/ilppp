package parser;

/**
 *
 * @author Pierre Nugues
 */
import java.util.*;
import format.Word;

public class ParserState {

    public Stack<Word> stack;
    public List<Word> queue;
    List<Word> wordList;
    List<String> transitionList;
    List<Word> depGraph;

    ParserState(List<Word> wordList) {
        this.stack = new Stack<Word>();
        this.queue = new ArrayList<Word>(wordList);
        this.wordList = new ArrayList<Word>(wordList);
        this.depGraph = new ArrayList<Word>();
        this.transitionList = new ArrayList<String>();
    }

    public void doLeftArc(String deprel) {
        stack.peek().setHead(queue.get(0).getId());
        stack.peek().setDeprel(deprel);
        depGraph.add(stack.pop());
    }

    public void doRightArc(String deprel) {
        queue.get(0).setHead(stack.peek().getId());
        queue.get(0).setDeprel(deprel);
        depGraph.add(queue.get(0));
        stack.push(queue.remove(0));
    }

    public void doReduce() {
        stack.pop();
    }

    public void doShift() {
        stack.push(queue.remove(0));
    }

    public boolean canLeftArc() {
        boolean canLeftArc = true;
        if (stack.empty()) {
            return false;
        }
        // Constraint: top of the stack has no head in the graph
        // This means that it is not already in the graph.
        for (int i = 0; i < depGraph.size(); i++) {
            if (depGraph.get(i).getId() == stack.peek().getId()) {
                canLeftArc = false;
                break;
            }
        }
        return canLeftArc;
    }

    public boolean canReduce() {
        boolean canReduce = false;
        if (stack.empty()) {
            return false;
        }

        // Constraint: top of the stack has a head somewhere is the graph
        // This guarantees that the graph is connected
        // Here this means that it is already in the graph
        for (int i = 0; i < depGraph.size(); i++) {
            if (depGraph.get(i).getId() == stack.peek().getId()) {
                canReduce = true;
                break;
            }
        }
        return canReduce;
    }

    public void addTransition(String transition) {
        transitionList.add(transition);
    }

    // Sets the root as head to words remaining in the stack that have no head
    public void doReduceAndSetRoot() {
        stack.peek().setHead(0);
        stack.peek().setDeprel("ROOT");
        depGraph.add(stack.pop());
    }
}
