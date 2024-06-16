
from datetime import datetime
from typing import Annotated, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


from fastapi import Depends, HTTPException

from src.config.database import get_session
from src.models.user import ActivationCode, User
from src.schemas.user import ResetPassword, ResetPasswordAccount
from src.security.hasher import Hasher
from src.security.jwt_manager import JwtManager



class AuthService:

    def __init__(
        self,
        session: Annotated[
            AsyncSession, Depends(get_session)
        ],
    ) -> None:
        self._sess = session
    async def find_user_by_email(self, email: str) -> Optional[User]:
           
        q = select(User).where(User.email == email)

        return (await self._sess.exec(q)).one_or_none()

        

    async def insert_user(self, body: User):
        self._sess.add(body)
        await self._sess.commit()
        await self._sess.refresh(body)
        return body

    async def insert_code(self, body: ActivationCode):
        self._sess.add(body)
        await self._sess.commit()
        await self._sess.refresh(body)

 
    async def get_all(self):
        q = select(User)
        users = (await self._sess.exec(q)).all()
        return users
    
    async def get_one(self, id:int):
        q = select(User).where(User.id == id)
        user = (await self._sess.exec(q)).one_or_none()
        return user

    async def activate_user(self, id:int):
        user = await self.get_one(id)
        if not user:
            return
        user.status = 1
        self._sess.add(user)
        await self._sess.commit()
        return user
    
    async def verify_activation_code_expiry(self, activation_code: ActivationCode):
        now = datetime.now()
        expiry_code: datetime = activation_code.expires_at
        if now > expiry_code:
            return False  # The activation code is expired
        else:
            return True  # The activation code is still valid

    async def reset_password(self, body: ResetPassword):
        user: Optional[User] = await self.find_user_by_email(body.email)
        if not user:
            return 
        user.hashed_password = Hasher.hash_text(password=body.password)
        self._sess.add(user)
        await self._sess.commit()
        return user
    
    async def reset_password_account(self, body: ResetPasswordAccount, user_id: int) -> bool:
        user: Optional[User] = await self.get_one(user_id)
        if not user:
            print("failed user check")
            return False
        if not Hasher.verify_hash(body.current_pass, user.hashed_password):
            print("Failed pass check")
            return False
        user.hashed_password = Hasher.hash_text(password=body.new_password)
        self._sess.add(user)
        await self._sess.commit()
        return True
    
    async def get_current_user_id(
        self,
        token: str 
    ) :
        # No need to check if token is present, AccessTokenBearer handles it

        payload = JwtManager.decode_access(token)
        user_id: int = int(payload.get("sub")) # type: ignore
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        """ user: Optional[User] = await AuthService.get_one(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found") """
        
        print(f"\n\n user id is : {user_id}\n\n")
        
        return user_id
    
    async def ban_user(self,user_id):
        user: Optional[User] = await self.get_one(user_id)
        if not user:
            return 
        user.ban_status = "banned"
        self._sess.add(user)
        await self._sess.commit()
        return user
    

    async def users_per_month(self):
        users_per_month = [0] * 12
        query = select(User)  # Replace UserModel with your actual user model
        
        users = (await self._sess.exec(query)).all()
        for user in users:
            if user.created_at:
                month = user.created_at.month
                print("User created in month:", month)
                users_per_month[month - 1] += 1  # month - 1 to use 0-based index
        
        return users_per_month