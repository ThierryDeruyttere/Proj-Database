import smtplib
import hashlib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendVerification(email):
    sender = 'info.codegalaxy@gmail.com'
    password = 'ruien9690'

    receiver = email

    hash_sequence = hashlib.md5(email.encode('utf-8')).hexdigest()

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Welcome to Codegalaxy!"
    msg['From'] = sender
    msg['To'] = receiver

    # Create the body of the message (a plain-text and an HTML version).
    text = "Welcome to Codegalaxy!\n\nlocalhost:8000/verification/{hash}".format(hash=hash_sequence)
    html = """
    <html>
      <head></head>
      <body>
        <h2>Welcome to Codegalaxy!</h2>
        <p>
          Verify your email now using the link below.<br /><br />
          <a href="localhost:8000/verification/{hash}">localhost:8000/verification/{hash}</a><br />
        </p>
      </body>
    </html>
    """.format(hash=hash_sequence)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(sender, password)
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()

def sendVerificationAccepted(email):
    pass
