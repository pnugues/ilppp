# This program counts the unigrams and the bigrams
# Author Pierre Nugues
# 2003-2012

@sentence = ("<s>", "a", "good", "deal", "of", "the", "literature", "of", "the", "past", "was", "indeed", "already", "being", "transformed", "in", "this", "way", "</s>");

$text = <>;
while ($line = <>) { 
   $text .= $line;
}

@words = split(/\s+/, $text);
for ($i = 0; $i <= $#words; $i++) {
	if (!exists($frequency{$words[$i]})) {
		$frequency{$words[$i]} = 1;
	} else {
		$frequency{$words[$i]}++;
	}
}

# Basic stats.
print "#words: ", $#words, "\n";
$count_unigrams = keys %frequency;
print "ngram 1: ", $count_unigrams, "\n";

$count_nohapax = 0;
foreach $word (sort keys %frequency){
        if ($frequency{$word} > 1) {
                $count_nohapax++;
        }
#	print "$frequency{$word} $word\n";
}
print "ngram 1, no hapax: ", $count_nohapax, "\n";

for ($i = 0; $i < $#words; $i++) {
	$bigrams[$i] = $words[$i] . " " . $words[$i + 1];
}
for ($i = 0; $i < $#words; $i++) {
	if (!exists($frequency_bigrams{$bigrams[$i]})) {
		$frequency_bigrams{$bigrams[$i]} = 1;
	} else {
		$frequency_bigrams{$bigrams[$i]}++;
	}
}

$count_bigrams = keys %frequency_bigrams;
print "ngram 2: ", $count_bigrams, "\n";

$count_bi_nohapax = 0;
foreach $word (sort keys %frequency_bigrams){
        if ($frequency_bigrams{$word} > 1) {
                $count_bi_nohapax++;
        }
#	print "$frequency_bigrams{$word} $word\n";
}
print "ngram 2: no hapax: ", $count_bi_nohapax, "\n";
print "\n";

foreach $bigram (sort keys %frequency_bigrams){
#	print "$frequency_bigrams{$bigram} $bigram \n";
}

# Unigram probability
print "Computing unigram likelihood:\n";
$unigram_likelihood = 1;
print "Frequency <s>: ", $frequency{"<s>"}, ", other words: ", $#words - $frequency{"<s>"}, "\n";

