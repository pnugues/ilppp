package pos_tagging;

import format.Word;

import java.util.List;

/**
 * @author pierre
 */
public interface POSTagger {
    double tag(List<Word> sentence);
}
