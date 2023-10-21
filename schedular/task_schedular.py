from apscheduler.schedulers.background import BackgroundScheduler
from tasks import global_tasks

schedular = BackgroundScheduler()

schedular.add_job(global_tasks.schedular_get_symbols, 'cron', second='*/5')
