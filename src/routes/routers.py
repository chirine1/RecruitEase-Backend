from fastapi import APIRouter


auth_router = APIRouter(prefix="/auth", tags=["auth"])
candidate_router = APIRouter(prefix="/candidate", tags=["candidate"])
company_router = APIRouter(prefix="/company", tags=["company"])
job_router = APIRouter(prefix="/job", tags=["job"])
industry_router = APIRouter(prefix="/industry", tags=["industry"])
skill_router = APIRouter(prefix="/skill", tags=["skill"])
application_router = APIRouter(prefix="/application", tags=["application"])
language_router = APIRouter(prefix="/language", tags=["language"])
enum_router = APIRouter(prefix="/enums", tags=["enums"])
country_router = APIRouter(prefix="/country", tags=["country"])
state_router = APIRouter(prefix="/state", tags=["state"])
resume_router = APIRouter(prefix="/resume", tags=["resume"])
payment_router = APIRouter(prefix="/payment", tags=["payment"])
blog_router = APIRouter(prefix="/blog_post", tags=["blog"])
test_router = APIRouter(prefix="/test", tags=["test"])
message_router = APIRouter(prefix="/message", tags=["message"])
model_router = APIRouter(prefix="/model", tags=["model"])
init_db = APIRouter(prefix="/init_db", tags=["init_db"])
comment_router = APIRouter(prefix="/comment", tags=["comment"])
notification_router = APIRouter(prefix="/notif", tags=["notification"])
stats_router = APIRouter(prefix="/stats", tags=["stats"])