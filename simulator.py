import threading
import time
import json

LOOP_INTERVAL_SECOND = 1

output = {"wind_power": 0, "solar_power": 0, "water_power": 0}


class Simulator:
    def __init__(self):
        self.callbacks = list()
        self.__ser = None
        self.__solar_power = None
        self.__loop = threading.Thread(target=self.thread, args=())
        self.__lock = threading.Lock()
        self.__stop_event = threading.Event()
        self.__stop_event.clear()
        self.__loop.start()
        self.__running = False

    def run(self):
        print("Simulator started")
        self.__running = True

    def stop(self):
        self.__running = False
        print("Simulator stopped")

    def kill(self):
        self.__running = False
        self.__stop_event.set()

    def thread(self):
        while not self.__stop_event.is_set():
            try:
                time.sleep(LOOP_INTERVAL_SECOND)
                if not self.__running:
                    continue
                if self.__solar_power is not None:
                    self.__solar_power -= 1
                    for callback in self.callbacks:
                        output["solar_power"] = self.__solar_power
                        callback(json.dumps(output))
            except Exception as e:
                pass
        print("Simulator stopped")

    def register_callback(self, callback):
        self.callbacks.append(callback)

    def unregister_callback(self, callback):
        self.callbacks.remove(callback)

    def set_solar_power(self, solar_power):
        with self.__lock:
            self.__solar_power = solar_power
