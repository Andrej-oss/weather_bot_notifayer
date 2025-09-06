from datetime import datetime, timedelta, time
import asyncio


class Scheduler:
    def __init__(self, app, job, tz, hour):
        self.app = app
        self.job = job
        self.tz = tz
        self.hour = hour

    def schedule(self):
        self.app.job_queue.run_daily(
            lambda ctx: asyncio.create_task(self.job(ctx)),
            time=time(self.hour, 0, tzinfo=self.tz),
            days=(0, 1, 2, 3, 4, 5, 6),
            name="daily_wind_report",
        )
        print(f"Заплановано щодня о {self.hour:02d}:00 {self.tz}")

