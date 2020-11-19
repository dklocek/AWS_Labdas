import boto3
import datetime


def send_mail(data):
    # Use your sender e-mail
    sender = "sender@email"

    # Use your recipient e-mail
    recipient = "recipient@email"

    # Use your AWS region where SES is used
    aws_region = "aws region"

    # e-mail subject
    subject = "AWS SES - Certificates will soon expire"

    # preparing massage to inject in html body
    massage = ""

    for line in data:
        massage = massage + "<p>" + line + "</p>"

    body_html = """
    <html>
        <head></head>
            <body>
                    <h1>Certificates that will expire in less then 30 days</h1>
                    
                    """ + massage + """
            </body>
    </html>
            """
    charset = "UTF-8"
    client = boto3.client('ses', region_name=aws_region)

    # Send notification e-mail
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
                        'Data': "",
                    },
                },
                'Subject': {
                    'Charset': charset,
                    'Data': subject,
                },
            },
            Source=sender,
        )
    # Return exception if something goes wrong
    except Exception as e:
        return e
    else:
        return "E-mail was send at" + str(datetime.datetime.now())
