from pydantic import BaseModel

class CurrentUser(BaseModel):
    user_id: int
    username: str
    email: str
    role: str