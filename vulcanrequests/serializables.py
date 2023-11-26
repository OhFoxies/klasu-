from dataclasses import dataclass
from typing import Optional, List

from vulcan.data import Exam, Homework


@dataclass
class Exams:
    new_exams: List[Optional[Exam]]
    upcoming_exams: List[Optional[Exam]]
    all_exams: List[Optional[Exam]]


@dataclass
class Homeworks:
    new_homeworks: List[Optional[Homework]]
    all_homeworks: List[Optional[Homework]]
