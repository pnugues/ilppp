package guide;

import format.Word;
import wekaglue.WekaGlue;
import parser.ParserState;

/**
 *
 * @author Pierre Nugues
 */
public abstract class Guide {

    WekaGlue wekaModel;
    ParserState parserState;

    Guide(WekaGlue wekaModel, ParserState parserState) {
        this.wekaModel = wekaModel;
        this.parserState = parserState;
    }

    public abstract String predict();

    Features extractFeatures() {
        Features feats;
        String topPostagStack = "nil";
        String secondPostagStack = "nil";
        String secondPostagQueue = "nil";
        if (!parserState.stack.empty()) {
            topPostagStack = parserState.stack.peek().getPostag();
            Word temp = parserState.stack.pop();
            if (!parserState.stack.empty()) {
                secondPostagStack = parserState.stack.peek().getPostag();
            }
            parserState.stack.push(temp);
        }
        if (parserState.queue.size() > 1) {
            secondPostagQueue = parserState.queue.get(1).getPostag();
        }

        //feats = new Features(topPostagStack, queue.get(0).getPostag());
        //feats = new Features(topPostagStack, queue.get(0).getPostag(), canLeftArc(), canReduce());
        feats = new Features(topPostagStack, secondPostagStack, parserState.queue.get(0).getPostag(), secondPostagQueue, parserState.canLeftArc(), parserState.canReduce());
        return feats;
    }
}
