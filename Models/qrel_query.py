from typing import List
from pydantic import BaseModel


class QrelQuery (BaseModel) :
    qid: int
    query: str
    score: int
    views: int
    answer_pids: List[int]

