import logging

class YtDlpLogger:
    '''
    A proxy logger for yt-dlp
    '''
    
    LOGGER=logging.getLogger(__name__)

    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith('[debug] '):
            self.LOGGER.debug(msg)
        else:
            self.info(msg)

    def info(self, msg):
        self.LOGGER.info(msg)

    def warning(self, msg):
        self.LOGGER.warn(msg)

    def error(self, msg):
        self.LOGGER.error("@5" + msg)