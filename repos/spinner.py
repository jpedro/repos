import os
import time


class Spinner:
    CHARS = ['⠏', '⠛', '⠹', '⠼', '⠶', '⠧']

    active = None
    index = 0

    @classmethod
    def start(cls, text):
        cls.active = True
        os.system("tput civis")
        while True:
            for i in range(len(cls.CHARS)):
                if not cls.active:
                    return

                cls.index += 1
                if cls.index > 1:
                    os.system("tput cuu1")
                print(f"\r\033[32;1m{cls.CHARS[i]}\033[0m {text}", end=None)
                time.sleep(0.1)

    @classmethod
    def stop(cls):
        cls.active = False
        os.system("tput cuu1")
        os.system("tput el")
        cls.show()

    @classmethod
    def show(cls):
        os.system("tput cvvis")

    # @classmethod
    # def __call__(cls, fn):
    #     print(f"__CALL__")
    #     return fn

    # # @classmethod
    # def __enter__(cls):
    #     print(f"__ENTER__")

    # # @classmethod
    # def __exit__(cls):
    #     print(f"__EXIT__")
