from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from app.core.config import settings

def check_researcher_role(token: str = Depends(...)):
    try:
        # Decode JWT
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])

        # Extract role from payload
        role = payload.get("role")
        if role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing role claim",
            )

        # Convert to int if it's a string digit
        try:
            role = int(role)
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid role format in token",
            )

        # 0 = patient, 1 = researcher
        if role != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only researchers can perform this action",
            )

        # Return payload if valid researcher
        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
