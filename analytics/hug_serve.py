import sys
sys.path.insert(0,'/app/data')
sys.path.insert(0,'/app/scripts')
sys.path.insert(0,'/app/analytics/nlp')
# sys.path.insert(0,'/Users/mandeep-std/repos/test_CICD/analytics/nlp')


import hug
from simscore import SimilarityMetric
import falcon

"""Initialize hug object"""
api = hug.API(__name__)

"""Apply CORS middleware to allow browser access"""
api.http.add_middleware(hug.middleware.CORSMiddleware(api, max_age=10))

@hug.get('/sim_score')
def get_sim_score(seq1: hug.types.text, seq2:hug.types.text, method:hug.types.text = 'levenshtein'):
    """ Compare Similarity between sequences

    Args:
        Two Sequences for which similarity score needs to be calculated,
        and the method used to calculate the score. Available methods are
        levenshtein (default), jaccard, jaro-winkler, hamming and sequencer-matcher

    Returns:
        Scaled Score between 0.0 and 1.0 with
        0.0 - Sequences are not similar at all
        1.0 - Sequences are completely similar (case-insensitive)

    """
    method = method.lower()

    simscore = SimilarityMetric()

    if method == 'levenshtein':
         similarity = simscore.levenshtein(seq1, seq2)
         return {'sim_score':round(similarity,4)}

    elif method == 'jaccard':
         similarity = simscore.jaccard(seq1, seq2)
         return {'sim_score':round(similarity,4)}

    elif method == 'jaro-winkler':
         similarity = simscore.jaro_winkler(seq1, seq2)
         return {'sim_score':round(similarity,4)}

    elif method == 'hamming':
         similarity = simscore.hamming(seq1, seq2)
         return {'sim_score':round(similarity,4)}

    elif method == 'sequencer-matcher':
         similarity = simscore.sequencer_matcher(seq1, seq2)
         return {'sim_score':round(similarity,4)}
    else:
        return 'Unsupported method. Supported method types are Levenshtein, Jaccard, Jaro-Winkler, Hamming, Sequence-Matcher'

if __name__ == '__main__':
    api.http.serve()
    # seq1 = 'Apple is red'
    # seq2 = 'Apple is green'
    # # print('seq1: '+seq1)
    # # print('seq2: '+seq2)
    # m = get_sim_score(seq1,seq2)
    # print('Levenshtein: ' + str(m))
    # m = get_sim_score(seq1,seq2,method='JACCARD')
    # print('Jaccard: ' + str(m))
    # m = get_sim_score(seq1,seq2,method='jaro-winkler')
    # print('Jaro Winkler: ' + str(m))
    # m = get_sim_score(seq1,seq2,method='hamming')
    # print('Hamming: ' + str(m))
    # m = get_sim_score(seq1,seq2,method='sequencer-matcher')
    # print('Sequence Matcher: ' + str(m))
