from typing import Optional, List
from dataclasses import dataclass
from vulcan.data import Exam


@dataclass
class Exams:
    new_exams: List[Optional[Exam]]
    upcoming_exams: List[Optional[Exam]]
    all_exams: List[Optional[Exam]]
