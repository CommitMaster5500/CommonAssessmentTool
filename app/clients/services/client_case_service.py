from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.client import Client
from app.models.user import User
from app.models.client_case import ClientCase
from app.clients.schemas.client_case import ServiceUpdate


class ClientCaseService:
    def __init__(self, db: Session):
        self.db = db

    def get_client_services(self, client_id: int):
        """Get all services for a specific client with case worker info"""
        client_cases = (
            self.db.query(ClientCase).filter(ClientCase.client_id == client_id).all()
        )
        if not client_cases:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No services found for client with id {client_id}",
            )
        return client_cases

    def update_client_services(
        self, client_id: int, user_id: int, service_update: ServiceUpdate
    ):
        """Update a client's service records"""
        client_case = (
            self.db.query(ClientCase)
            .filter(ClientCase.client_id == client_id, ClientCase.user_id == user_id)
            .first()
        )

        if not client_case:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No case found for client {client_id} with case worker {user_id}",
            )

        update_data = service_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(client_case, field, value)

        try:
            self.db.commit()
            self.db.refresh(client_case)
            return client_case
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update client services: {str(e)}",
            )

    def create_case_assignment(self, client_id: int, case_worker_id: int):
        """Assign a case worker to a client"""
        client = self.db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id {client_id} not found",
            )

        case_worker = self.db.query(User).filter(User.id == case_worker_id).first()
        if not case_worker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Case worker with id {case_worker_id} not found",
            )

        existing_case = (
            self.db.query(ClientCase)
            .filter(
                ClientCase.client_id == client_id, ClientCase.user_id == case_worker_id
            )
            .first()
        )

        if existing_case:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Client {client_id} already assigned to case worker {case_worker_id}",
            )

        new_case = ClientCase(
            client_id=client_id,
            user_id=case_worker_id,
            employment_assistance=False,
            life_stabilization=False,
            retention_services=False,
            specialized_services=False,
            employment_related_financial_supports=False,
            employer_financial_supports=False,
            enhanced_referrals=False,
            success_rate=0,
        )

        try:
            self.db.add(new_case)
            self.db.commit()
            self.db.refresh(new_case)
            return new_case
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create case assignment: {str(e)}",
            )

    def get_clients_by_case_worker(self, case_worker_id: int):
        """Fetch all clients assigned to a specific case worker."""
        case_worker = self.db.query(User).filter(User.id == case_worker_id).first()
        if not case_worker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Case worker with id {case_worker_id} not found",
            )

        clients = (
            self.db.query(Client)
            .join(ClientCase)
            .filter(ClientCase.user_id == case_worker_id)
            .all()
        )

        return clients
