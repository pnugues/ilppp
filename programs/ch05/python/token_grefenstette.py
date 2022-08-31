"""
Tokenization program by Gregory Grefenstette.
In Hans Van Halteren ed., Syntactic Wordclass Tagging, (Text, Speech & Language Technology S.)
Kluwer Academic Publishers 1999.
Translated and slightly modified from nawk into Python by Pierre Nugues
"""
__author__ = "Pierre Nugues"

import regex as re
import sys

letter = r"[\p{L}']"
not_letter = r"[^\p{L}'0-9]"
always_sep = r"[?!()\";/\\|,`]"
begin_sep = r"['&]"
end_sep = "('|:|-|'S|'D|'M|'LL|'RE|'VE|N'T|'s|'d|'m|'ll|'re|'ve|n't)"
abbr = {"Co.": 1, "Corp.": 1, "vs.": 1, "e.g.": 1,
        "etc.": 1, "ex.": 1, "cf.": 1, "eg.": 1,
        "Jan.": 1, "Feb.": 1, "Mar.": 1, "Apr.": 1,
        "Jun.": 1, "Jul.": 1, "Aug.": 1, "Sept.": 1,
        "Oct.": 1, "Nov.": 1, "Dec.": 1,
        "jan.": 1, "feb.": 1, "mar.": 1, "apr.": 1,
        "jun.": 1, "jul.": 1, "aug.": 1, "sept.": 1,
        "oct.": 1, "nov.": 1, "dec.": 1,
        "ed.": 1, "eds.": 1, "repr.": 1, "trans.": 1,
        "vol.": 1, "vols.": 1, "rev.": 1, "est.": 1,
        "b.": 1, "m.": 1, "bur.": 1, "d.": 1, "r.": 1,
        "M.": 1, "Dept.": 1, "MM.": 1, "U.": 1,
        "Mr.": 1, "Jr.": 1, "Ms.": 1, "Mme.": 1, "Mrs.": 1,
        "Dr.": 1}


def tokenize(text):
    # This line changes tabs into spaces
    text = re.sub(r"\t", " ", text)
    # put blanks around characters that are unambiguous separators
    text = re.sub(always_sep, r" \g<0> ", text)
    # if a word is a separator in the beginning of a token separate it here
    text = re.sub("^" + begin_sep, r"\g<0> ", text)
    text = re.sub(" " + begin_sep, r"\g<0> ", text)
    text = re.sub("(" + not_letter + ")(" + begin_sep + ")", r"\1 \2", text)
    # idem for final separators
    text = re.sub(end_sep + r"\s", r" \g<0>", text)
    text = re.sub(end_sep + "(" + not_letter + ")", r"\1 \2",
                  text)  # the end separator is already between parentheses and is stored in $1

    # This line divides the input line and assigns it to elements of an array
    all_words = text.split()
    words = []
    # We examine all the elements
    for word in all_words:
        # if it contains a letter followed by a period,
        if re.search(letter + r"\.", word):
            # we see if it is an abbreviation
            # if it is explicitly found in the abbreviation list
            if word not in abbr:
                # or matches the regular expression below, we keep the period attached (possible acronyms)
                if not re.search(r"^(\p{L}\.(\p{L}\.)+|\p{Lu}[bcdfghj-np-tvxz]+\.)$", word):
                    # if not, a space is inserted before the period
                    word = re.sub(r"\.$", r" .", word)
        # Change all spaces to new lines
        word = re.sub(r"[ \t]+", r"\n", word)
        # Append the current word
        words.append(word)
    return words


if __name__ == '__main__':
    for line in sys.stdin:
        words = tokenize(line)
        for word in words:
            print(word)