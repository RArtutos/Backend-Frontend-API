from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ...core.auth import get_current_admin_user
from ...db.database import Database
from ...schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter()
db = Database()

@router.get("/", response_model=List[UserResponse])
async def get_users(current_user: dict = Depends(get_current_admin_user)):
    users = db.get_users()
    return users

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, current_user: dict = Depends(get_current_admin_user)):
    if db.get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return db.create_user(user.dict())

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user: UserUpdate,
    current_user: dict = Depends(get_current_admin_user)
):
    """Update user details"""
    existing_user = db.get_user_by_email(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if existing_user.get("is_admin") and not user.is_admin:
        raise HTTPException(status_code=400, detail="Cannot remove admin status")
    
    updated_user = db.update_user(user_id, user.dict(exclude_unset=True))
    if not updated_user:
        raise HTTPException(status_code=400, detail="Failed to update user")
    return updated_user

@router.delete("/{user_id}")
async def delete_user(user_id: str, current_user: dict = Depends(get_current_admin_user)):
    """Delete a user"""
    if user_id == current_user["email"]:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    if db.get_user_by_email(user_id).get("is_admin"):
        raise HTTPException(status_code=400, detail="Cannot delete admin users")
        
    if db.delete_user(user_id):
        return {"success": True, "message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")

@router.get("/{user_id}/accounts")
async def get_user_accounts(user_id: str, current_user: dict = Depends(get_current_admin_user)):
    """Get accounts assigned to a user"""
    user = db.get_user_by_email(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return db.get_accounts(user_id)