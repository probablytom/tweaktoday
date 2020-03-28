from .models import TaskSuggestion, Mission
from django.db.models.functions import Trunc
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
import datetime

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')

@scheduler.scheduled_job("interval",
                         seconds=(60*60*24),
                         next_run_time=(datetime.date.today()+datetime.timedelta(days=1)),
                         id='mission cycler', max_instances=1)
def cycle_current_challenge():
    print("replacing now")
    suggs = sorted(TaskSuggestion.objects.all(), key=lambda s: -s.votes)
    if len(suggs) is 0:
        raise Exception("No new suggestions to pick")

    suggestion = suggs[0]
    new_mission = Mission(task_text=suggestion.task_text, task_explainer=suggestion.task_explainer)
    new_mission.save()
    suggestion.delete()

register_events(scheduler)
scheduler.start()
print("started scheduler")