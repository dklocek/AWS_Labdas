import boto3


def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    data = event['Records'][0]
    sourceBucket = data['s3']['bucket']['name']
    sourceKey = data['s3']['object']['key']
    sourceIp = data['requestParameters']['sourceIPAddress']

    destinationBucket = "yaml-bucket-buldas"

    print("File was puted from " + sourceIp)
    print("Bucket Name" + sourceBucket)
    print("File Name" + sourceKey)

    copy_source = {
        'Bucket': sourceBucket,
        'Key': sourceKey
    }

    print("Trying to copy to: s3://" + destinationBucket)

    try:
        s3.meta.client.copy(copy_source, destinationBucket, sourceKey)
    except Exception as e:
        print(e)
    else:
        print("Success!")

    sender = "buldas@wp.pl"
    recipient = "d.klocek@wp.pl"
    aws_region = "eu-west-1"
    subject = "Amazon SES Test"
    body_text = ("Source IP - " + sourceIp + "\r\n"
                                             "Bucket name - " + sourceBucket + "\r\n"
                                                                               "File Name - " + sourceKey + "\r\n"
                                                                                                            "Destination Bucket - " + destinationBucket)
    body_html = """
    <html>
        <head></head>
            <body>
                    <h1>LAMBDA EMAIL</h1>
                    <p>Source IP    - {sourceIp}</p>
                    <p>Bucket name  - {sourceBucket}</p>
                    <p>File Name    - {sourceKey}</p>
                    <p>Destination Bucket - {destinationBucket}</p>
                    
                    <p>This email was sent with
                    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
                    <a href='https://aws.amazon.com/sdk-for-python/'>
                    AWS SDK for Python (Boto)</a>.</p>
            </body>
    </html>
            """.format(sourceIp=sourceIp, sourceBucket=sourceBucket, sourceKey=sourceKey,
                       destinationBucket=destinationBucket)
    charset = "UTF-8"
    client = boto3.client('ses', region_name=aws_region)

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': charset,
                        'Data': body_html,
                    },
                    'Text': {
                        'Charset': charset,
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': charset,
                    'Data': subject,
                },
            },
            Source=sender,
        )
    except Exception as e:
        print(e)
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])