#!/usr/bin/env python3
"""
Send a song to an email address

Does not check for validity of transaction, just deals with distributing song
to the user.
"""

import argparse
import ssl
import smtplib
import configparser
import os
import subprocess

def get_message(links, config, src_email, dest_email):
    """format proper message"""
    message = ''

    message += f'To: {dest_email}\n'
    message += f'From: {config["Email"]["name"]} <{src_email}>\n'
    message += f'Subject: {config["Email"]["subject"]}\n\n'
    message += 'Thank you for purchasing music. Here are the download links:\n\n'
    message += '\n'.join(links)

    return message

def firefox_send(files):
    """get firefox send links for each file"""
    links = []

    for song_file in files:
        args = ['send-cli', song_file]
        firefox_send = subprocess.run(args, capture_output=True)
        output_lines = firefox_send.stdout.decode('utf-8').split('\n')
        link = output_lines[-3]
        print(firefox_send)
        print(output_lines)
        print(link)
        links.append(link)

    return links

def links_from_songs(songs, files_config):
    """go from a song name/id to a url to download song"""
    links = []

    # for now, just combine the base url and the song name
    base = files_config['song_dir']
    for song in songs:
        links.append(os.path.join(os.path.dirname(__file__), base, song))

    return firefox_send(links)

def main():
    """Deal with input (called from command line by other software)"""
    config_filename = os.path.join(os.path.dirname(__file__), 'config.ini')

    # load config
    config = configparser.ConfigParser()
    config.read(config_filename)

    # parse command line arguments
    parser = argparse.ArgumentParser(description='Send purchased tracks to an email')
    parser.add_argument('email', help='email address to which tracks are sent')
    parser.add_argument('-s', dest='tracks', nargs='+', help='song or tracks to send')
    args = parser.parse_args()

    dest_email = args.email
    songs = args.songs

    files_config = config['Files']

    # load email credentials
    email_credentials_file = os.path.join(os.path.dirname(__file__),
                                          'email_credentials.txt')

    with open(email_credentials_file, 'r') as f:
        src_email = f.readline().strip()
        password = f.readline()

    links = links_from_songs(songs, files_config)
    message = get_message(links, config, src_email, dest_email)

    # establish connection to smtp server
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(src_email, password)
        server.sendmail(src_email, dest_email, message)

if __name__ == '__main__':
    main()
