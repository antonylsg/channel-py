from enum import Enum
from typing import Any
from typing import List
from typing import Tuple
from typing import Union
from typing import Callable
from typing import Iterable
import math
import random
import itertools


def find(predicate: Callable[..., bool], iterable: Iterable):
    for item in filter(predicate, iterable):
        return item
    return None


class EventKind(Enum):
    ENTER = 0
    RELEASE = 1


class Event:
    def __init__(self, kind: EventKind, time: float) -> None:
        self._kind = kind
        self._time = time

    @property
    def kind(self):
        return self._kind

    @property
    def time(self):
        return self._time


class Channel:
    def __init__(self, passage_time=1.0, block_time=2.0):
        self._wait_time: Union[None, float] = None
        self._passage_time = passage_time
        self._block_time = block_time
        self._count = 0

    def wait_time(self):
        return self._wait_time

    def forward(self, step_time: float):
        if self._wait_time is None:
            return 0

        self._wait_time -= step_time
        return self.release()

    def is_empty(self):
        return self._count == 0

    def is_occupied(self):
        return self._count == 1

    def is_blocked(self):
        return self._count >= 2

    def is_waiting(self):
        return self._wait_time is not None

    def enter(self):
        if self.is_empty():
            self._wait_time =  self._passage_time
        elif self.is_occupied():
            self._wait_time += self._block_time
        else: # self.is_blocked():
            return

        self._count += 1

    def release(self):
        """Free the channel and return the number of released particules"""

        if self._wait_time > 0.0:
            return 0
        
        self._wait_time = None

        count = self._count
        self._count = 0
        return count


class ChannelHandler:
    def __init__(self, intensity: float, stop_time: float, channels: List[Channel]) -> None:
        self._time = 0.0
        self._next_enter_event: Union[None, float] = None
        self._inv_intensity = 1.0 / float(intensity)
        self._stop_time = stop_time
        self._channels = channels.copy()

    def __iter__(self):
        return self

    def __next__(self):
        if self._time > self._stop_time:
            raise StopIteration
        else:
            count = self.next_step()
            return (self._time, count)

    def next_event(self):
        if self._next_enter_event is None:
            rand = random.random()
            self._next_enter_event = -math.log(rand) * self._inv_intensity

        waiting_channels = filter(Channel.is_waiting, self._channels)
        wait_times = map(Channel.wait_time, waiting_channels)
        min_wait_time = min(wait_times, default=None)

        if min_wait_time is None or self._next_enter_event <= min_wait_time:
            return Event(EventKind.ENTER, self._next_enter_event)

        return Event(EventKind.RELEASE, min_wait_time)

    def forward(self, step_time: float):
        self._time += step_time
        self._next_enter_event -= step_time

        if self._next_enter_event <= 0.0:
            self._next_enter_event = None

    def next_step(self):
        event = self.next_event()
        self.forward(event.time)

        # Make the event happen right now!!!
        forward = lambda channel: channel.forward(event.time)
        released = sum(map(forward, self._channels))

        if event.kind == EventKind.ENTER:
            random.shuffle(self._channels)
            is_not_blocked = lambda channel: not channel.is_blocked()
            channel = find(is_not_blocked, self._channels)
            if channel is not None:
                channel.enter()

        return released


if __name__ is '__main__':
    intensity = 0.5
    channel_count = 2
    stop_time = 10.0

    channels = list(itertools.repeat(
        Channel(passage_time=1.0, block_time=2.0), channel_count
    ))
    handler = ChannelHandler(intensity, stop_time, channels)
    history = list(
        filter(lambda time_count: time_count[1] is not 0, handler)
    )

    print(history)
