import random, re

SEP = " " # token separator symbol

def make_ngrams(tokens, N):
    """ Returns a list of N-long ngrams from a list of tokens """

    ngrams = []
    for i in range(len(tokens)-N+1):
        ngrams.append(tokens[i:i+N])
    return ngrams


# Extracs necessary data from our preprocessed string
# Relative frequency is not taken into account given we are using a trigram
# model on a research paper
# Returns dict of dict named counts
# where counts[a][b] = p(b follows a | a)
def get_ngram_data(ngrams):
    counts = {}

    for ngram in ngrams:
        token_seq  = SEP.join(ngram[:-1])
        last_token = ngram[-1]

        if token_seq not in counts:
            counts[token_seq] = {};

        if last_token not in counts[token_seq]:
            counts[token_seq][last_token] = 0;

        counts[token_seq][last_token] += 1;

    return counts;


def next_word(text, N, counts):
    """ Outputs the next word to add by using most recent tokens """

    token_seq = SEP.join(text.split()[-(N-1):]);
    choices = counts[token_seq].items();

    # [see http://stackoverflow.com/a/3679747/2023516]
    total = sum(weight for choice, weight in choices)
    r = random.uniform(0, total)
    upto = 0
    for choice, weight in choices:
        upto += weight;
        if upto > r: return choice
    assert False                            # should not reach here


def preprocess_corpus(filename):
    s = open(filename, 'r').read()
    s = re.sub('[()]', r'', s)                              # remove certain punctuation chars
    s = re.sub('([.-])+', r'\1', s)                         # collapse multiples of certain chars
    s = re.sub('([^0-9])([.,!?])([^0-9])', r'\1 \2 \3', s)  # pad sentence punctuation chars with whitespace
    s = ' '.join(s.split()).lower()                         # remove extra whitespace (incl. newlines)
    return s;


def postprocess_output(s):
    s = re.sub('\\s+([.,!?])\\s*', r'\1 ', s)                       # correct whitespace padding around punctuation
    s = s.capitalize();                                             # capitalize first letter
    s = re.sub('([.!?]\\s+[a-z])', lambda c: c.group(1).upper(), s) # capitalize letters following terminated sentences
    return s


def gengram_sentence(corpus, N=3, sentence_count=5, start_seq=None):
    """ Generate a random sentence based on input text corpus """

    ngrams = make_ngrams(corpus.split(SEP), N)
    counts = get_ngram_data(ngrams)

    if start_seq is None: start_seq = random.choice(counts.keys());
    rand_text = start_seq.lower();

    sentences = 0;
    while sentences < sentence_count:
        rand_text += SEP + next_word(rand_text, N, counts);
        sentences += 1 if rand_text.endswith(('.','!', '?')) else 0

    return postprocess_output(rand_text);


if __name__ == "__main__":
    corpus = preprocess_corpus("concatTXT.txt")
    print gengram_sentence(corpus, start_seq = "Our enumeration")