# ============ FILE: medication-service/app/services/notification_scheduler.py ============
from datetime import datetime
from typing import Dict, List

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import joinedload

from app.models.reminder import Reminder
from app.models.device_token import DeviceToken
from app.services.db import SessionLocal
from app.services.push_service import send_push

_scheduler = None
_fired_cache = set()


def _day_key(dt: datetime) -> str:
    return ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"][dt.weekday()]


def _should_fire(reminder: Reminder, now: datetime) -> bool:
    if not reminder.is_active or not reminder.scheduled_time:
        return False

    days = reminder.days_of_week or []
    if days and _day_key(now) not in [d.lower() for d in days]:
        return False

    if reminder.scheduled_time.hour != now.hour or reminder.scheduled_time.minute != now.minute:
        return False

    fire_key = f"{reminder.id}-{now.date()}-{now.hour}:{now.minute}"
    if fire_key in _fired_cache:
        return False

    _fired_cache.add(fire_key)
    if len(_fired_cache) > 2000:
        _fired_cache.clear()

    return True


def _collect_tokens(db, user_ids: List[int]) -> Dict[int, List[str]]:
    if not user_ids:
        return {}

    tokens = db.query(DeviceToken).filter(DeviceToken.user_id.in_(user_ids)).all()
    by_user: Dict[int, List[str]] = {}
    for t in tokens:
        by_user.setdefault(t.user_id, []).append(t.token)
    return by_user


def _run_once():
    now = datetime.now()
    db = SessionLocal()
    try:
        reminders = (
            db.query(Reminder)
            .options(
                joinedload(Reminder.patient),
                joinedload(Reminder.prescription).joinedload("medication"),
            )
            .filter(Reminder.is_active == True)
            .all()
        )

        due = [r for r in reminders if _should_fire(r, now)]
        if not due:
            return

        user_ids = list({
            (r.patient.caregiver_id if r.patient and r.patient.caregiver_id is not None else r.patient.user_id)
            for r in due if r.patient is not None
        })
        tokens_by_user = _collect_tokens(db, user_ids)

        for r in due:
            caregiver_id = None
            if r.patient:
                caregiver_id = r.patient.caregiver_id if r.patient.caregiver_id is not None else r.patient.user_id

            if caregiver_id is None:
                continue

            tokens = tokens_by_user.get(caregiver_id, [])
            if not tokens:
                continue

            patient_name = r.patient.name if r.patient else "Pasien"
            med_name = None
            if r.prescription and r.prescription.medication:
                med_name = r.prescription.medication.name
            med_name = med_name or "Obat"

            title = "Waktunya Minum Obat!"
            body = f"{patient_name} — {med_name}\nJadwal: {r.scheduled_time.strftime('%H:%M')}"
            data = {
                "reminderId": r.id,
                "patientName": patient_name,
                "medicationName": med_name,
                "time": r.scheduled_time.strftime("%H:%M"),
            }

            invalid = send_push(tokens, title, body, data)
            if invalid:
                db.query(DeviceToken).filter(DeviceToken.token.in_(invalid)).delete(synchronize_session=False)
                db.commit()
    finally:
        db.close()


def start_scheduler():
    global _scheduler
    if _scheduler:
        return

    _scheduler = BackgroundScheduler(daemon=True)
    _scheduler.add_job(_run_once, "interval", seconds=30)
    _scheduler.start()
