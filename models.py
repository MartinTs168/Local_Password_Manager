import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from encryption import encrypt

engine = sqlalchemy.create_engine("sqlite:///manager.db")
Session = sessionmaker(bind=engine)

Base = automap_base()
Base.prepare(engine, reflect=True)


User = Base.classes.users
Password = Base.classes.passwords


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
