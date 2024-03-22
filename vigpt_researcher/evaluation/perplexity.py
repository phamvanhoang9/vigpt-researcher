from collections import defaultdict 
import numpy as np


def bigram_model(refs):
    bigram = defaultdict(lambda: defaultdict(int))
    for ref in refs:
        words = ref.split()
        for i in range(1, len(words)):
            bigram[words[i-1]][words[i]] += 1
            
    return bigram

def bigram_probability(bigram, word1, word2):
    return bigram[word1][word2] / sum(bigram[word1].values())

def language_model(context, word, bigram, smoothing=0.1):
    context_count = sum(bigram[context].values())
    if context_count == 0:
        return smoothing / (context_count + smoothing * len(bigram))
    else:
        word_count = bigram[context][word]
        return (word_count + smoothing) / (context_count + smoothing * len(bigram))

def perplexity(cands, bigram, smoothing=0.1):
    perplexity = 0
    N = 0
    words = " ".join(cands).split()
    for i in range(1, len(words)):
        context = words[i-1]
        word = words[i]
        perplexity += -1 * np.log(language_model(context, word, bigram, smoothing))
        N += 1
    return np.exp(perplexity / N)

if __name__ == "__main__":
    with open("refs.txt") as f:
        refs = [line.strip() for line in f]
    with open("hypos.txt") as f:
        cands = [line.strip() for line in f]
    bigram = bigram_model(refs)
    print(f"Perplexity: {perplexity(cands, bigram):.2f}")
