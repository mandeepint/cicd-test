import sys
sys.path.insert(0, '/app/analytics/nlp')
# sys.path.insert(0, '/Users/mandeep-std/repos/test_CICD/analytics/nlp')

import pytest
from simscore import SimilarityMetric

#Just a comment
@pytest.fixture
def s():
    return SimilarityMetric()


@pytest.fixture
def different_sequences1():
    return ['Roses are red', 'Violets are blue']


@pytest.fixture
def same_sequences():
    return ['Roses are red', 'ROSES ARE RED']


@pytest.fixture
def wrong_args():
    return [1, 'ROSES ARE RED']


def test_levenshtein_with_diff_seqs(s, different_sequences1):
    score = s.levenshtein(different_sequences1[0], different_sequences1[1])
    assert score < 1.0


def test_levenshtein_with_same_seqs(s, same_sequences):
    score = s.levenshtein(same_sequences[0], same_sequences[1])
    assert score == 1.0


def test_levenshtein_with_incorrect_args(s, wrong_args):
    score = s.levenshtein(wrong_args[0], wrong_args[1])
    assert score == 0.0


def test_nltk_levenshtein_with_diff_seqs(s, different_sequences1):
    score = s.nltk_levenshtein(different_sequences1[0], different_sequences1[1])
    assert score < 1.0


def test_nltk_levenshtein_with_same_seqs(s, same_sequences):
    score = s.nltk_levenshtein(same_sequences[0], same_sequences[1])
    assert score == 1.0


def test_nltk_levenshtein_with_incorrect_args(s, wrong_args):
    score = s.nltk_levenshtein(wrong_args[0], wrong_args[1])
    assert score == 0.0


def test_jaccard_with_diff_seqs(s, different_sequences1):
    score = s.jaccard(different_sequences1[0], different_sequences1[1])
    assert score < 1.0


def test_jaccard_with_same_seqs(s, same_sequences):
    score = s.jaccard(same_sequences[0], same_sequences[1])
    assert score == 1.0


def test_jaccard_with_incorrect_args(s, wrong_args):
    score = s.jaccard(wrong_args[0], wrong_args[1])
    assert score == 0.0


def test_jaro_winkler_with_diff_seqs(s, different_sequences1):
    score = s.jaro_winkler(different_sequences1[0], different_sequences1[1])
    assert score < 1.0


def test_jaro_winkler_with_same_seqs(s, same_sequences):
    score = s.jaro_winkler(same_sequences[0], same_sequences[1])
    assert score == 1.0


def test_jaro_winkler_with_incorrect_args(s, wrong_args):
    score = s.jaro_winkler(wrong_args[0], wrong_args[1])
    assert score == 0.0


def test_hamming_with_diff_seqs(s, different_sequences1):
    score = s.hamming(different_sequences1[0], different_sequences1[1])
    assert score < 1.0


def test_hamming_with_same_seqs(s, same_sequences):
    score = s.hamming(same_sequences[0], same_sequences[1])
    assert score == 1.0


def test_hamming_with_incorrect_args(s, wrong_args):
    score = s.hamming(wrong_args[0], wrong_args[1])
    assert score == 0.0


def test_sequencer_matcher_with_diff_seqs(s, different_sequences1):
    score = s.sequencer_matcher(different_sequences1[0], different_sequences1[1])
    assert score < 1.0


def test_sequencer_matcher_with_same_seqs(s, same_sequences):
    score = s.sequencer_matcher(same_sequences[0], same_sequences[1])
    assert score == 1.0


def test_sequencer_matcher_with_incorrect_args(s, wrong_args):
    score = s.sequencer_matcher(wrong_args[0], wrong_args[1])
    assert score == 0.0
