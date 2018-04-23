import math
import random
import itertools
from event import Event
from event import EventKind
from channel import Channel
from channel_handler import ChannelHandler

import numpy as np
import matplotlib 
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt


def poisson(intensity: float):
    inv_intensity = 1.0 / intensity

    def inner():
        rand = random.random()
        return -math.log(rand) * inv_intensity

    return inner


intensity = 4.0
channel_count = 1
stop_time = 40.0

trials = 10_000
bins = 10 * int(stop_time)
# step = stop_time / bins
inv_step = bins / stop_time
histogram = list(itertools.repeat(0, bins))

for _ in range(trials):
    channels = [
        # Channel(capacity=2, passage_time=lambda: 1.0, block_time=lambda: 4.0)
        Channel(capacity=2, passage_time=poisson(1.0), block_time=poisson(4.0))
        for _ in range(channel_count)
    ]
    handler = ChannelHandler(intensity, stop_time, channels)
    history = filter(lambda time_count: time_count[1] is not 0, handler)
    history = filter(lambda time_count: time_count[0] <= stop_time, history)

    for time, count in history:
        idx = int(time * inv_step)
        histogram[idx] += count

x = np.linspace(0.0, stop_time, bins)
y = np.asarray(histogram) * inv_step / trials
plt.plot(x, y, 'red')
plt.xlabel('$t$')
plt.ylabel(r'$\langle J \rangle$')
plt.show()
