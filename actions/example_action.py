import time


class ExampleAction:
    def __init__(self, configuration):
        self.configuration = configuration

    def perform(self):
        print('perform example action')
        time.sleep(120)
        print('finish example action')
        return self.configuration
