from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Task:
    id: Optional[int] = None
    title: str = ""
    description: Optional[str] = None
    assigned_to: Optional[str] = None
    status: str = "pending"
    due_date: Optional[datetime] = None

@dataclass
class Notification:
    id: Optional[int] = None
    message: str = ""
    user: str = ""
    sent_at: datetime = datetime.now()