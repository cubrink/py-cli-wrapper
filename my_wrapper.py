# https://stackoverflow.com/questions/4022600/python-pty-fork-how-does-it-work

import sys
import os
import time
import pty
import random


class CliWrapper:
    """Provides an read -> input -> read ... interface for interacting with interactive CLI applications"""
    def __init__(self, child_fd, page_size=-1, delay=0.1, ignore_last_line=False):
        """Initializes a CliWrapper object

        Args:
            child_fd: File descriptor of child process
            page_size (int, optional): Max size of page. Unlimited by default.
            delay (float, optional): Time given for child process to respond to input. Defaults to 0.1.
            ignore_last_line (bool, optional): Set to remove input prompt from page. Defaults to False.
        """
        self.child_fd = child_fd
        self.delay = delay
        self.page_size = page_size
        self.ignore_last_line = ignore_last_line

        time.sleep(self.delay)
        self.page = self._read()

    def input(self, text):
        """Send text to the child process"""
        if isinstance(text, str):
            # Convert to bytes
            text = text.encode(encoding='utf-8')
        text = text + b'\n'
        os.write(self.child_fd, text)
        
        # Wait for the child to process the input
        time.sleep(self.delay)

        # Ignore the input we just sent
        os.read(self.child_fd, len(text))

        self._read()

            
    def _read(self):
        """Reads the stdout of the child process"""
        self.page = os.read(self.child_fd, self.page_size).decode('utf-8').replace('\r', '')

        if self.ignore_last_line:
            self.page = self.page[:self.page.rfind('\n')]
        return self.page



if __name__ == "__main__":
    args = ["python", "my_cli.py"]

    try:
        child_pid, fd = pty.fork()  # OK
    except OSError as e:
        print(str(e))

    if (child_pid == 0):
        sys.stdout.flush()
        try:
            #Note: "the first of these arguments is passed to the new program as its own name"
            # so:: "python": actual executable; "ThePythonProgram": name of executable in process list (`ps axf`); "pyecho.py": first argument to executable..
            os.execlp("python","ThePythonProgram","my_cli.py")
        except:
            print("Cannot spawn execlp...")
    else:
        commands = ["help", "hello", "goodbye"]
        my_wrapper = CliWrapper(fd, page_size=2048, ignore_last_line=True)

        # print("On startup:")
        # print(my_wrapper.page)

        # print('------------------')

        # print("Printing 'help' command:")
        # my_wrapper.input("help")
        # print(my_wrapper.page)

        # print('------------------')

        # print("Printing 'hello' command:")
        # my_wrapper.input("hello")
        # print(my_wrapper.page)

