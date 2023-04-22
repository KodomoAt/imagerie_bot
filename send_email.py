import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(receiver, dates):
    sender_email = os.getenv("SENDER")
    receiver_email = receiver
    password = os.getenv("EMAIL_PASSWORD")

    message = MIMEMultipart("alternative")
    message["Subject"] = "Un nouveau rendez-vous"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message

    html = """\
    <html>
    <body>
        <p>Bonjour,<br>
        Un nouveau rendez-vous est disponible.<br>
        
        {}
        </p>
    </body>
    </html>
    """.format(dates)

    # Turn these into plain/html MIMEText objects

    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first

    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(os.getenv("SMTP_SERVER"), 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )