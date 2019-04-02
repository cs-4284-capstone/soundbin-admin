import subprocess

from api.models import Track, Purchase, Customer


def upload_song(track: Track) -> str:
    cmd = ["ffsend", "upload", track.mp3.path]
    print("Sending song:", cmd)
    ffsend = subprocess.check_output(cmd)
    link = ffsend.decode("utf-8").split(" ")[3]
    return link


def send_download_email(link: str, to: Customer):
    print("pretending to send download email to: ", to.email) # TODO


def send_song(purchase: Purchase) -> str:
    link = upload_song(purchase.track)
    send_download_email(link, purchase.buyer)
    purchase.status = "fufilled"
    purchase.save()

    return link
