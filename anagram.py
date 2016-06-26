#This file is Johannes Gårdsted Valbjørns sollution to trustpilot code challenge.
#This file is part of a MIT licensed git repository located at https://github.com/sloev/anagram_challenge
# - Johannes Gårdsted Valbjørn

from collections import Counter
from hashlib import md5
from sys import stdout

def find_candidates(wordlist, anagram):
    """Compute dict of candidates (bins)

    :param wordlist: a list of words
     :type wordlist: list
    :param anagram: the phrase of which to find anagrams for
     :type anagram: string
    """
    candidate_lengths = set(len(word) for word in anagram.split())
    candidates = {}
    anagram_counter = Counter(anagram)
    for word in wordlist:
        word_counter = Counter(word)
        word_len = len(word)
        if not word_counter - anagram_counter and word_len in candidate_lengths:
            candidates.setdefault(word_len, []).append(word)
    return candidates


def find_matching_md5(candidates, anagram, target_md5):
    """Find matching md5 hash from candidate words

    :param candidates: A dict with candidate_length:candidate_list
     :type candidates: dict
    :param anagram: The string of which to find an anagram phrase
     :type anagram: string
    :param target_md5: The given md5 to find an anagram phrase for
     :type taget_md5: string
    """
    def find_match(candidate_lengths, prev_words=[]):
        """Recursive function that finds a matching md5

        :param candidate_lengths: an ordered list of candidate lengths
         :type candidate_lengths: list
        :param prev_words: a list of previous words in the recursive function
                            used to compute the total string.
        """
        candidate_length = candidate_lengths[0]
        for word in candidates[candidate_length]: 
            cand_words = prev_words + [word]
            if len(candidate_lengths) > 1:
                #Recursive call to go one level deeper (next word in phrase)
                recursive_result = find_match(candidate_lengths[1:], cand_words)
                if recursive_result:
                    return recursive_result
            else:
                cand_word = " ".join(cand_words)
                cand_md5 = md5(cand_word).hexdigest()
                if cand_md5 == target_md5:
                    return cand_word

    candidate_lengths = [len(word) for word in anagram.split()] #for example: [7,7,4]
    return find_match(candidate_lengths)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('anagram', nargs="*", default="poultry outwits ants")
    parser.add_argument('target_md5', nargs="*", default="4624d200580677270a54ccff86b9610e")
    parser.add_argument('wordlist_filename', nargs="*", default="wordlist")
    args = parser.parse_args()

    print "Finding md5 hash matching: '{}' from original phrase: '{}' and wordlist_file: '{}'".format(
         args.target_md5, args.anagram, args.wordlist_filename)
    with open(args.wordlist_filename, "r") as file:
        wordlist = file.read().splitlines()
        candidate_bins = find_candidates(wordlist, args.anagram)
        match = find_matching_md5(candidate_bins, args.anagram, args.target_md5)
        print "Found match:'{}'".format(match)
