from pydantic import BaseModel


class PredictionInput(BaseModel):
    """
    Schema for ML prediction input data
    """

    age: int
    gender: str
    work_experience: int
    canada_workex: int
    dep_num: int
    canada_born: str
    citizen_status: str
    level_of_schooling: str
    fluent_english: str
    reading_english_scale: int
    speaking_english_scale: int
    writing_english_scale: int
    numeracy_scale: int
    computer_scale: int
    transportation_bool: str
    caregiver_bool: str
    housing: str
    income_source: str
    felony_bool: str
    attending_school: str
    currently_employed: str
    substance_use: str
    time_unemployed: int
    need_mental_health_support_bool: str
    employment_assistance: int
    life_stabilization: int
    retention_services: int
    specialized_services: int
    employment_related_financial_supports: int
    employer_financial_supports: int
    enhanced_referrals: int


class PredictionResponse(BaseModel):
    """Response model for prediction results"""

    success_rate: float
    model_used: str
