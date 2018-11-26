import sys
sys.path.insert(0,'/app/data')
sys.path.insert(0,'/app/scripts')

import io
import gzip
import boto3
import time
from auth_settings import aws_secret_access_key, aws_access_key_id, bucket_name

timestr = time.strftime("%Y%m%d-%H%M%S")
filename = 'news-'+timestr

def news_to_s3(data):
    # set s3
    s3 = boto3.resource('s3',
         aws_access_key_id=aws_access_key_id,
         aws_secret_access_key=aws_secret_access_key)
    s3.Object(bucket_name, filename).put(Body=str(data))

def news_to_df_s3(data):
    # set s3
    s3 = boto3.resource('s3')

    # write DF to string stream
    file_buffer = io.StringIO()

    # reset stream position
    file_buffer.seek(0)

    # create binary stream
    gz_buffer = io.BytesIO()

    # compress string stream using gzip
    with gzip.GzipFile(mode='w', fileobj=gz_buffer) as gz_file:
        gz_file.write(bytes(file_buffer.getvalue(), 'utf-8'))

    # write stream to S3
    s3.Object(bucket_name, filename).put(Body=file_buffer.getvalue())
