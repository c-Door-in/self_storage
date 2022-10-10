import smtplib
import os
import qrcode
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from platform import python_version
from email import encoders
from dotenv import load_dotenv


def get_qr_code(storage_id, box_id, user_id):

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f'Информация о Ваших складах: Номер склада: {storage_id}, номер бокса: {box_id}, ваш идентификатор: {user_id}')
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    image_name = f'qrcode{user_id}{box_id}.jpg'
    img.save(image_name, "JPEG")

    return image_name


def send_email(recepient, subject, message, qr_file=None):
    load_dotenv()
    server = 'smtp.gmail.com'
    user = os.getenv('SENDER')
    password = os.getenv('EMAIL_PASSWORD')

    recipient = recepient
    sender = 'devmanselfstorage@gmail.com'
    subject = subject
    text = message

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['To'] = recipient
    msg['Reply-To'] = sender
    msg['Return-Path'] = sender
    msg['X-Mailer'] = 'Python/' + (python_version())

    if qr_file:
    
        file_path = os.path.abspath(qr_file)

        if os.path.exists(file_path):
            basename = os.path.basename(file_path)
            filesize = os.path.getsize(file_path)
            part_file = MIMEBase('application', 'octet-stream; name="{}"'.format(basename))
            part_file.set_payload(open(file_path, "rb").read())
            part_file.add_header('Content-Description', basename)
            part_file.add_header('Content-Disposition', 'attachment; filename="{}"; size={}'.format(basename, filesize))
            encoders.encode_base64(part_file)
            msg.attach(part_file)

    part_text = MIMEText(text, 'plain')
    msg.attach(part_text)

    mail = smtplib.SMTP_SSL(server)
    mail.login(user, password)
    mail.sendmail(sender, recipient, msg.as_string())
    mail.quit()


