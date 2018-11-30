from array import array
from difflib import SequenceMatcher
import nltk

class SimilarityMetric():

    def levenshtein(self, seq1, seq2):
        """
        Calculates the Levenshtein Similarity (minimum distance) between two string sequences

        The return value will be a float between 0 and 1 included, where 0 means
        totally different, and 1 equal.
        The return value will be 0.0 if any of the two sequences are not instance of string
        """

        result = self.pre_checks(seq1, seq2)
        if result is not None:
            return result
        seq1, seq2 = seq1.lower(), seq2.lower()

        len1, len2 = len(seq1), len(seq2)

        if len1 < len2:
            len1, len2 = len2, len1
            seq1, seq2 = seq2, seq1

        column = array('L', range(len2 + 1))

        for x in range(1, len1 + 1):
            column[0] = x
            last = x - 1
            for y in range(1, len2 + 1):
                old = column[y]
                cost = int(seq1[x - 1] != seq2[y - 1])
                column[y] = min(column[y] + 1, column[y - 1] + 1, last + cost)
                last = old

        # Raw distance
        distance = column[len2]
        # print('Raw Distance: %d' % distance)
        norm_distance = distance / float(len1)
        # print('Normalized Distance: %.4f' % norm_distance)
        similarity = 1 - norm_distance
        # print('similarity: %.4f' % similarity)
        return similarity

    def nltk_levenshtein(self, seq1, seq2):
        """
        Calculates the Levenshtein Similarity (minimum distance) between two string sequences.
        This method is implemented using the NLTK module.

        The return value will be a float between 0 and 1 included, where 0 means
        totally different, and 1 equal.
        The return value will be 0.0 if any of the two sequences are not instance of string
        """
        result = self.pre_checks(seq1, seq2)
        if result is not None:
            return result
        seq1, seq2 = seq1.lower(), seq2.lower()

        len1, len2 = len(seq1), len(seq2)

        if len1 < len2:
            len1, len2 = len2, len1
            seq1, seq2 = seq2, seq1

        distance = nltk.edit_distance(seq1, seq2)
        norm_distance = distance / float(len(seq1))
        similarity = 1 - norm_distance
        return similarity

    def jaccard(self, seq1, seq2):
        """
        Calculates the Jaccard Similarity between two string sequences

        The return value will be a float between 0 and 1 included, where 0 means
        totally different, and 1 equal.
        The return value will be 0.0 if any of the two sequences are not instance of string
        """
        result = self.pre_checks(seq1, seq2)
        if result is not None:
            return result
        seq1, seq2 = seq1.lower(), seq2.lower()

        seq1, seq2 = set(seq1), set(seq2)
        norm_distance = nltk.jaccard_distance(seq1, seq2)
        # print('Normalized Distance: %.4f' % norm_distance)
        similarity = 1 - norm_distance
        return similarity

    def jaro_winkler(self, seq1, seq2):
        """
        Calculates the Jaro Winkler Similarity between two string sequences

        The return value will be a float between 0 and 1 included, where 0 means
        totally different, and 1 equal.
        The return value will be 0.0 if any of the two sequences are not instance of string
        """

        result = self.pre_checks(seq1, seq2)
        if result is not None:
            return result
        seq1, seq2 = seq1.lower(), seq2.lower()

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

    def hamming(self, seq1, seq2):
        """Compute the Hamming distance between the two sequences `seq1` and `seq2`.
        The Hamming distance is the number of differing items in two ordered
        sequences of the same length. If the sequences submitted do not have the
        same length, a score of 0.0 will be returned.

        The return value will be a float between 0 and 1 included, where 0 means
        totally different, and 1 equal.
        """

        result = self.pre_checks(seq1, seq2)
        if result is not None:
            return result
        seq1, seq2 = seq1.lower(), seq2.lower()

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

    def sequencer_matcher(self, seq1, seq2):
        """
        Calculates the Similarity between two string sequences using the difflib.Sequence matcher classxs

        The return value will be a float between 0 and 1 included, where 0 means
        totally different, and 1 equal.
        The return value will be 0.0 if any of the two sequences are not instance of string
        """
        result = self.pre_checks(seq1, seq2)
        if result is not None:
            return result
        seq1, seq2 = seq1.lower(), seq2.lower()
        m = SequenceMatcher(None, seq1, seq2)
        return m.ratio()

    def pre_checks(self, seq1, seq2):
        if not seq1 or not seq2:
            return 0.0
        if seq1 == seq2:
            return 1.0
        if not all(isinstance(item, str) for item in [seq1, seq2]):
            return 0.0


if __name__ == '__main__':
    # pass
    sm = SimilarityMetric()
    seq1 = 'Apple'
    # seq1 = 1
    seq2= 'apples are not oranges'
    # print('seq1: '+seq1)
    # print('seq2: '+seq2)
    m = sm.levenshtein(seq1,seq2)
    print('Levenshtein: ' + str(m))
    m = sm.nltk_levenshtein(seq1,seq2)
    print('NLTK Levenshtein: ' + str(m))
    m = sm.jaccard(seq1,seq2)
    print('Jaccard: ' + str(m))
    m = sm.jaro_winkler(seq1,seq2)
    print('Jaro Winkler: ' + str(m))
    m = sm.hamming(seq1,seq2)
    print('Hamming: ' + str(m))
    m = sm.sequencer_matcher(seq1,seq2)
    print('Sequence Matcher: ' + str(m))
