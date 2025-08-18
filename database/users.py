from sqlalchemy import func

from database.models import User, sql_cursor


def get_or_create_user(telegram_user) -> User:
    with sql_cursor() as session:
        db_user = session.query(User).filter(User.telegram_id == telegram_user.id).first()

        if db_user:
            db_user.username = telegram_user.username
            db_user.first_name = telegram_user.first_name
            db_user.last_activity = func.now()

            print(f"Existing user logged in: {db_user.username} ({db_user.telegram_id})")

        else:
            db_user = User(
                telegram_id=telegram_user.id,
                username=telegram_user.username,
                first_name=telegram_user.first_name,
                balance=0.0,
                purchases=0,
                is_active=True,
            )
            session.add(db_user)

            print(f"New user created: {telegram_user.username} ({telegram_user.id})")

        return db_user



def get_user_by_telegram_id(telegram_id: int) -> None:
    with sql_cursor() as session:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        return user



