from typing import TypeVar, Generic, Callable, List
T = TypeVar('T')


class State(Generic[T]):
    def __init__(self, value: T):
        self._value = value
        self._observers: List[Callable[[T], None]] = []

    def get(self) -> T:
        return self._value

    def set(self, new_value: T):
        if self._value != new_value:
            self._value = new_value
            for observer in self._observers:
                observer(new_value)  # 変更時に各オブザーバーに通知する

    def bind(self, observer: Callable[[T], None]):
        self._observers.append(observer)  # 変更時に呼び出すオブザーバーを登録
