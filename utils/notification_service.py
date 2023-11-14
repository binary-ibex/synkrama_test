from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings

def send_email(subject, to_email, html_content):
    message = Mail(
        from_email=settings.SENDGRID_SENDER_MAIL,
        to_emails=to_email,
        subject=subject,
        html_content=html_content,
    )

    try:
        sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {str(e)}")
