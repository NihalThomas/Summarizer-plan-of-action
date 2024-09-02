import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to send email
def send_mail(recipients, summary, plan_of_action):
    sender_email = "Enter the sender's mail ID"  # Your sender email
    app_password = "APP PASSWORD"  # Your app-specific password

    subject = "Meeting Summary and Plan of Action"
    body = f"""
    Dear Team,<br><br>

    I hope this email finds you well. The purpose of this message is to highlight the key points discussed in today's meeting:<br><br>

    <b>Summary:</b><br>
    {summary}<br><br>

    <b>Plan of Action:</b><br>
    {plan_of_action}<br>

    Your prompt attention to these matters is appreciated.<br><br>

    Best regards,<br>
    Nihal Thomas
    """

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