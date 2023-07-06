import time


class Stopwatch:
    """
    a class to measure time for running code

    when initialized it starts the timer and with every "round" it prints the time since the last round, resets the timer and
    """

    def __init__(self):
        self.init_time = time.time()
        self.start = self.init_time

    def round(self, event: str):
        """
        - logs the time since the last round or initialization of this class
        - resets the time for next round

        :param event: keyword to find the logged time in the terminal
        """
        stop = time.time()
        difference = stop - self.start
        print(f"Time Spent ({event}): {difference:.5f}s")
        self.start = stop

    def total(self, event: str):
        """
        - logs the time since the initialization
        - is unaffected by `self.round()`
        - does not reset anything

        :param event: keyword to find the logged time in the terminal
        """
        stop = time.time()
        difference = stop - self.init_time
        print(f"Total Time Spent ({event}): {difference:.5f}s")
