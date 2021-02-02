# @Author  : Shusheng Wang
# @Time    : 2021/2/2 6:31 下午
# @Email   : lastshusheng@163.com


import multiprocessing

bind = '0.0.0.0:7000'
workers = multiprocessing.cpu_count() * 2 + 1
backlog = 2048
worker_class = "gevent"
daemon = False
debug = True
pidfile = './gunicore.pid'
loglevel = 'info'
accesslog = 'logs/gunicorn.log'
errorlog = 'logs/gunicorn.err'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" "%({X-Real-IP}i)s"'
timeout = 60
