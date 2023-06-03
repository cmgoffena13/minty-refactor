import redis
import rq
from flask import current_app
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import *

from minty.extensions import db


class Task(db.Model):
    __tablename__ = "tasks"

    task_id = db.Column(VARCHAR(36), primary_key=True)
    name = db.Column(VARCHAR(128), index=True)
    description = db.Column(VARCHAR(128))
    created_on = db.Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )

    def get_rq_job(self):
        try:
            rq_job = rq.job.Job.fetch(self.task_id, connection=current_app.redis)
        except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
            return None
        return rq_job

    def get_progress(self):
        job = self.get_rq_job()
        return job.meta.get("progress", 0) if job is not None else 100
