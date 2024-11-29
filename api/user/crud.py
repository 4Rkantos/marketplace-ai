from sqlalchemy.orm import Session
from ...models import user as userSchema

def get_user(db: Session, user_id: int):
    return db.query(userSchema.UserResponse).filter(userSchema.UserResponse.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(userSchema.UserResponse).offset(skip).limit(limit).all()

def create_user(db: Session, user: userSchema.UserCreate):
    db_user = userSchema.UserResponse(name=user.email, description=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user