import logging
import time


class ExampleAction:
    def __init__(self, configuration):
        self.configuration = configuration

    def perform(self):
        logging.info('perform example action')
        time.sleep(5)
        logging.info('finish example action')
        return self.configuration
