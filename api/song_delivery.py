import subprocess
import ssl
import smtplib
import configparser
import os

from api.models import Track, Purchase, Customer


def upload_song(track: Track) -> str:
    cmd = ["ffsend", "upload", track.mp3.path]
    print("Sending song:", cmd)
    ffsend = subprocess.check_output(cmd)
    link = ffsend.decode("utf-8").split(" ")[3]
    return link


def send_download_email(link: str, to: Customer):
    """actually send an email for a particular file"""
    config_filename = os.path.join(os.path.dirname(__file__), 'config.ini')

    # load config
    config = configparser.ConfigParser()
    config.read(config_filename)
    
    email_credentials_file = os.path.join(os.path.dirname(__file__),
                                          'email_credentials.txt')

    with open(email_credentials_file, 'r') as f:
        src_email = f.readline().strip()
        password = f.readline()

    message = get_message([link], config, src_email, to.email)

    # establish connection to smtp server
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(src_email, password)
        server.sendmail(src_email, to.email, message)

def send_song(purchase: Purchase) -> str:
    link = upload_song(purchase.track)
    send_download_email(link, purchase.buyer)
    purchase.status = "fufilled"
    purchase.save()

    return link

def get_message(links, config, src_email, dest_email):
    """format email and add headers"""
    message = ''

    message += f'To: {dest_email}\n'
    message += f'From: {config["Email"]["name"]} <{src_email}>\n'
    message += f'Subject: {config["Email"]["subject"]}\n\n'
    message += 'Thank you for purchasing music. Here are the download links:\n\n'
    message += '\n'.join(links)

    return message
