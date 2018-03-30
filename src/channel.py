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
        if self._wait_time > 0.0:
            return 0

        self._wait_time = None

        count = self._count
        self._count = 0
        return count

    def _is_empty(self) -> bool:
        return self._count == 0

    def _is_occupied(self) -> bool:
        return self._count == 1

    def _is_blocked(self) -> bool:
        return self._count >= 2

    def is_waiting(self) -> bool:
        return self._wait_time is not None

    def try_enter(self) -> bool:
        if self._is_empty():
            self._wait_time =  self._passage_time
        elif self._is_occupied():
            self._wait_time += self._block_time
        elif self._is_blocked():
            return False
        else:
            raise NotImplementedError

        self._count += 1
        return True
