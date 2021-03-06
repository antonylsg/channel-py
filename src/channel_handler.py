import math
import random
from typing import Any, Callable, Iterable, List, Union

from channel import Channel
from event import Event, EventKind


def find(
    predicate: Union[None, Callable[..., bool]], iterable: Iterable
) -> Union[None, Any]:
    for item in filter(predicate, iterable):
        return item
    return None


class ChannelHandler:
    def __init__(
        self, intensity: float, stop_time: float, channels: List[Channel]
    ) -> None:
        rand = random.random()

        self._time = 0.0
        self._inv_intensity = 1.0 / float(intensity)
        self._next_enter_event = -math.log(rand) * self._inv_intensity
        self._stop_time = stop_time
        self._channels = channels

    def __iter__(self):
        return self

    def __next__(self):
        if self._time > self._stop_time:
            raise StopIteration
        else:
            count = self._next_step()
            return (self._time, count)

    def _next_event(self) -> Event:
        waiting_channels = filter(Channel.is_waiting, self._channels)
        wait_times = map(Channel.wait_time, waiting_channels)
        min_wait_time = min(wait_times, default=None)

        if min_wait_time is None or self._next_enter_event <= min_wait_time:
            return Event(EventKind.ENTER, self._next_enter_event)

        return Event(EventKind.RELEASE, min_wait_time)

    def _forward(self, step_time: float):
        self._time += step_time
        self._next_enter_event -= step_time

        if self._next_enter_event <= 0.0:
            rand = random.random()
            self._next_enter_event = -math.log(rand) * self._inv_intensity

    def _next_step(self) -> int:
        event = self._next_event()
        self._forward(event.time)

        # Make the event happen right now!!!
        def forward(channel):
            return channel.forward(event.time)

        released = sum(map(forward, self._channels))

        if event.kind == EventKind.ENTER:
            random.shuffle(self._channels)
            find(None, map(Channel.try_enter, self._channels))

        return released
