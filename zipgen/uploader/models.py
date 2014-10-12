import boto
import os

from django.db import models
from django.conf import settings
#from storages.backends.s3boto import S3BotoStorage
from uploader.storage import ThreadedS3BotoStorage  # faster

private_storage = ThreadedS3BotoStorage(headers={'Content-Disposition': 'attachment'})


class S3Object(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(storage=private_storage, upload_to='uploads', max_length=255)
