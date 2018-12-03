from array import array
from difflib import SequenceMatcher
import nltk
from base_nlp import BaseNLP


class SimilarityMetric(BaseNLP):

    def __init__(self, text):
        """Constructor to initialize the base class"""

        super(SimilarityMetric, self).__init__(text)
        self.cleaned_text = self.clean_text_util(self._text)
        if len(self.cleaned_text) != 2:
            raise ValueError('Please supply two sequences')

    def levenshtein(self):
        """
        Calculates the Levenshtein Similarity (minimum distance) between two string sequences.
        This method is implemented using the NLTK module.

        The return value will be a float between 0 and 1 included, where 0 means
        totally different, and 1 equal.
        The return value will be 0.0 if any of the two sequences are not instance of string
        """

        seq1 = self.cleaned_text[0]
        seq2 = self.cleaned_text[1]

        if seq1 == seq2:
            return 1.0

        len1, len2 = len(seq1), len(seq2)

        if len1 < len2:
            len1, len2 = len2, len1
            seq1, seq2 = seq2, seq1

        distance = nltk.edit_distance(seq1, seq2)
        norm_distance = distance / float(len(seq1))
        similarity = 1 - norm_distance
        return similarity

    def jaccard(self):
        """
        Calculates the Jaccard Similarity between two string sequences

        The return value will be a float between 0 and 1 included, where 0 means
        totally different, and 1 equal.
        The return value will be 0.0 if any of the two sequences are not instance of string
        """
        seq1 = self.cleaned_text[0]
        seq2 = self.cleaned_text[1]

        seq1, seq2 = set(seq1), set(seq2)
        norm_distance = nltk.jaccard_distance(seq1, seq2)
        # print('Normalized Distance: %.4f' % norm_distance)
        similarity = 1 - norm_distance
        return similarity

    def jaro_winkler(self):
        """
        Calculates the Jaro Winkler Similarity between two string sequences

        The return value will be a float between 0 and 1 included, where 0 means
        totally different, and 1 equal.
        The return value will be 0.0 if any of the two sequences are not instance of string
        """

        seq1 = self.cleaned_text[0]
        seq2 = self.cleaned_text[1]

        s1_len, s2_len = len(seq1), len(seq2)
        match_distance = (max(s1_len, s2_len) // 2) - 1
        if match_distance < 0:
            match_distance = 0

        # print('match_distance: %d' % match_distance)

        s1_matches = [False] * s1_len
        s2_matches = [False] * s2_len

        matches = 0
        transpositions = 0

        # look for matches within the match_distance only
        for i, s1_ch in enumerate(seq1):
            # print(f'i: {i}; s1_ch: {s1_ch}')
            start = int(max(0, i - match_distance))
            end = int(min(i + match_distance + 1, s2_len))
            # print(f'Match Range for s2 = {start} - {end}')

            for j in range(start, end):
                if s2_matches[j]:
                    continue
                if seq1[i] != seq2[j]:
                    continue
                s1_matches[i] = s2_matches[j] = True
                matches += 1
                break

        if matches == 0:
            return 0.0

        # count transpositions
        k = 0
        for i in range(s1_len):
            if not s1_matches[i]:
                continue
            while not s2_matches[k]:
                k += 1
            if seq1[i] != seq2[k]:
                transpositions += 1
            k += 1

        score = ((matches / s1_len) + (matches / s2_len) + ((matches - transpositions) / matches)) / 3

        # winkler modification
        # adjust for up to first 4 chars in common
        prefix_weight = 0.1
        j = min(match_distance, 4)
        i = 0
        while i < j and seq1[i] == seq2[i] and seq1[i]:
            i += 1
        if i:
            score += i * prefix_weight * (1.0 - score)

        return score

    def hamming(self):
        """Compute the Hamming distance between the two sequences `seq1` and `seq2`.
        The Hamming distance is the number of differing items in two ordered
        sequences of the same length. If the sequences submitted do not have the
        same length, a score of 0.0 will be returned.

        The return value will be a float between 0 and 1 included, where 0 means
        totally different, and 1 equal.
        """

        seq1 = self.cleaned_text[0]
        seq2 = self.cleaned_text[1]

        s1_len = len(seq1)
        if s1_len != len(seq2):
            return 0.0
        if s1_len == 0:
            return 0.0

        distance = sum(c1 != c2 for c1, c2 in zip(seq1, seq2))
        # Normalized distance
        norm_distance = distance / float(s1_len)
        # Similarity
        return 1 - norm_distance

    def sequencer_matcher(self):
        """
        Calculates the Similarity between two string sequences using the difflib.SequenceMatcher class

        The return value will be a float between 0 and 1 included, where 0 means
        totally different, and 1 equal.
        The return value will be 0.0 if any of the two sequences are not instance of string
        """
        seq1 = self.cleaned_text[0]
        seq2 = self.cleaned_text[1]

        m = SequenceMatcher(None, seq1, seq2)
        return m.ratio()

if __name__ == '__main__':
    # pass
    text = ['Apples are red', 'Apples are bananas']
    sm = SimilarityMetric(text)
    m = sm.levenshtein();
    print('Levenshtein: ' + str(m))
    m = sm.jaccard();
    print('jaccard: ' + str(m))
    m = sm.jaro_winkler();
    print('jaro_winkler: ' + str(m))
    m = sm.hamming();
    print('hamming: ' + str(m))
    m = sm.sequencer_matcher();
    print('sequencer_matcher: ' + str(m))
