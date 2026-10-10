from app.models.domain import (
    User,
    UserRole,
    Complaint,
    PriorityLevel,
    University,
    Campus,
    Department,
)
from app.models.academic import AcademicCourse, ClassSchedule
from app.models.emergency import EmergencyAlert
from app.models.notification import Notification

__all__ = [
    "User",
    "UserRole",
    "Complaint",
    "PriorityLevel",
    "University",
    "Campus",
    "Department",
]