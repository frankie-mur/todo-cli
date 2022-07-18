from dataclasses import dataclass
import datetime


@dataclass
class Todo:
    task: str
    category: str
    status: str
    position: int
    date_added: str = datetime.datetime.now().isoformat()
    data_completed: str = None
    status: str = 1
    position: int = None

    def __repr__(self) -> str:
        return f'{self.task}, {self.category}, {self.status}, {self.position}, {self.date_added}, {self.data_completed}, {self.status}, {self.position}'
