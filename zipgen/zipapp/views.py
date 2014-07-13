from django.http import StreamingHttpResponse, HttpResponse
from django.conf import settings
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import boto
import zipstream
import urllib2
import tempfile

class BotoKeyWrapper(Key):
    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.closed = True

    def __enter__(self):
        return self


def test(request):
    conn = S3Connection(settings.AWS_ACCESS_KEY_ID,
                        settings.AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)

    # list of s3 keys to put in zip file
    tracks = [
        'wool.jpg',
    ]

    z = zipstream.ZipFile(mode='w', compression=zipstream.ZIP_STORED)

    # also put in a file downloaded from a url
    req = urllib2.urlopen("http://hexus.net/media/img/hexus_web_shadow_trans.png?402516240412")
    t = tempfile.TemporaryFile()
    t.write(req.read())
    t.seek(0)
    z.write(t, arcname="test_art.png")

    for track in tracks:
        key = bucket.get_key(track)
        if key:
            # Yeah that's right...what an awesome hack!
            key.__class__ = BotoKeyWrapper
            z.write(key, arcname=track)
        else:
            print "bad key"


    response = StreamingHttpResponse(z, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="lol.zip"'
    return response
