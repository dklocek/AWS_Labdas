import boto3
import datetime
from ses_sender import send_mail


def lambda_handler(event, context):
    # Creates an Amazon Certificate Manager client
    client = boto3.client('acm')

    # Get the list of certificates in ACM
    certs_list = client.list_certificates()['CertificateSummaryList']
    notification_list = []

    # Process every found certificate
    for data in certs_list:
        cert_data = client.describe_certificate(CertificateArn=data['CertificateArn'])
        domain_name = cert_data['Certificate']['DomainName']
        expiration_date = cert_data['Certificate']['NotAfter'].date()
        days_left = expiration_date - datetime.datetime.now().date()
        days_left = days_left.days
        print(domain_name)
        print(days_left)
        # Expiration time alert, if changed please change in the html_body in ses_sender.py
        # Adds domain name and days left to expire to a list that will be pass to send_mail() function
        if days_left < 30:
            notification_list.append("Domain " + domain_name + " will expire in <b>" + str(days_left) + "</b> "
                                                                                                        "days")
    # If any certificate will expire in given time, email notification will be send
    if len(notification_list) != 0:
        return send_mail(notification_list)
    else:
        return "Nothing to send"
