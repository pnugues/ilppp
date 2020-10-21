class HMMProb:
    (lambda1_trigram, lambda2_trigram, lambda3_trigram) = (0.1, 0.2, 0.7)
    (lambda1_bigram, lambda2_bigram) = (0.2, 0.8)

    def __init__(self, cnt):
        self.POS_cnts = cnt.POS_cnts
        self.POS_bigram_cnts = cnt.POS_bigram_cnts
        self.pos_trigram_cnts = cnt.POS_trigram_cnts
        self.word_POS_cnts = cnt.word_POS_cnts
        self.unk_POS_cnts = cnt.unk_POS_cnts
        self.token_cnt = cnt.token_cnt

    # Bigrams: P(w_i | t_i) x P(t_i | t_{i - 1})
    def compute_bi(self, word, prev_pos, pos):
        # First term
        tag_cnt = self.POS_cnts.get(pos, 0)
        if pos in self.unk_POS_cnts:  # to have a prob sum equals to 1.
            tag_cnt += self.unk_POS_cnts[pos]

        if word not in self.word_POS_cnts:  # UNK word
            # firstTerm = 0.02; // This value is not meaningful
            first_term = self.unk_POS_cnts.get(pos) / tag_cnt
        else:
            pair_cnt = self.word_POS_cnts[word].get(pos)
            first_term = pair_cnt / tag_cnt

        # Second term
        prev_tag_cnt = self.POS_cnts.get(prev_pos)
        tag_bigram = (prev_pos, pos)
        if tag_bigram not in self.POS_bigram_cnts:
            # Backoff
            second_term = self.lambda1_bigram * tag_cnt / self.token_cnt
            # secondTerm = (double) 1.0/(double) prevTagFreq;
        else:
            tag_bigram_cnt = self.POS_bigram_cnts[tag_bigram]
            second_term = self.lambda1_bigram * tag_cnt / self.token_cnt
            second_term += self.lambda2_bigram * tag_bigram_cnt / prev_tag_cnt
        # System.out.println(pairFreq + "\t" + tagFreq + "\t" + prevTagFreq + "\t" + tagBigramFreq);
        return first_term * second_term

    # P(w_i | t_i) x P(t_i | t_{i - 2}, t_{i - 1})
    def compute_tri(self, word, prev_bigram, pos):
        # First term
        tag_cnt = self.POS_cnts.get(pos, 0)
        # to have a prob sum equals to 1.
        if pos in self.unk_POS_cnts:
            tag_cnt += self.unk_POS_cnts[pos]

        if word not in self.word_POS_cnts:  # UNK word
            # first_term = 0.02; // This value is not meaningful
            first_term = self.unk_POS_cnts.get(pos) / tag_cnt
        else:
            pair_cnt = self.word_POS_cnts[word].get(pos, 0)
            first_term = pair_cnt / tag_cnt

        # Second term
        tag_trigram = (prev_bigram[0], prev_bigram[1], pos)
        tag_bigram = (prev_bigram[1], pos)
        if tag_trigram not in self.pos_trigram_cnts and tag_bigram not in self.POS_bigram_cnts:
            # Backoff
            second_term = self.lambda1_trigram * tag_cnt / self.token_cnt
            # secondTerm = (double) 1.0/(double) prevTagFreq;
        elif tag_trigram not in self.pos_trigram_cnts and tag_bigram in self.POS_bigram_cnts:
            second_term = self.lambda1_trigram * tag_cnt / self.token_cnt
            second_term += self.lambda2_trigram * \
                           self.POS_bigram_cnts[tag_bigram] / \
                           self.POS_cnts[tag_bigram[0]]
        else:
            second_term = self.lambda1_trigram * tag_cnt / self.token_cnt
            second_term += self.lambda2_trigram * \
                           self.POS_bigram_cnts[tag_bigram] / \
                           self.POS_cnts[tag_bigram[0]]
            second_term += self.lambda3_trigram * \
                           self.pos_trigram_cnts[tag_trigram] / \
                           self.POS_bigram_cnts[prev_bigram]
        return first_term * second_term

    def set_lambdas_bi(self, lambda1, lambda2):
        self.lambda1_bigram = lambda1
        self.lambda2_bigram = lambda2

    def set_lambdas_tri(self, lambda1, lambda2, lambda3):
        self.lambda1_trigram = lambda1
        self.lambda2_trigram = lambda2
        self.lambda3_trigram = lambda3
