import logging
import logging.handlers


class TextboxHandler(logging.Handler):
    def __init__(self, textbox):
        logging.Handler.__init__(self)
        self.textbox = textbox

    def emit(self, record):
        msg = self.format(record)
        self.textbox.insert("end", f"{record.asctime}:{record.levelname}: {record.getMessage()}\n")


def log_init(window, text):
    # logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s',
    #                     handlers=[logging.StreamHandler(), logging.FileHandler('actool.log', delay=True)])
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    logger.addHandler(logging.FileHandler('actool.log', delay=True))
    logger.handlers[0].setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    handler = TextboxHandler(text)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    log = logging
    return log
