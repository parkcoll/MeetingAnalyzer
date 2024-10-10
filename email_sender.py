import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import io

def send_email_report(email, figs):
    try:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = 'your_email@example.com'  # Replace with your email
        msg['To'] = email
        msg['Subject'] = 'Weekly Calendar Analysis Report'

        # Add text content
        text = "Here's your weekly calendar analysis report. Please find the visualizations attached below."
        msg.attach(MIMEText(text, 'plain'))

        # Add visualizations as inline images
        for i, fig in enumerate(figs):
            img_bytes = fig.to_image(format="png")
            img = MIMEImage(img_bytes)
            img.add_header('Content-ID', f'<image{i}>')
            msg.attach(img)

        # Create the HTML content with embedded images
        html = "<html><body>"
        for i in range(len(figs)):
            html += f'<img src="cid:image{i}"><br><br>'
        html += "</body></html>"
        msg.attach(MIMEText(html, 'html'))

        # Send the email
        smtp_server = "smtp.gmail.com"  # Replace with your SMTP server
        smtp_port = 587
        smtp_username = "your_email@example.com"  # Replace with your email
        smtp_password = "your_password"  # Replace with your email password or app-specific password

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)

        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
