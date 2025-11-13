import requests

def send_email(to_email, subject, html_content):
    url = "https://api.sendinblue.com/v3/smtp/email"
    headers = {
        "api-key": "YOUR_SENDINBLUE_API_KEY",  # Replace with your key
        "Content-Type": "application/json"
    }
    data = {
        "sender": {"name": "Task Manager", "email": "your-email@example.com"},
        "to": [{"email": to_email}],
        "subject": subject,
        "htmlContent": html_content
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.status_code, response.text)
