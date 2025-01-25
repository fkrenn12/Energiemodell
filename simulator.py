import threading
import time


class Simulator:
    def __init__(self):
        self.callbacks = list()
        self.__ser = None
        self.__solar_power = None
        self.__loop = threading.Thread(target=self.thread, args=())
        self.__lock = threading.Lock()
        self.__stop_event = threading.Event()

    def start(self):
        self.__stop_event.clear()
        self.__loop.start()
        print("Simulator started")

    def stop(self):
        self.__stop_event.set()

    def thread(self):
        while not self.__stop_event.is_set():
            try:
                time.sleep(2)
                if self.__solar_power is not None:
                    self.__solar_power -= 1
                    for callback in self.callbacks:
                        callback(str(self.__solar_power))
            except Exception as e:
                pass

    def register_callback(self, callback):
        self.callbacks.append(callback)

    def unregister_callback(self, callback):
        self.callbacks.remove(callback)

    def set_solar_power(self, solar_power):
        with self.__lock:
            self.__solar_power = solar_power
