from pydantic import BaseModel

# 🔐 Registration schema
class UserCreate(BaseModel):
    username: str
    password: str

# ✅ Add this for /auth/register response
class User(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True  # Required in Pydantic v2+

# 🔑 Token response schema for /auth/login
class Token(BaseModel):
    access_token: str
    token_type: str

# 🔗 URL Shorten request
class URLCreate(BaseModel):
    url: str

# 🔗 URL Shorten response
class URLInfo(BaseModel):
    original_url: str
    short_url: str
    qr_code: str

    class Config:
        from_attributes = True
