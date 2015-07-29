package lppp.ch02;

import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by Pierre Nugues on 28/07/15.
 */
public class regex06 {
    public static void main(String[] args) {
        Pattern pattern = Pattern.compile("\\$ *([0-9]+)\\.?([0-9]*)");
        Scanner scan = new Scanner(System.in).useDelimiter("\\n");
        while (scan.hasNext()) {
            String line = scan.next();
            Matcher matcher = pattern.matcher(line);
            if (matcher.find()) {
                line = matcher.replaceAll("$1 dollars and $2 cents");
                System.out.println(line);
                //System.out.println(line.replaceAll("\\$ *([0-9]+)\\.?([0-9]*)", "$1 dollars and $2 cents"));
            }
        }
    }
}
