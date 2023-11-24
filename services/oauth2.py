from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from security import token
from schemas.user import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(data: str = Depends(oauth2_scheme)):
    credentails_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"},
                                          )
    return token.verify_token(data, credentails_exception)


def get_current_admin(tokendata: TokenData = Depends(get_current_user)):
    print(tokendata)
    if tokendata.role == 2:
        raise HTTPException(status_code=403, detail="Admin access required")
    return tokendata
