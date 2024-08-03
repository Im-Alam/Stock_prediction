from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    def deselect(self, *args: str):
        outKey = set(self.__dict__.keys()) - set(args) - {'_sa_instance_state'}
        user = {}
        for key in outKey:
            user[key] = getattr(self, key)

        return user
