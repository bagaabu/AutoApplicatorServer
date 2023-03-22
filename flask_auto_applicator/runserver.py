# coding=utf-8
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# init root logger
# 修改flask日志输出默认行为--使其最终输出到日志文件和控制台
# Flask框架在处理完请求后，调用了werkzeug库的_log函数；用的root loger即name=None
# apps.logger.debug('a') 用的是名称为flask.app的logger
from log import get_logger

logger = get_logger(clear_handlers=True)

from flask import Flask

app = Flask(__name__)

from setting import config

app.config.from_object(config)

from app.applicator import collect_info

app.add_url_rule('/collect_info', view_func=collect_info, methods=["POST", "GET"])


# 打印urls映射
url_map = list(sorted(app.url_map.iter_rules(), key=lambda e: str(e)))
urlstring = "\n".join([repr(k) for k in url_map])
logger.info("\n" + urlstring + '\n')

if "gevent" in os.environ.get('GUNICORN_CMD_ARGS', ''):
    from gevent import monkey
    flag = monkey.patch_all(subprocess=True)
    print(flag)

if __name__ == '__main__':
    pass