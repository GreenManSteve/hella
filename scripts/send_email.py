import boto3
from botocore.exceptions import ClientError

class Email:
    def __init__(self, subject, body_text, link_url=""):
        self.SENDER = "HellaIngester@belron.com"
        self.RECIPIENT = "HellaIngester@belron.com"
        self.SUBJECT = subject
        self.BODY_TEXT = body_text
        self.LINK_URL = link_url


    def send_email(self):
        # The character encoding for the email.
        CHARSET = "UTF-8"
        # Create a new SES resource and specify a region.
        client = boto3.client('ses', region_name='eu-west-1')
        if self.LINK_URL is not None:
            a_link = "<a href={link}>{link}</a>".format(link=self.LINK_URL)
        else:
            a_link = ''
        BODY_HTML = """<html>
        <head></head>
        <body>
          <h1>{subject}</h1>
          <p>{message}<br />
         {link}
          </p>
        </body>
        </html>
                    """.format(subject=self.SUBJECT, message=self.BODY_TEXT, link=a_link)

        # Try to send the email.
        try:
            # Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        self.RECIPIENT,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': BODY_HTML,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': self.SUBJECT,
                    },
                },
                Source=self.SENDER,
                # If you are not using a configuration set, comment or delete the
                # following line
                # ConfigurationSetName=CONFIGURATION_SET,
            )
        # Display an error if something goes wrong.
        except ClientError as e:
            print(e.response['Error']['Message'])
        finally:
            print("Email sent! Message ID:"),
