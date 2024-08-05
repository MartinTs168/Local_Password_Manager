from typing import List
from sqlalchemy import ForeignKey, Integer, String, create_engine, Column
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from encryption import encrypt

engine = create_engine("sqlite:///manager.db")
Session = sessionmaker(bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    passwords = relationship("Password", back_populates="user")


class Password(Base):
    __tablename__ = "passwords"
    id = Column(Integer, primary_key=True, autoincrement=True)
    service = Column(String, nullable=False)
    username = Column(String, nullable=True)
    email = Column(String, nullable=True)
    password = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="passwords")


def add_password(app_user: str, service, username, email, password):
    encrypted_password = encrypt(password)
    with Session() as session:
        user = session.query(User).filter_by(username=app_user).first()
        new_password = Password(
            service=service,
            username=username,
            email=email,
            password=encrypted_password,
            user_id=user.id,
        )

        session.add(new_password)
        print(session.commit())


def create_tables():
    Base.metadata.create_all(engine)


def edit_password(password_id: int, service, username, email, new_password):
    encrypted_password = encrypt(new_password)
    with Session() as session:
        password = session.query(Password).get(password_id)
        password.service = service
        password.username = username
        password.email = email
        password.password = encrypted_password

        session.commit()


def get_password(password_id: int) -> Password:
    with Session() as session:
        password = session.query(Password).get(password_id)
        return password


def get_user_through_password(password_id: int):
    with Session() as session:
        password = session.query(Password).get(password_id)
        user = session.query(User).get(password.user_id)
        return user


def delete_password(password_id: int):
    with Session() as session:
        password = session.query(Password).get(password_id)
        session.delete(password)
        session.commit()


def get_users_passwords(username: str):
    with Session() as session:
        passwords = (
            session.query(Password).join(User).where(User.username == username).all()
        )
        print(passwords)
        return passwords


def get_user_login_password(username: str):
    with Session() as session:
        user = session.query(User).filter_by(username=username).first()
        return user.password


def get_users() -> List[tuple]:
    with Session() as session:
        users = session.query(User.username).all()
        return users


def add_user(username: str, password: str):
    with Session() as session:
        new_user = User(username=username, password=password)
        session.add(new_user)
        session.commit()
