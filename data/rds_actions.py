import sys
sys.path.insert(0,'/app/scripts')
import shutil

import psycopg2
from auth_settings import dbname, user, password, host, port
from datetime import datetime
import hashlib
import os.path
import csv
import pandas as pd
import math

conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
cur = conn.cursor()

def _list_depth(l):
    if isinstance(l, list):
        return 1 + max(_list_depth(item) for item in l)
    else:
        return 0

def remove_cache():
    """Remove local _cache dir"""
    if os.path.isdir("_cache"):
        shutil.rmtree("_cache")

def safe_execute(query, cmd='fetchall'):
    """Execute database operations and fetch rows of query result

    Args:
        query (str): database query string
        cmd (str): psycopg2 command used to fetch from cursor

    Returns:
        result (json): rows resulting from execute operation
    """

    result = None

    date_str = datetime.now().strftime("%Y-%m-%d") #"%Y-%m-%d %H"
    query_hash = hashlib.sha1((query+date_str).encode('utf-8')).hexdigest()

    if 'api_keys' not in query:
        hash_path = os.path.join("_cache","{}.csv".format(query_hash))

        if os.path.exists(hash_path):
            df = pd.read_csv(hash_path, header=None)
            df.where((pd.notnull(df)), None)
            result = df.values.tolist()
            if (pd.isnull(nl).any() for nl in result):
                result = [[None if pd.isnull(x) else x for x in c] for c in result]
            return result
        else:
            try:
                q = cur.execute(query)
                if cmd == 'fetchall':
                    result = cur.fetchall()
                elif cmd == 'fetchone':
                    result = cur.fetchone()

                if not os.path.isdir("_cache"):
                    os.makedirs("_cache")

                if result:
                    df = pd.DataFrame(result)
                    df.to_csv(hash_path, index=False, header=False)
            except (psycopg2.InternalError, psycopg2.DataError) as e:
                if conn:
                    conn.reset()
            finally:
                return result
    else:
        try:
            q = cur.execute(query)
            if cmd == 'fetchall':
                result = cur.fetchall()
            elif cmd == 'fetchone':
                result = cur.fetchone()
        except (psycopg2.InternalError, psycopg2.DataError) as e:
            if conn:
                conn.reset()
        finally:
            return result

# inserts returned json from aylien to RDS
def json_to_rds(stories_json_obj={}):
    for item in stories_json_obj:
        cur.execute('insert into collection(content_id, collector_name, news_source_id, publish_date, \
        news_source_name, source_url, author_name, news_title, story_text, summary_sents,\
         selectors, topic_tags, impact_score) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT \
         (content_id) DO NOTHING', (item['content_id'], 'News', item['news_source_id'], \
         item['publish_date'], item['news_source_name'], item['source_url'], \
         item['author_name'], item['news_title'], item['text'], \
         item['summary_sents'], item['selectors'], item['topic_tags'], item['impact_score']))
        conn.commit()


# inserts returned json from Twitter to RDS
def twitter_to_rds(json_data):
    cur.execute('insert into collection(selectors, content_id, collector_name, social_id, \
    publish_date, story_text, topic_tags, source_url, ref_id, impact_score, ref_user_id) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) \
    ON CONFLICT (content_id) DO NOTHING', (json_data['selectors'], json_data['content_id'], \
    'Twitter', json_data['social_id'], json_data['publish_date'], json_data['story_text'], json_data['topic_tags'], \
    json_data ['source_url'], json_data['ref_id'], json_data['impact_score'], json_data['ref_user_id']))
    conn.commit()

# inserts concepts json from concepts.py to RDS
def insert_concepts(json_data):
    cur.execute('insert into ling_features (fk_content_id, fk_collection_publish_date, chunk_text, \
    chunk_root_head_text, chunk_root_dep, chunk_concept, chunk_perspective) VALUES (%s,%s,%s,%s,%s,%s,%s)', \
    (item['content_id'], item['publish_date'], item['chunk_text'], item['chunk_root_head_text'], \
    item['chunk_root_dep'], item['chunk_concept'], item['chunk_perspective']))
    con.commit()

# inserts concepts json from concepts.py to RDS
def insert_perspectives(json_data):
    cur.execute('insert into ling_features (fk_content_id, fk_collection_publish_date, sentence, tok_text, \
    tok_lemma, tok_tag, tok_pos, noun_chunk) VALUES (%s,%s,%s,%s,%s,%s,%s, %s)', \
    (item['content_id'], item['publish_date'], item['sents'], item['tok_text'], \
    item['tok_lemma'], item['tok_tag'], item['tok_pos']))
    con.commit()

if __name__ == '__main__':
    pass
