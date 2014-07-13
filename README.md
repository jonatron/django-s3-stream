django-s3-stream
================

Django S3 Streaming Example

A tiny django app to run on S3, to generate streaming zip files from S3. 

Uses a branch of a fork zipstream 
https://github.com/longaccess/python-zipstream/tree/streaminput
and a hack around BotoKey to make it enough like a file-like object

The secret key should be the same as the def003/defected key

For reasons I can't work out, for really big zips, uwsgi+nginx and 
gunicorn+nginx do not work. So we're using django-wsgiserver. 