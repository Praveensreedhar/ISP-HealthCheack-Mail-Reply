import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
smtp_server = '10.10.10.10'  # Replace with your SMTP server address
smtp_port = 25  # Replace with the appropriate port for your SMTP server
sender_email = '123@utstr.com'  # Replace with your email address
recipient_email = '123@utstr.com'  # Replace with the recipient's email address

# Create a message object
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = recipient_email
msg['Subject'] = 'Subject of your email'

# Add the email body
email_body = 'Please create Docket with TATA for further investigation CKT ID 1234567'
msg.attach(MIMEText(email_body, 'plain'))

# Connect to the SMTP server
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Enable TLS encryption (if supported by your SMTP server)
    #server.login(sender_email, 'your_email_password')  # Replace with your email password

    # Send the email
    server.sendmail(sender_email, recipient_email, msg.as_string())
    print('Email sent successfully!')
except Exception as e:
    print(f'Error: {str(e)}')
finally:
    server.quit()
