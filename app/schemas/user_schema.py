from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=4, max_length=100)


class UserResponse(BaseModel):
    user_id: int
    username: str

    class Config:
        from_attributes = True
