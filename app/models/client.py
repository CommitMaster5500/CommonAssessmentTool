from app.database import Base
from sqlalchemy import Column, Integer, Boolean, CheckConstraint
from sqlalchemy.orm import relationship


class Client(Base):
    """
    Client model representing client data in the database.
    """

    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    age = Column(Integer, CheckConstraint("age >= 18"))
    gender = Column(Integer, CheckConstraint("gender = 1 OR gender = 2"))
    work_experience = Column(Integer, CheckConstraint("work_experience >= 0"))
    canada_workex = Column(Integer, CheckConstraint("canada_workex >= 0"))
    dep_num = Column(Integer, CheckConstraint("dep_num >= 0"))
    canada_born = Column(Boolean)
    citizen_status = Column(Boolean)
    level_of_schooling = Column(
        Integer, CheckConstraint("level_of_schooling >= 1 AND level_of_schooling <= 14")
    )
    fluent_english = Column(Boolean)
    reading_english_scale = Column(
        Integer,
        CheckConstraint("reading_english_scale >= 0 AND reading_english_scale <= 10"),
    )
    speaking_english_scale = Column(
        Integer,
        CheckConstraint("speaking_english_scale >= 0 AND speaking_english_scale <= 10"),
    )
    writing_english_scale = Column(
        Integer,
        CheckConstraint("writing_english_scale >= 0 AND writing_english_scale <= 10"),
    )
    numeracy_scale = Column(
        Integer, CheckConstraint("numeracy_scale >= 0 AND numeracy_scale <= 10")
    )
    computer_scale = Column(
        Integer, CheckConstraint("computer_scale >= 0 AND computer_scale <= 10")
    )
    transportation_bool = Column(Boolean)
    caregiver_bool = Column(Boolean)
    housing = Column(Integer, CheckConstraint("housing >= 1 AND housing <= 10"))
    income_source = Column(
        Integer, CheckConstraint("income_source >= 1 AND income_source <= 11")
    )
    felony_bool = Column(Boolean)
    attending_school = Column(Boolean)
    currently_employed = Column(Boolean)
    substance_use = Column(Boolean)
    time_unemployed = Column(Integer, CheckConstraint("time_unemployed >= 0"))
    need_mental_health_support_bool = Column(Boolean)
    cases = relationship("ClientCase", back_populates="client", passive_deletes=True)
