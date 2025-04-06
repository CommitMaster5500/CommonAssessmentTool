from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, status
from app.models.client import Client
from app.models.client_case import ClientCase


class ClientQueryService:
    def __init__(self, db: Session):
        self.db = db

    def get_clients_by_criteria(self, **filters):
        query = self.db.query(Client)

        # Explicitly handle "age_min"
        if "age_min" in filters and filters["age_min"] is not None:
            age_min = filters["age_min"]
            if age_min < 18:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Minimum age must be at least 18",
                )
            query = query.filter(Client.age >= age_min)
            del filters["age_min"]

        # handle other filters
        for field, value in filters.items():
            if value is not None:
                query = query.filter(getattr(Client, field) == value)

        return query.all()

    def get_clients_by_services(self, **service_filters):
        """Fetch clients based on service status filters"""
        query = self.db.query(Client).join(ClientCase)

        for service_name, status in service_filters.items():
            if status is not None:
                query = query.filter(getattr(ClientCase, service_name) == status)

        try:
            return query.all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving clients by service: {str(e)}",
            )

    def get_clients_by_success_rate(self, min_rate: int = 70):
        """Fetch clients with a success rate >= min_rate"""
        if not (0 <= min_rate <= 100):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Success rate must be between 0 and 100",
            )

        return (
            self.db.query(Client)
            .join(ClientCase)
            .filter(ClientCase.success_rate >= min_rate)
            .all()
        )
