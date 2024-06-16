from sqlalchemy import Column, ForeignKey, Table

from src.config.database import Base


""" company_industry = Table(
    "company_industry",
    Base.metadata,
    Column("company", ForeignKey("company.id"), primary_key=True),
    Column("industry", ForeignKey("industry.id"), primary_key=True),
) """

job_skill = Table(
    "job_skill",
    Base.metadata,
    Column("job", ForeignKey("job.id"), primary_key=True),
    Column("skill", ForeignKey("skill.id"), primary_key=True),
)

resume_skill = Table(
    "resume_skill",
    Base.metadata,
    Column("resume", ForeignKey("resume.id"), primary_key=True),
    Column("skill", ForeignKey("skill.id"), primary_key=True),
)

resume_language = Table(
    "resume_language",
    Base.metadata,
    Column("resume", ForeignKey("resume.id"), primary_key=True),
    Column("language", ForeignKey("language.id"), primary_key=True),
)

""" job_industry = Table(
    "job_industry",
    Base.metadata,
    Column("job", ForeignKey("job.id"), primary_key=True),
    Column("industry", ForeignKey("industry.id"), primary_key=True),
) """

