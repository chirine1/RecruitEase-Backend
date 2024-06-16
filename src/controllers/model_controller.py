import os
from typing import Annotated, List, Optional
import joblib
from fastapi import Depends
import pandas as pd

from src.schemas.model import JobCandidate, JobCandidateOut
from src.services.candidate import CandidateService
from src.services.company import CompanyService
from src.services.job import JobService
from src.services.user import AuthService



class ModelController:
    def __init__(
        self,
        candidate_service: Annotated[CandidateService, Depends()],
        job_service: Annotated[JobService, Depends()],
        auth_service: Annotated[AuthService, Depends()],
        
    ) -> None:
        self.candidate_service = candidate_service
        self.job_service = job_service
        self.auth_service = auth_service

   

    async def predict(self, candidate_id: int, job_id: int):
        current_dir = os.path.dirname(__file__)
        model_path = os.path.join(current_dir, '../AI/rf_model.pkl')
        model = joblib.load(model_path)

        candidate_job = await self.prepare_data(candidate_id=candidate_id, job_id=job_id)
        if not candidate_job:
            return
        
        data = pd.DataFrame([candidate_job.model_dump()])

         # Preprocess and predict
        prediction = model.predict(data)

        # Convert numpy types to native Python types
        prediction = prediction.astype(str).tolist()

        return  self.create_job_candidate_out(candidate_job, prediction)

       
    


    async def prepare_data(self, candidate_id: int, job_id: int) -> Optional[JobCandidate]:
        job = await self.job_service.get_one(job_id)
        if not job:
            return None
        candidate = await self.candidate_service.get_one(candidate_id)
        if not candidate:
            return None

        job_company_contact = getattr(job.company, "contact_info", None)
        job_country =  getattr(job_company_contact, "country",None)
        job_country_label = "USA" if not job_country else getattr(job_country,"label","USA")

        
        candidate_contact = getattr(candidate, "contact_info", None)
        candidate_country =  getattr(candidate_contact, "country", None)
        candidate_country_label ="Tunisia" if not candidate_country else getattr(candidate_country, "label", "USA")
        candidate_job = JobCandidate(
            Age=25,
            CurrentSalary=5000,
            ExpectedSalary=6000,
            OfferedSalaryMin=job.offered_salary_min,
            OfferedSalaryMax=job.offered_salary_max,
            EducationLevel="bachelor's degree",
            CareerLevel="senior",
            CandidateCountry=candidate_country_label,
            JobType=job.job_type,
            JobCareerLevel=job.career_level,
            Industry=job.industry.label,
            JobCountry=job_country_label,
            CandidateSkills="Python, SQL, Machine Learning",
            JobSkills="Python, SQL, Data Analysis"
        )

        candidate_attrs = {
            "age": "Age",
            "current_salary": "CurrentSalary",
            "expected_salary": "ExpectedSalary",
            "education_level": "EducationLevel",
            "career_level": "CareerLevel",
        }

        for attr, result_attr in candidate_attrs.items():
            if hasattr(candidate, attr) and getattr(candidate, attr) is not None:
                new_value = getattr(candidate, attr)
                setattr(candidate_job, result_attr, new_value)

        # Transform skills into a string
        job_skills_stringified = ", ".join([skill.label for skill in job.skills])

        candidate_skills_stringified = ""
        candidate_skills = getattr(candidate.resume, "skills", None)
        if candidate_skills:
            candidate_skills_stringified = ", ".join([skill.label for skill in candidate_skills])

        candidate_job.JobSkills = job_skills_stringified
        candidate_job.CandidateSkills = candidate_skills_stringified

        return candidate_job


    def create_job_candidate_out(self, candidate: JobCandidate, prediction_label: List) -> JobCandidateOut:   
        return JobCandidateOut(
            Age=candidate.Age,
            CurrentSalary=candidate.CurrentSalary,
            ExpectedSalary=candidate.ExpectedSalary,
            OfferedSalaryMin=candidate.OfferedSalaryMin,
            OfferedSalaryMax=candidate.OfferedSalaryMax,
            EducationLevel=candidate.EducationLevel,
            CareerLevel=candidate.CareerLevel,
            CandidateCountry=candidate.CandidateCountry,
            JobType=candidate.JobType,
            JobCareerLevel=candidate.JobCareerLevel,
            Industry=candidate.Industry,
            JobCountry=candidate.JobCountry,
            CandidateSkills=candidate.CandidateSkills,
            JobSkills=candidate.JobSkills,
            label=prediction_label
        )