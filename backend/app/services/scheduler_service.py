from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import asyncio
from app.services.telegram_service import send_telegram_message

scheduler = AsyncIOScheduler()
participant_jobs: dict[int, str] = {}  # participant_id -> job_id
check_in_attempts: dict[int, int] = {}  # participant_id -> attempts

def send_check_in(participant_id: int, user_id: int):
    attempts = check_in_attempts.get(participant_id, 0) + 1
    check_in_attempts[participant_id] = attempts
    print(f"Sending check-in to user {user_id} for participant {participant_id}, attempt {attempts}")
    # Send message to user
    send_telegram_message(str(user_id), f"Проверка безопасности (попытка {attempts}): Вы в безопасности? Ответьте в приложении.")
    
    if attempts >= 3:
        # Escalate to trusted contact
        print(f"Escalating for participant {participant_id}")
        # For now, send alert to self
        send_telegram_message(str(user_id), "Эскалация: Не удалось связаться, уведомление отправлено доверенному лицу.")
        # Remove job
        if participant_id in participant_jobs:
            scheduler.remove_job(participant_jobs[participant_id])
            del participant_jobs[participant_id]
            if participant_id in check_in_attempts:
                del check_in_attempts[participant_id]

# Function to start check-in job for a participant
def start_check_in_job(participant_id: int, user_id: int):
    if participant_id not in participant_jobs:
        job = scheduler.add_job(send_check_in, trigger=IntervalTrigger(minutes=5), args=[participant_id, user_id])
        participant_jobs[participant_id] = job.id
        print(f"Started check-in job for participant {participant_id}")

def init_scheduler():
    scheduler.start()

def shutdown_scheduler():
    scheduler.shutdown()