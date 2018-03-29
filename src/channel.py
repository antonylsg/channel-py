from typing import Union
from typing import Callable
from typing import Iterable


class Channel:
    def __init__(self, passage_time=1.0, block_time=2.0):
        self._wait_time: Union[None, float] = None
        self._passage_time = passage_time
        self._block_time = block_time
        self._count = 0

    def wait_time(self) -> Union[None, float]:
        return self._wait_time

    def forward(self, step_time: float) -> int:
        if self._wait_time is None:
            return 0

        self._wait_time -= step_time
        return self.release()

    def is_empty(self) -> bool:
        return self._count == 0

    def is_occupied(self) -> bool:
        return self._count == 1

    def is_blocked(self) -> bool:
        return self._count >= 2

    def is_waiting(self) -> bool:
        return self._wait_time is not None

    def enter(self):
        if self.is_empty():
            self._wait_time =  self._passage_time
        elif self.is_occupied():
            self._wait_time += self._block_time
        else: # self.is_blocked():
            return

        self._count += 1

    def release(self) -> int:
        """Free the channel and return the number of released particules"""

        if self._wait_time > 0.0:
            return 0
        
        self._wait_time = None

        count = self._count
        self._count = 0
        return count
