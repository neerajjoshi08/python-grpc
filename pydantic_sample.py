from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    uid: int
    name: Optional[str] = "Alice"
    friends: list[str] = []


user = User(uid=123)
print(user)
