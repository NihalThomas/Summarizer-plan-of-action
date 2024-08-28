import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to send email
def send_mail(recipients, subject, body):
    sender_email = "Enter the sender's mail ID"  # Your sender email
    app_password = "APP PASSWORD"  # Your app-specific password

    # Create MIMEText object
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = ', '.join(recipients)
    message['Subject'] = subject
    message.attach(MIMEText(body, 'html'))  # Ensure HTML formatting for the body

    try:
        # Establish SMTP connection
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, recipients, message.as_string())

        print(f"Email has been successfully sent to {', '.join(recipients)}")

    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")

