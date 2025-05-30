"""
Router module for client-related endpoints.
Handles all HTTP requests for client operations including create, read, update, and delete.
"""

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.auth.router import get_current_user, get_admin_user
from app.database import get_db
from app.models.user import User
from app.clients.services import ClientRepository, ClientQueryService, ClientCaseService, ClientService
from app.clients.schemas import (
    ClientResponse,
    ClientUpdate,
    ClientListResponse,
    ServiceResponse,
    ServiceUpdate,
    PredictionInput,
    PredictionResponse
)

router = APIRouter(prefix="/clients", tags=["clients"])

# ------------------ CD Test Endpoint ------------------

@router.get("/cd-test", tags=["CD Test"])
async def cd_pipeline_test():
    """
    A simple endpoint to verify that the CD pipeline works.
    Returns a fixed message.
    """
    return {"message": "CD pipeline is working!"}


# ------------------ Clients ------------------


@router.get("/", response_model=ClientListResponse)
async def get_clients(
    current_user: User = Depends(get_admin_user),
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        default=50, ge=1, le=150, description="Maximum number of records to return"
    ),
    db: Session = Depends(get_db),
):
    return ClientRepository(db).get_clients(skip, limit)


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """Get a specific client by ID"""
    return ClientRepository(db).get_client(client_id)


@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: int,
    client_data: ClientUpdate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """Update a client's information"""
    return ClientRepository(db).update_client(client_id, client_data)


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    client_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """Delete a client"""
    ClientRepository(db).delete_client(client_id)
    return None


# ------------------ Query Clients ------------------


@router.get("/search/by-criteria", response_model=List[ClientResponse])
async def get_clients_by_criteria(
    employment_status: Optional[bool] = None,
    education_level: Optional[int] = Query(None, ge=1, le=14),
    age_min: Optional[int] = Query(None, ge=18),
    gender: Optional[int] = Query(None, ge=1, le=2),
    work_experience: Optional[int] = Query(None, ge=0),
    canada_workex: Optional[int] = Query(None, ge=0),
    dep_num: Optional[int] = Query(None, ge=0),
    canada_born: Optional[bool] = None,
    citizen_status: Optional[bool] = None,
    fluent_english: Optional[bool] = None,
    reading_english_scale: Optional[int] = Query(None, ge=0, le=10),
    speaking_english_scale: Optional[int] = Query(None, ge=0, le=10),
    writing_english_scale: Optional[int] = Query(None, ge=0, le=10),
    numeracy_scale: Optional[int] = Query(None, ge=0, le=10),
    computer_scale: Optional[int] = Query(None, ge=0, le=10),
    transportation_bool: Optional[bool] = None,
    caregiver_bool: Optional[bool] = None,
    housing: Optional[int] = Query(None, ge=1, le=10),
    income_source: Optional[int] = Query(None, ge=1, le=11),
    felony_bool: Optional[bool] = None,
    attending_school: Optional[bool] = None,
    substance_use: Optional[bool] = None,
    time_unemployed: Optional[int] = Query(None, ge=0),
    need_mental_health_support_bool: Optional[bool] = None,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """Search clients by any combination of criteria"""
    return ClientQueryService(db).get_clients_by_criteria(
        employment_status=employment_status,
        education_level=education_level,
        age_min=age_min,
        gender=gender,
        work_experience=work_experience,
        canada_workex=canada_workex,
        dep_num=dep_num,
        canada_born=canada_born,
        citizen_status=citizen_status,
        fluent_english=fluent_english,
        reading_english_scale=reading_english_scale,
        speaking_english_scale=speaking_english_scale,
        writing_english_scale=writing_english_scale,
        numeracy_scale=numeracy_scale,
        computer_scale=computer_scale,
        transportation_bool=transportation_bool,
        caregiver_bool=caregiver_bool,
        housing=housing,
        income_source=income_source,
        felony_bool=felony_bool,
        attending_school=attending_school,
        substance_use=substance_use,
        time_unemployed=time_unemployed,
        need_mental_health_support_bool=need_mental_health_support_bool,
    )


@router.get("/search/success-rate", response_model=List[ClientResponse])
async def get_clients_by_success_rate(
    min_rate: int = Query(
        70, ge=0, le=100, description="Minimum success rate percentage"
    ),
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """Get clients with success rate above specified threshold"""
    return ClientQueryService(db).get_clients_by_success_rate(min_rate)


@router.get("/search/by-services", response_model=List[ClientResponse])
async def get_clients_by_services(
    employment_assistance: Optional[bool] = None,
    life_stabilization: Optional[bool] = None,
    retention_services: Optional[bool] = None,
    specialized_services: Optional[bool] = None,
    employment_related_financial_supports: Optional[bool] = None,
    employer_financial_supports: Optional[bool] = None,
    enhanced_referrals: Optional[bool] = None,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """Get clients filtered by multiple service statuses"""
    return ClientQueryService(db).get_clients_by_services(
        employment_assistance=employment_assistance,
        life_stabilization=life_stabilization,
        retention_services=retention_services,
        specialized_services=specialized_services,
        employment_related_financial_supports=employment_related_financial_supports,
        employer_financial_supports=employer_financial_supports,
        enhanced_referrals=enhanced_referrals,
    )


# ------------------ Client Case  -----------------------


@router.get("/case-worker/{case_worker_id}", response_model=List[ClientResponse])
async def get_clients_by_case_worker(
    case_worker_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ClientCaseService(db).get_clients_by_case_worker(case_worker_id)


@router.get("/{client_id}/services", response_model=List[ServiceResponse])
async def get_client_services(
    client_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """Get all services and their status for a specific client, including case worker info"""
    return ClientCaseService(db).get_client_services(client_id)


@router.put("/{client_id}/services/{user_id}", response_model=ServiceResponse)
async def update_client_services(
    client_id: int,
    user_id: int,
    service_update: ServiceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ClientCaseService(db).update_client_services(
        client_id, user_id, service_update
    )


@router.post("/{client_id}/case-assignment", response_model=ServiceResponse)
async def create_case_assignment(
    client_id: int,
    case_worker_id: int = Query(..., description="Case worker ID to assign"),
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """Create a new case assignment for a client with a case worker"""
    return ClientCaseService(db).create_case_assignment(client_id, case_worker_id)

# ------------------ Prediction ------------------

@router.post("/{client_id}/predict", response_model=PredictionResponse)
async def predict_client_success(
    client_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    prediction = ClientService.predict_success(db, client_id)
    return prediction
