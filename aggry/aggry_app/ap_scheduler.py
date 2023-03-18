from datetime import datetime, date
from django.core.cache import cache
from apscheduler.schedulers.background import BackgroundScheduler
import os
import time


# def periodic_execution(): # 任意の関数名
#     # ここに定期実行したい処理を記述する
#     os.system('ls')
#     os.chdir('jobs')
#     if not cache.get('is_job_running'):
#         cache.set('is_job_running', True)
#         os.system('scrapy crawl conma')
#     if not cache.get('is_job_running'):
#         cache.set('is_job_running', True)
#         os.system('scrapy crawl oreyume')
#     if not cache.get('is_job_running'):
#         cache.set('is_job_running', True)
#         os.system('scrapy crawl copro')
#     os.chdir('../')

import subprocess

def periodic_execution():
    os.chdir('jobs')
    
    spider_process1 = subprocess.Popen(['scrapy', 'crawl', 'conma'])
    spider_process1.wait()
    
    spider_process2 = subprocess.Popen(['scrapy', 'crawl', 'oreyume'])
    spider_process2.wait()
    
    spider_process3 = subprocess.Popen(['scrapy', 'crawl', 'copro'])
    spider_process3.wait()
    
    os.chdir('../')
    subprocess.Popen(['python', 'clustering.py'])


# スケジュールの設定
def start():
    scheduler=BackgroundScheduler()
    scheduler.add_job(periodic_execution, 'cron', hour=18, minute=3)
    scheduler.start()