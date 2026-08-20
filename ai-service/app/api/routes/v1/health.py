from fastapi import APIRouter, Depends

from app.api.dependencies.health import get_health_use_case
from app.application.use_cases.health_check import HealthCheckUseCase

router = APIRouter()


@router.get("")
async def health_check(
    use_case: HealthCheckUseCase = Depends(get_health_use_case),
) -> dict[str, str]:

    return use_case.execute()