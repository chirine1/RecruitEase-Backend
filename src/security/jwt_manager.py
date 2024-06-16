from datetime import datetime, timedelta, timezone

from jose import jwt


from ..config import Settings






class JwtManager:
    
    @staticmethod
    def create_access_token(sub: str):
        return JwtManager.__gen_token(
            Settings().ACCESS_TOKEN_EXPIRE_MINUTES,
            sub,
            Settings().JWT_SECRET,
        )
    
    @staticmethod
    def create_refresh_token(sub: str):
        return JwtManager.__gen_token(
            Settings().REFRESH_TOKEN_EXPIRE_MINUTES,
            sub,
            Settings().REFRESH_SECRET,
        )

    @staticmethod
    def decode_access(token: str):
        return jwt.decode(token, key=Settings().JWT_SECRET)

    @staticmethod
    def decode_refresh(refresh: str):
        return jwt.decode(
            refresh, key=Settings().REFRESH_SECRET
        )

    """     @staticmethod
    def check_token_validity(exp: int):
        return datetime.now(
            timezone.utc
        ) < datetime.fromtimestamp(exp) """
    @staticmethod
    def check_token_validity(exp: int):
        current_time = datetime.now(timezone.utc)
        expiration_time = datetime.fromtimestamp(exp, timezone.utc)
        return current_time < expiration_time

    @staticmethod
    def __gen_token(exp: int, sub: str, sec: str):
        to_encode = {
            "sub": sub,
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=exp),
        }

        return jwt.encode(to_encode, sec)
    





    
