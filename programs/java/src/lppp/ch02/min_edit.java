package lppp.ch02;

import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by Pierre Nugues on 28/07/15.
 */
public class min_edit {
    public static void main(String[] args) {
        String source = args[0];
        String target = args[1];
        int length_s = source.length();
        int length_t = target.length();

        int[][] table = new int[length_s + 1][length_t + 1];

        // Initialize first row and column
        for (int i = 0; i <= length_s; i++) {
            table[i][0] = i;
        }
        for (int j = 0; j <= length_t; j++) {
            table[0][j] = j;
        }

        String[] source_char = source.split("");
        String[] target_char = target.split("");
        // Fills the table. Start index of rows and columns is 1
        for (int i = 1; i <= length_s; i++) {
            for (int j = 1; j <= length_t; j++) {
                // Is it a copy or a substitution?
                int cost = source_char[i - 1].equals(target_char[j - 1]) ? 0 : 2;
                // Computes the minimum
                int min = table[i - 1][j - 1] + cost;
                if (min > table[i][j - 1] + 1) {
                    min = table[i][j - 1] + 1;
                }
                if (min > table[i - 1][j] + 1) {
                    min = table[i - 1][j] + 1;
                }
                table[i][j] = min;
            }
        }

        for (int j = 0; j <= length_t; j++) {
            for (int i = 0; i <= length_s; i++) {
                System.out.print(table[i][j] + " ");
            }
            System.out.println();
        }
        System.out.println("Minimum distance: " + table[length_s][length_t]);
    }
}
