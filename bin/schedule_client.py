from datetime import datetime
import api_util
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import app_start


class Scheduler:
    def __init__(self):
        # Grab Schedule from API
        self.api_client_cls = api_util.ApiClient()
        self.app_schedule_dict = self.api_client_cls.get_app_schedules()
        scheduler = AsyncIOScheduler()
        scheduler.add_job()

    def update_app_schedule(self):
        """Method to be used to update the scheduler with up to date application run schedules"""
        new_schedule = self.api_client_cls.get_app_schedules()


