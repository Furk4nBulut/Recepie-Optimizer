from django.shortcuts import render
import threading
import time
from django.shortcuts import render
from .models import Task

def index(request):
    task1 = Task.objects.create(

        name="Malzemeleri Hazırla",
        description="Tüm malzemeleri masaya diz ve hazırla.",
        time_needed=3
    )

    task2 = Task.objects.create(
        name="Fırını Isıt",
        description="Fırını 200 dereceye ayarla ve ısıt.",
        time_needed=1,
        prerequisite=task1
    )

    task3 = Task.objects.create(
        name="Yemeği Fırına Ver",
        description="Hazırlanan yemeği fırına koy ve 30 dakika pişir.",
        time_needed=5,
        prerequisite=task2
    )

    return render(request, 'index.html')



def run_task(task):
    if task.prerequisite and task.prerequisite.state != 'COMPLETED':
        return

    task.state = 'IN_PROGRESS'
    task.save()

    time.sleep(task.time_needed * 60)  # Dakikaları saniyeye çevirme

    task.state = 'COMPLETED'
    task.save()


def start_tasks_in_parallel():
    tasks = Task.objects.all()

    threads = []
    for task in tasks:
        thread = threading.Thread(target=run_task, args=(task,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def start_tasks(request):
    threading.Thread(target=start_tasks_in_parallel).start()

    return render(request, 'task.html', {'tasks': Task.objects.all()})

