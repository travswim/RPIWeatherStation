from subprocess import call

import time
import os

from apscheduler.schedulers.background import BackgroundScheduler


def job():
    print("In job")


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    # scheduler.configure(timezone=utc)
    scheduler.add_job(job, 'cron', second=10)
    # scheduler.add
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()