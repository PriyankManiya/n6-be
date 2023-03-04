from django.core.mail import EmailMessage
import os


class Util:
    @staticmethod
    def send_email(data):
        try :
            email_from = os.environ.get('EMAIL_HOST_FROM')
            email = EmailMessage(
                subject=data['email_subject'], 
                body=data['email_body'], 
                from_email=email_from, 
                to=[data['email_to']]
                )
            email.send()
        except Exception as e:
            print('Error : ' , e)