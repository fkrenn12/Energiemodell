import threading

import serial

DEFAULT_TIMEOUT = 0.1
DEFAULT_BAUDRATE = 115200
DEFAULT_PORT = 'COM1'
MESSAGE_SERIAL_OPENED = 'Serial opened'
MESSAGE_SERIAL_CLOSED = 'Serial closed'
MESSAGE_SERIAL_ERROR = 'Serial error'
MESSAGE_SERIAL_WRITE = 'Serial write'
MESSAGE_UNREGISTERED_CALLBACK = 'Unregistered callback'
MESSAGE_REGISTERED_CALLBACK = 'Registered callback'
MESSAGE_EXCEPTION_SERIAL_READ = 'Exception reading serial'
MESSAGE_EXCEPTION_SERIAL_CALLBACK = 'Exception calling serial callback'


class SerialComm:
    def __init__(self):
        self.callbacks = list()
        self.__ser = None
        self.__loop = threading.Thread(target=self.thread_serial_read_loop, args=())
        self.__lock = threading.Lock()
        self.__stop_event = threading.Event()

    def open(self, port=DEFAULT_PORT, baud_rate=DEFAULT_BAUDRATE):
        self.__ser = serial.Serial(port=port,
                                   baudrate=baud_rate,
                                   timeout=DEFAULT_TIMEOUT)

        self.__stop_event.clear()
        self.__loop.start()
        print(MESSAGE_SERIAL_OPENED)

    def is_open(self):
        return self.__ser is not None and self.__ser.is_open

    def close(self):
        self.__stop_event.set()
        self.__loop.join()
        self.__ser.close()
        self.__ser = None
        print(MESSAGE_SERIAL_CLOSED)

    def register_callback(self, callback):
        print(MESSAGE_REGISTERED_CALLBACK)
        self.callbacks.append(callback)

    def unregister_callback(self, callback):
        print(MESSAGE_UNREGISTERED_CALLBACK)
        self.callbacks.remove(callback)

    def thread_serial_read_loop(self):
        while not self.__stop_event.is_set():
            try:
                payload = self.__ser.readline()
            except Exception as e:
                print(f'{MESSAGE_EXCEPTION_SERIAL_READ} {e}')
                self.__ser.close()
                self.__ser = None
                break

            if payload and self.callbacks:
                for callback in self.callbacks:
                    try:
                        with self.__lock:
                            callback(payload)
                    except Exception as e:
                        print(f'{MESSAGE_EXCEPTION_SERIAL_CALLBACK} {e}')

    def write(self, payload):
        with self.__lock:
            self.__ser.write(payload.encode())
            print(f'{MESSAGE_SERIAL_WRITE} : {payload}')


serial_client = SerialComm()
