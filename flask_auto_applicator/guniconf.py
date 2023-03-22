import os
import json
import socket
import gunicorn


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip.replace('.', '_')


# 监控日志
def post_worker_init(worker):
    flask_app = worker.wsgi
    increment = getattr(worker.log, 'increment', None)
    if callable(increment):
        def get_path_and_source(request):
            path = "url%s" % request.path.replace('/', '_FXG_').replace('.', '_Dot_')
            source = 'UNKNOWN'
            try:
                args = request.get_json(force=True)
                request_id = str(args.get('request_id', ""))
                source_tmp = request_id.split('_')[0]
                if source_tmp.isalpha() and source_tmp.isupper():
                    source = source_tmp
            except:
                pass
            return path, source

        @flask_app.after_request
        def after_request(response):
            http_code = response.status_code
            try:
                yewu_code = json.loads(response.data).get('code', 0)
            except Exception:
                yewu_code = '0'

            from flask import request
            path, source = get_path_and_source(request)
            prefix = "gunicorn.after_request.%s.%s.%s" % (path, source, str(http_code))
            prefix += ".%s" % str(yewu_code)
            try:
                increment(prefix, 1)
            except:
                pass
            return response


# def pre_request(worker, req):
#     _monitor_key = '_monitor_request'
#     if _monitor_key in getattr(req, 'query', ''):
#         increment = getattr(worker.log, 'increment', None)
#         if callable(increment):
#             status = 1000
#             increment("gunicorn.request.status.%d" % status, 1)


worker_class = 'gevent'
bind = "0.0.0.0:7887"
proc_name = 'rotate'
capture_output = True
timeout = 120

statsd_host = '172.16.5.204:8125'
statsd_prefix = "%s.%s.%s" % (os.environ.get('FLASK_ENV', 'development'), proc_name, get_host_ip())
