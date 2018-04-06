import itertools
from event import Event
from event import EventKind
from channel import Channel
from channel_handler import ChannelHandler


intensity = 0.5
channel_count = 2
stop_time = 10.0

channels = [
    Channel(capacity=2, passage_time=lambda: 1.0, block_time=lambda: 4.0)
    for _ in range(channel_count)
]
handler = ChannelHandler(intensity, stop_time, channels)
history = list(
    filter(lambda time_count: time_count[1] is not 0, handler)
)

print(history)
