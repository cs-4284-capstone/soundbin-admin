import subprocess
import ssl
import smtplib
import configparser
import os

from api.models import Track, Purchase, Customer


EMAIL_SRC_EMAIL = os.getenv("EMAIL_SRC_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_HOST = os.getenv("EMAIL_HOST")


def upload_song(track: Track) -> str:
    cmd = ["ffsend", "upload", "--api", "3", track.mp3.path]
    print("Sending song:", cmd)
    ffsend = subprocess.check_output(cmd)
    link = ffsend.decode("utf-8").split(" ")[3]
    return link


def send_download_email(link: str, purchase: Purchase):
    to = purchase.buyer

    """actually send an email for a particular file"""
    config_filename = os.path.join(os.path.dirname(__file__), 'config.ini')

    # load config
    config = configparser.ConfigParser()
    config.read(config_filename)
    
    """
    email_credentials_file = os.path.join(os.path.dirname(__file__),
                                          'email_credentials.txt')

    with open(email_credentials_file, 'r') as f:
        src_email = f.readline().strip()
        password = f.readline()
    """

    message = get_message([link], config, EMAIL_SRC_EMAIL, purchase)

    # establish connection to smtp server
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(EMAIL_HOST, 465, context=context) as server:
        server.login(EMAIL_SRC_EMAIL, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SRC_EMAIL, to.email, message)

def send_song(purchase: Purchase) -> str:
    link = upload_song(purchase.track)
    send_download_email(link, purchase)
    purchase.status = "fufilled"
    purchase.save()

    return link

def get_message(link: str, config, src_email, purchase: Purchase):
    """format email and add headers"""
    message = ''

    message += f'To: {purchase.buyer.email}\n'
    message += f'From: {config["Email"]["name"]} <{src_email}>\n'
    message += f'Subject: {config["Email"]["subject"]}\n\n'
    message += f"""
    Your purchase from Soundbin has been completed! 
    You purchased the following track:
    
    {purchase.track} - SYS {purchase.track.price}
    
    Follow the Firefox Send link below to download your purchased content:
    
    {link}

    This link will expire after being clicked, so make sure you save the content as soon as possible.
    """

    return message
