from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_users(
    # users: UserRepository = Depends(get_user_repository),
    limit: int = 100, 
    skip: int = 0):
    return {'limit': limit, 'skip': 0}