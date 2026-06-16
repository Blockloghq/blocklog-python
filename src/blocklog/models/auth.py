from pydantic import BaseModel

from blocklog.models.teams import Team


class User(BaseModel):
    user_id: str
    username: str
    email: str
    company_id: str
    is_active: bool
    is_admin: bool = False


class SignupResponse(BaseModel):
    user: User
    token: str
    expires_in: int
    team: Team


class LoginResponse(BaseModel):
    user: User
    token: str
    expires_in: int
    team: Team | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: str
    company_id: str
    team_id: str | None = None
