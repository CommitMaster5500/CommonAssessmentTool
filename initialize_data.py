import os
import logging
import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.client import Client
from app.models.user import User, UserRole
from app.models.client_case import ClientCase
from app.auth.service import get_password_hash
from app.config.settings import (
    DATA_CSV_PATH,
    ADMIN_USERNAME,
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
    WORKER_USERNAME,
    WORKER_EMAIL,
    WORKER_PASSWORD,
)


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def initialize_database():
    logger.info("Starting database initialization...")
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == ADMIN_USERNAME).first()
        if not admin:
            admin_user = User(
                username=ADMIN_USERNAME,
                email=ADMIN_EMAIL,
                hashed_password=get_password_hash(ADMIN_PASSWORD),
                role=UserRole.admin,
            )
            db.add(admin_user)
            db.commit()
            logger.info("Admin user created.")
        else:
            admin_user = admin
            logger.info("Admin user already exists.")

        case_worker = db.query(User).filter(User.username == WORKER_USERNAME).first()
        if not case_worker:
            case_worker = User(
                username=WORKER_USERNAME,
                email=WORKER_EMAIL,
                hashed_password=get_password_hash(WORKER_PASSWORD),
                role=UserRole.case_worker,
            )
            db.add(case_worker)
            db.commit()
            logger.info("Case worker created.")
        else:
            logger.info("Case worker already exists.")

        if not os.path.exists(DATA_CSV_PATH):
            logger.error(f"CSV file not found: {DATA_CSV_PATH}")
            return

        logger.info(f"Loading CSV data from {DATA_CSV_PATH}...")
        df = pd.read_csv(DATA_CSV_PATH)

        integer_columns = [
            "age",
            "gender",
            "work_experience",
            "canada_workex",
            "dep_num",
            "level_of_schooling",
            "reading_english_scale",
            "speaking_english_scale",
            "writing_english_scale",
            "numeracy_scale",
            "computer_scale",
            "housing",
            "income_source",
            "time_unemployed",
            "success_rate",
        ]
        df[integer_columns] = df[integer_columns].apply(pd.to_numeric, errors="coerce")

        for _, row in df.iterrows():
            client = Client(
                age=int(row["age"]),
                gender=int(row["gender"]),
                work_experience=int(row["work_experience"]),
                canada_workex=int(row["canada_workex"]),
                dep_num=int(row["dep_num"]),
                canada_born=bool(row["canada_born"]),
                citizen_status=bool(row["citizen_status"]),
                level_of_schooling=int(row["level_of_schooling"]),
                fluent_english=bool(row["fluent_english"]),
                reading_english_scale=int(row["reading_english_scale"]),
                speaking_english_scale=int(row["speaking_english_scale"]),
                writing_english_scale=int(row["writing_english_scale"]),
                numeracy_scale=int(row["numeracy_scale"]),
                computer_scale=int(row["computer_scale"]),
                transportation_bool=bool(row["transportation_bool"]),
                caregiver_bool=bool(row["caregiver_bool"]),
                housing=int(row["housing"]),
                income_source=int(row["income_source"]),
                felony_bool=bool(row["felony_bool"]),
                attending_school=bool(row["attending_school"]),
                currently_employed=bool(row["currently_employed"]),
                substance_use=bool(row["substance_use"]),
                time_unemployed=int(row["time_unemployed"]),
                need_mental_health_support_bool=bool(
                    row["need_mental_health_support_bool"]
                ),
            )
            db.add(client)
            db.flush()

            client_case = ClientCase(
                client_id=client.id,
                user_id=admin_user.id,
                employment_assistance=bool(row["employment_assistance"]),
                life_stabilization=bool(row["life_stabilization"]),
                retention_services=bool(row["retention_services"]),
                specialized_services=bool(row["specialized_services"]),
                employment_related_financial_supports=bool(
                    row["employment_related_financial_supports"]
                ),
                employer_financial_supports=bool(row["employer_financial_supports"]),
                enhanced_referrals=bool(row["enhanced_referrals"]),
                success_rate=int(row["success_rate"]),
            )
            db.add(client_case)

        db.commit()
        logger.info("Database initialization completed.")

    except Exception as e:
        logger.error(f"Error during initialization: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    initialize_database()
