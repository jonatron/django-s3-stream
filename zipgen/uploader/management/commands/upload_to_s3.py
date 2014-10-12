from django.core.management.base import BaseCommand, CommandError

from django.conf import settings
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from uploader.models import S3Object
from django.core.files import File


class Command(BaseCommand):
    def handle(self, *args, **options):
        conn = S3Connection(settings.AWS_ACCESS_KEY_ID,
                            settings.AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)

        s3track = S3Object(file=File(open('uploader/cat.gif')))
        s3track.file.name = 'cat2.gif' # change uploaded file name
        failed = True
        for i in range(3): #retry up to 3 times:
            try:
                s3track.save()
                failed = False
                break
            except Exception, e:
                print "Upload attempt: " + str(i)
                print e