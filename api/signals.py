def on_init():
    print("on init")

def on_addsong(sender, **kwargs):
    print("on add song")
    track = kwargs['instance']
    if kwargs['created']:
        print("sending song to nodeos:", track.id, track.price)