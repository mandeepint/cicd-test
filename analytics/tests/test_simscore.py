import sys
sys.path.insert(0, '/app/analytics/nlp')

import pytest
from simscore import SimilarityMetric


@pytest.fixture
def sm_diff_seq():
    return SimilarityMetric(['Roses are red', 'Violets are blue'])

@pytest.fixture
def sm_same_seq():
    return SimilarityMetric(['Roses are red', 'ROSES ARE RED'])



@pytest.fixture
def different_sequences1():
    return ['Roses are red', 'Violets are blue']


@pytest.fixture
def same_sequences():
    return ['Roses are red', 'ROSES ARE RED']


def test_wrong_args():
    with pytest.raises(TypeError):
        SimilarityMetric([1, 'ROSES ARE RED'])


def test_missing_args():
    with pytest.raises(ValueError):
        SimilarityMetric(['ROSES ARE RED'])


def test_levenshtein_with_diff_seqs(sm_diff_seq):
    score = sm_diff_seq.levenshtein()
    assert score < 1.0


def test_levenshtein_with_same_seqs(sm_same_seq):
    score = sm_same_seq.levenshtein()
    assert score == 1.0


def test_jaccard_with_diff_seqs(sm_diff_seq):
    score = sm_diff_seq.jaccard()
    assert score < 1.0


def test_jaccard_with_same_seqs(sm_same_seq):
    score = sm_same_seq.jaccard()
    assert score == 1.0


def test_jaro_winkler_with_diff_seqs(sm_diff_seq):
    score = sm_diff_seq.jaro_winkler()
    assert score < 1.0


def test_jaro_winkler_with_same_seqs(sm_same_seq):
    score = sm_same_seq.jaro_winkler()
    assert score == 1.0


def test_hamming_with_diff_seqs(sm_diff_seq):
    score = sm_diff_seq.hamming()
    assert score < 1.0


def test_hamming_with_same_seqs(sm_same_seq):
    score = sm_same_seq.hamming()
    assert score == 1.0


def test_sequencer_matcher_with_diff_seqs(sm_diff_seq):
    score = sm_diff_seq.sequencer_matcher()
    assert score < 1.0


def test_sequencer_matcher_with_same_seqs(sm_same_seq):
    score = sm_same_seq.sequencer_matcher()
    assert score == 1.0