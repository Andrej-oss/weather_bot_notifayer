from datetime import datetime, timedelta
import pytz


class Scheduler:
    def __init__(self, app, job, tz, hour):
        self.app = app
        self.job = job
        self.tz = tz
        self.hour = hour

    def schedule(self):
        now_local = datetime.now(self.tz)
        run_time_local = now_local.replace(hour=self.hour, minute=0, second=0, microsecond=0)
        if run_time_local <= now_local:
            run_time_local += timedelta(days=1)

        self.app.job_queue.run_daily(
            self.job,
            time=run_time_local.timetz(),
            days=(0,1,2,3,4,5,6),
            name="daily_wind_report",
            timezone=self.tz,
        )
        print(f"Заплановано щодня о {self.hour:02d}:00 {self.tz}")
