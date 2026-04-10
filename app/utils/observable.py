from typing import Callable, Dict, List


class Observable:
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}

    def add_listener(self, property_name: str, callback: Callable):
        """
        Подписка на изменение конкретного свойства
        :param property_name: Свойство отслеживания
        :param callback: Функция вызова при изменении свойства
        :return:
        """
        if property_name not in self.listeners:
            self.listeners[property_name] = []
        self.listeners[property_name].append(callback)

    def remove_listener(self, property_name: str, callback: Callable):
        """
        Отписка от изменений
        :param property_name: Свойство отслеживания
        :param callback: Функция callback
        :return:
        """
        if property_name in self.listeners:
            self.listeners[property_name].remove(callback)

    def notify(self, property_name: str):
        """
        Уведомление подписчиков об изменении свойства
        :param property_name: Свойство отслеживания
        :return:
        """
        if property_name in self.listeners:
            for callback in self.listeners[property_name]:
                callback(property_name)

