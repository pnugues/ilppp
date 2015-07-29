package lppp.ch02;

import java.io.File;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by Pierre Nugues on 28/07/15.
 */
public class regex02 {
    public static void main(String[] args) {
        Pattern pattern = Pattern.compile("ab+c");
        Scanner scan = new Scanner(System.in).useDelimiter("\\n");
        while (scan.hasNext()) {
            String line = scan.next();
            Matcher matcher = pattern.matcher(line);
            if (matcher.find()) {
                line = matcher.replaceAll("ABC");
                System.out.println(line);
            }
        }
    }
}
