from fastapi import APIRouter, Depends, status, HTTPException
import models
from security import token
from config import database
from security.hashing import Hash
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Tài khoản không đúng')
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Mật khẩu không đúng')
    access_token = token.create_access_token(data={"sub": user.username, "role": user.id_role})
    return {"access_token": access_token, "token_type": "bearer"}