from boto.s3.connection import S3Connection
from storages.backends.s3boto import S3BotoStorage
import os
import math
from multiprocessing.pool import Pool


def _upload_part(bucketname, aws_key, aws_secret, multipart_id, part_num,
                 source_path, offset, bytes, amount_of_retries=10):
    """
    Uploads a part with retries.
    """
    def _upload(retries_left=amount_of_retries):
        try:
            conn = S3Connection(aws_key, aws_secret)
            bucket = conn.get_bucket(bucketname)
            for mp in bucket.get_all_multipart_uploads():
                if mp.id == multipart_id:
                    with open(source_path, 'rb') as fp:
                        fp.seek(offset)
                        mp.upload_part_from_file(fp=fp, part_num=part_num, size=bytes)
                    break
        except Exception, exc:
            if retries_left:
                _upload(retries_left=retries_left - 1)
            else:
                print('... Failed uploading part #%d' % part_num)
                raise exc
    _upload()


class ThreadedS3BotoStorage(S3BotoStorage):

    def _save_content(self, key, content, headers):
        print "key.name", key.name
        source_size = os.stat(content.file.name).st_size
        bytes_per_chunk = max(int(math.sqrt(5242880) * math.sqrt(source_size)), 5242880)
        chunk_amount = int(math.ceil(source_size / float(bytes_per_chunk)))
        mp = self.bucket.initiate_multipart_upload(key.name, headers=headers)

        pool = Pool(processes=1)
        for i in range(chunk_amount):
            offset = i * bytes_per_chunk
            remaining_bytes = source_size - offset
            bytes = min([bytes_per_chunk, remaining_bytes])
            part_num = i + 1
            pool.apply_async(_upload_part, [self.bucket_name, self.access_key,
                             self.secret_key, mp.id, part_num,
                             content.file.name, offset, bytes])
        pool.close()
        pool.join()

        if len(mp.get_all_parts()) == chunk_amount:
            mp.complete_upload()
            key = self.bucket.get_key(key.name)
        else:
            mp.cancel_upload()
