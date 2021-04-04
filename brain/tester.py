import os
import pusher

pusher_client = pusher.Pusher("1182764", "92c64299da2189a14546", "4d76a1c2883725c1acdf", cluster='ap1')

pusher_client.trigger(u'drama', u'timeIsUp', {})