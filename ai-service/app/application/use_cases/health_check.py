from app.application.services.health_service import HealthService

class HealthCheckUseCase:
    def __init__(self, health_service: HealthService) -> None:
        self.health_service = health_service

    def execute(self) -> dict[str, str]:
        return self.health_service.get_status()