package lppp.ch02;

import java.io.File;
import java.io.IOException;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by Pierre Nugues on 28/07/15.
 */
public class concord {
    public static void main(String[] args) throws IOException {
        String file = args[0];
        String pattern = args[1];
        int width = new Integer(args[2]);
        String text = new Scanner(new File(file)).useDelimiter("\\Z").next();
        text.replaceAll("\\s+", " ");
        String concRegex = String.format("(.{0,%s}%s.{0,%s})", width, pattern, width);
        //System.out.println(concRE);
        Pattern concPattern = Pattern.compile(concRegex);
        Matcher matcher = concPattern.matcher(text);
        while (matcher.find()) {
            System.out.println(matcher.group());
        }
    }
}