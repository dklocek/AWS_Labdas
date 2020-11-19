#lambda-s3trigger-copy-ses-notify

A triggered by S3 PUT event on specified bucket function that:

- copy uploaded file to another bucket
- send an email with information about event (ip of uploader, uploaded file name and bucket name and name of bucket file copied to) 

#acm-cert-days-left-for-expiration-scan

Scans all certificates in Amazon Certificate Manager, and if any will expire in less then 30 day (can be changed) a notification e-mail will be sent.    
