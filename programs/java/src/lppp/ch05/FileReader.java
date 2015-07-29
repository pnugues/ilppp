package lppp.ch05;

import java.io.File;
import java.io.IOException;
import java.util.Scanner;

/**
 * Created by Pierre Nugues on 25/07/15.
 */
public class FileReader {
    String readFile(String file) throws IOException {
        String text = new Scanner(new File(file)).useDelimiter("\\Z").next();
        return text;
    }
}