for ($i = 1; $i <= $#sentence; $i++) {
    $unigram = $sentence[$i];
    if (exists($frequency{$unigram})) {
		print $unigram, "\t", $frequency{$unigram}, "\t", $frequency{$unigram}/($#words - $frequency{"<s>"}), "\n";
		$unigram_likelihood *= $frequency{$unigram}/($#words - $frequency{"<s>"});
    } else {
		print $unigram, "\t", 0, "\t" , 0.0, "\n";
		$unigram_likelihood *= 0.0;
    }
}
print "unigram_likelihood: ", $unigram_likelihood, "\n";
print "\n";

#Bigram likelihood using raw counts
print "Computing bigram likelihood:\n";

$bigram_likelihood = 1;
for ($i = 0; $i < $#sentence; $i++) {
    $bigram = $sentence[$i]. " " .  $sentence[$i+1];
    if (exists($frequency_bigrams{$bigram})) {
		print $bigram, "\t\t", $frequency_bigrams{$bigram}, "\t", $frequency_bigrams{$bigram}/$frequency{$sentence[$i]}, "\n";
		$bigram_likelihood *= $frequency_bigrams{$bigram}/$frequency{$sentence[$i]};
    } else {
		print $bigram, "\t", 0 , "\t", 0.0, "\n";
		$bigram_likelihood *= 0.0;
    }
}

print "bigram_likelihood using raw counts: ", $bigram_likelihood, "\n\n";

print "Computing bigram likelihood using Laplace:\n";
$bigram_lap_likelihood = 1;
for ($i = 0; $i < $#sentence; $i++) {
    $bigram = $sentence[$i]. " " .  $sentence[$i+1];
    if (exists($frequency_bigrams{$bigram})) {
		print $bigram, "\t\t", $frequency_bigrams{$bigram} + 1, "\t", ($frequency_bigrams{$bigram} + 1)/($frequency{$sentence[$i]} + $count_unigrams - 1), "\n";
		$bigram_lap_likelihood *= ($frequency_bigrams{$bigram} + 1)/($frequency{$sentence[$i]} + $count_unigrams - 1);
    } else {
		print $bigram, "\t\t", 1, "\t", 1/($frequency{$sentence[$i]} + $count_unigrams - 1), "\n";
		$bigram_lap_likelihood *= 1/($frequency{$sentence[$i]} + $count_unigrams - 1);
    }	
}
print "bigram_likelihood_laplace: ", $bigram_lap_likelihood, "\n\n";


# Computing the reestimated frequencies
print "Computing reestimated frequencies using Good Turing:\n";

$count_bigrams = keys %frequency_bigrams;
print "ngram 2: ", $count_bigrams, "\n";
$freq_freq[0] = $count_unigrams * $count_unigrams - $count_bigrams;
print "Frequency of frequency:\t", 0, "\t", $freq_freq[0];
for ($i = 1; $i <= 10; $i++) {
    $count_count = 0;
    foreach $word (sort keys %frequency_bigrams){
        if ($frequency_bigrams{$word} == $i) {
	    $count_count++;
        }
    }
    $freq_freq[$i] = $count_count;
    $gt_discount[$i] = $i*$freq_freq[$i]/$freq_freq[$i - 1];
    print "\t", $gt_discount[$i], "\n";
    print "Frequency of frequency:\t", $i, "\t", $freq_freq[$i];
}
print "\n\n";

print "Computing bigram likelihood using Good Turing:\n";
$bigram_gt_likelihood = 1;
for ($i = 0; $i < $#sentence; $i++) {
    $bigram = $sentence[$i]. " " .  $sentence[$i+1];
    if (exists($frequency_bigrams{$bigram})) {
       if ($frequency_bigrams{$bigram} < 10) {
	print $bigram, "\t\t", $frequency_bigrams{$bigram}, "\t", $gt_discount[$frequency_bigrams{$bigram} + 1]/$frequency{$sentence[$i]}, "\n";
	$bigram_gt_likelihood *= $gt_discount[$frequency_bigrams{$bigram} + 1]/$frequency{$sentence[$i]};
     } else {
	print $bigram, "\t\t", $frequency_bigrams{$bigram}, "\t", $frequency_bigrams{$bigram}/$frequency{$sentence[$i]}, "\n";
	$bigram_gt_likelihood *= $frequency_bigrams{$bigram}/$frequency{$sentence[$i]};
     }
    } else {
	print $bigram, "\t\t", 0, "\t", $gt_discount[1]/$frequency{$sentence[$i]}, "\n";
	$bigram_gt_likelihood *= $gt_discount[1]/$frequency{$sentence[$i]};
    }	
}
print "bigram_likelihood_good_turing: ", $bigram_gt_likelihood, "\n\n";

#Bigram likelihood using deleted interpolation
$lambda1 = 0.3;
$lambda2 = 0.7;
$bigram_di_likelihood = 1.0;
for ($i = 0; $i < $#sentence; $i++) {
    $bigram = $sentence[$i]. " " .  $sentence[$i+1];
    $unigram = $sentence[$i+1];
	print $bigram, "\t\t", $frequency_bigrams{$bigram}, "\t", $frequency{$unigram}, "\t", $frequency_bigrams{$bigram}/$frequency{$sentence[$i]}, "\t", $frequency{$unigram}/($#words - $frequency{"<s>"}), "\t", $lambda1 * $frequency{$unigram}/($#words - $frequency{"<s>"}) + $lambda2 * $frequency_bigrams{$bigram}/$frequency{$sentence[$i]}, "\n";
	$bigram_di_likelihood *= $lambda1 * $frequency{$unigram}/($#words - $frequency{"<s>"}) + $lambda2 * $frequency_bigrams{$bigram}/$frequency{$sentence[$i]};
}
print "bigram_likelihood_deleted_interpolation: ", $bigram_di_likelihood, "\n\n";

#Bigram likelihood using backoff
print "Computing bigram likelihood with simple backoff:\n";

$bigram_backoff_likelihood = 1;
for ($i = 0; $i < $#sentence; $i++) {
    $bigram = $sentence[$i]. " " .  $sentence[$i+1];
    $unigram = $sentence[$i+1];
    if (exists($frequency_bigrams{$bigram})) {
		print $bigram, "\t\t", $frequency_bigrams{$bigram}, "\t", $frequency_bigrams{$bigram}/$frequency{$sentence[$i]}, "\n";
		$bigram_backoff_likelihood *= $frequency_bigrams{$bigram}/$frequency{$sentence[$i]};
    } else {
		print $bigram, "\t", 0 , "\t", "backing off", "\t", $frequency{$unigram}/($#words - $frequency{"<s>"}),"\n";
		$bigram_backoff_likelihood *= $frequency{$unigram}/($#words - $frequency{"<s>"});
    }
}
print "bigram_likelihood_backoff: ", $bigram_backoff_likelihood, "\n\n";


