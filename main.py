import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randint
from flask import Flask, request

app = Flask("mail")

smtp_server = "smtp.mail.ru"
smtp_port = 465
smtp_user = "post@pe4en1e.ru"
smtp_password = os.getenv("SMTP_PASSWORD")

sender_email = "post@pe4en1e.ru"

def random_code():
    code = ""
    for i in range(5):
        code += str(randint(0, 9))
    return str(code)

subject = "Your verification code"

@app.route('/mail/send')
def sendMail():
    recipient_email = request.args.get("to")
    print(recipient_email)

    verification_code = random_code()
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Verification Code</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .email-container {{
                max-width: 600px;
                margin: 20px auto;
                background: #ffffff;
                border: 1px solid #dddddd;
                border-radius: 8px;
                overflow: hidden;
            }}
            .email-header {{
                background-color: #545ACA;
                color: #ffffff;
                text-align: center;
                padding: 20px;
            }}
            .email-body {{
                padding: 20px;
                color: #333333;
                line-height: 1.6;
            }}
            .verification-code {{
                font-size: 24px;
                font-weight: bold;
                color: #545ACA;
                text-align: center;
                margin: 20px 0;
            }}
            .email-footer {{
                text-align: center;
                padding: 10px;
                background-color: #f9f9f9;
                color: #888888;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="email-header">
                <h1>Verification Code</h1>
            </div>
            <div class="email-body">
                <p>Dear user,</p>
                <p>Thank you for registering with us. Please use the following verification code to complete your registration:</p>
                <div class="verification-code">{code}</div>
                <p>If you did not request this code, please ignore this email.</p>
            </div>
            <div class="email-footer">
                &copy; 2025 PollFlow
            </div>
        </div>
    </body>
    </html>
    """.format(code=verification_code)

    message = MIMEMultipart("alternative")
    message["From"] = "pluto <post@pe4en1e.ru>"
    message["To"] = recipient_email
    message["Subject"] = subject

    mime_html = MIMEText(html_content, "html")
    message.attach(mime_html)

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        return verification_code
    except Exception as e:
        return "error"



if __name__ == "__main__":
    app.run(debug=True, port=6090, host='0.0.0.0')
