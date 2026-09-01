from app.application.services.health_service import HealthService
from app.application.use_cases.health_check import HealthCheckUseCase


def get_health_use_case() -> HealthCheckUseCase:
    health_service = HealthService()

    return HealthCheckUseCase(health_service)