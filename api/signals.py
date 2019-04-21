import requests

NODEOS_HOST = "http://nodeos:5000" # flask control panel on nodeos

def on_addsong(sender, **kwargs):
    print("on edit song")
    track = kwargs['instance']
    if kwargs['created']:
        print("Sending song info to Nodeos:", track.id, track.price)
        requests.post(f"{NODEOS_HOST}/songs/add/{track.id}/{track.price}")