import os
import time
import re
import logging

try:
    import colorlog
except:
    colorlog = None

from logging import getLogger, Formatter, StreamHandler, LoggerAdapter
from logging.handlers import BaseRotatingHandler

curdir = os.path.abspath(os.path.dirname(__file__))
logsdir = os.path.join(curdir, 'logfiles')
if not os.path.exists(logsdir):
    os.mkdir(logsdir)

# import werkzeug.serving
# 防止flask 对日志加控制台颜色； 输出到文件后可能会有一些不必要的颜色信息
# 调用链 [send_response, python3.6/site-packages/werkzeug/serving.py:332] -> [log_request, serving.py:373] -> [log, serving.py:384] -> [_log, _internal.py:88]
# 其中log_request函数会对 msg 用termcolor模块加控制台颜色
os.environ['ANSI_COLORS_DISABLED'] = 'true'

# FLASK_DEBUG 模式下 会出现多日志问题werkzeug 造成
# _internal.py:85 执行时间有可能早于root创建时间 就会增加StreamHandler 和root的StreamHandler冲突
werkzeug = logging.getLogger('werkzeug')
werkzeug.setLevel(logging.NOTSET)
werkzeug.handlers.clear()

_loggers = {}


def get_logger(name=None, filename='default', clear_handlers=False, userid_format=False):
    name = name or filename
    key = "{}{}".format(name, filename)
    if not clear_handlers and key in _loggers:
        logger = _loggers[key]
        assert isinstance(logger, LoggerAdapter)
        return logger

    filepath = os.path.join(curdir, 'logfiles', filename)

    if userid_format:
        formatter = '%(asctime)s|%(process)d|%(filename)s|nm:%(lineno)d|%(levelname)s|%(userid)s|%(message)s'
    else:
        formatter = '%(asctime)s|%(process)d|%(filename)s|nm:%(lineno)d|%(levelname)s|%(message)s'
    formatter_color = '%(log_color)s' + formatter

    logger = logging.getLogger(name)
    # 防止信息往上级传递 eg: root loger
    # 如果配置上级logger，就会输出两边
    logger.propagate = False
    if clear_handlers:
        logger.handlers.clear()

    # 控制台
    if colorlog:
        handler = colorlog.StreamHandler()
        fmt = colorlog.ColoredFormatter(formatter_color,
                                        datefmt=None,
                                        reset=True,
                                        log_colors={
                                            'DEBUG': 'cyan',
                                            'INFO': 'green',
                                            'WARNING': 'yellow',
                                            'ERROR': 'red',
                                            'CRITICAL': 'red,bg_white',
                                        },
                                        secondary_log_colors={
                                            # 'message': {
                                            #     'ERROR': 'yellow',
                                            #     'CRITICAL': 'yellow'}
                                        })
    else:
        fmt = Formatter(formatter)
        handler = StreamHandler()
    handler.setFormatter(fmt)
    logger.addHandler(handler)

    if filename:
        keep_days = 365

        # 日志文件 按日期划分 DEBUG 开发使用
        fileTimeHandler = SafeDaysRotatingFileHandler(filepath + '.debug.log', backup_count=keep_days)
        fileTimeHandler.setFormatter(Formatter(formatter))
        fileTimeHandler.setLevel(logging.DEBUG)
        non_error_filter = logging.Filter()
        non_error_filter.filter = lambda record: record.levelno < logging.INFO
        fileTimeHandler.addFilter(non_error_filter)
        logger.addHandler(fileTimeHandler)

        # 日志文件 按日期划分 INFO 生产使用
        fileTimeHandler = SafeDaysRotatingFileHandler(filepath + '.info.log', backup_count=keep_days)
        fileTimeHandler.setFormatter(Formatter(formatter))
        fileTimeHandler.setLevel(logging.INFO)
        non_error_filter = logging.Filter()
        non_error_filter.filter = lambda record: record.levelno < logging.WARNING
        fileTimeHandler.addFilter(non_error_filter)
        logger.addHandler(fileTimeHandler)

        # 日志文件 按日期划分  ERROR 生产使用
        fileTimeHandler = SafeDaysRotatingFileHandler(filepath + '.error.log', backup_count=keep_days)
        fileTimeHandler.setFormatter(Formatter(formatter))
        fileTimeHandler.setLevel(logging.ERROR)
        logger.addHandler(fileTimeHandler)

        logger.setLevel(logging.DEBUG)

    # LoggerAdapter 每个用户可以持有一个adapter. 便可添加额外信息
    # new_loger=LoggerAdapter(logger.logger, {'userid':'guest'})
    _loggers[key] = logger = LoggerAdapter(logger, {'userid': 'default'})
    assert isinstance(logger, LoggerAdapter)
    return logger


class SafeDaysRotatingFileHandler(BaseRotatingHandler):

    def __init__(self, filename, backup_count=0, encoding=None, delay=False):
        self.suffix = "%Y%m%d"
        self.extMatch = re.compile(r"^\d{4}\d{2}\d{2}(\.\w+)?$")

        # self.suffix = "%Y%m%d_%H%M"
        # self.extMatch = re.compile(r"^\d{4}\d{2}\d{2}_\d{2}\d{2}(\.\w+)?$")

        self._cur_suffix = self.cur_suffix
        BaseRotatingHandler.__init__(self, filename + self._cur_suffix, 'a', encoding, delay)
        self.backup_count = backup_count
        self._baseFilename = self.baseFilename[:-len(self._cur_suffix)]
        self.delete_old_files()

    @property
    def cur_suffix(self):
        return "." + time.strftime(self.suffix, time.localtime())

    @property
    def cur_filename(self):
        return self._baseFilename + self.cur_suffix

    def shouldRollover(self, record):
        """
        Determine if rollover should occur.

        record is not used, as we are just comparing times, but it is needed so
        the method signatures are the same
        """
        if self._cur_suffix != self.cur_suffix or not os.path.exists(self.cur_filename):
            return 1
        else:
            return 0

    def delete_old_files(self):
        """
        Determine the files to delete when rolling over.

        More specific than the earlier method, which just used glob.glob().
        """
        dirName, baseName = os.path.split(self._baseFilename)
        fileNames = os.listdir(dirName)

        result = []
        prefix = baseName + "."
        plen = len(prefix)
        for fileName in fileNames:
            if fileName[:plen] == prefix:
                suffix = fileName[plen:]
                if self.extMatch.match(suffix):
                    result.append(os.path.join(dirName, fileName))
        result.sort()
        if self.backup_count > 0 and len(result) > self.backup_count:
            result = result[:len(result) - self.backup_count]
            for s in result:
                try:
                    os.remove(s)
                except:
                    pass

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None

        self.baseFilename = self.cur_filename
        self.mode = 'a'
        if not self.delay:
            self.stream = self._open()
        self._cur_suffix = self.cur_suffix
        self.delete_old_files()


if __name__ == '__main__':
    from multiprocessing import Process

    Process(target=lambda e:e, name='batch_encode')

    a = get_logger(filename='test1')
    # while True:
    a.debug('debug')
    a.info('info')
    a.warning('warning')
    a.error('error')
    a.critical('critical')
    time.sleep(0.1)
