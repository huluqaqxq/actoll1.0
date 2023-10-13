import logging as log


def log_init():
    log.basicConfig(level=log.INFO, format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[log.StreamHandler(), log.FileHandler('actool.log', delay=True)])
    return log
