from models import Base, User, User_group
import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy.orm import scoped_session, declarative_base, sessionmaker
from sqlalchemy import select


if __name__ == '__main__':
    load_dotenv()

    password = str(os.getenv("DB_PASSWORD"))
    database = str(os.getenv("DB_DATABASE"))

    engine = create_engine(f"postgresql+psycopg2://postgres:{password}@localhost/{database}",pool_pre_ping=True ) # , echo=True

    print("del TABLES >>>> ")
    Base.metadata.drop_all(bind=engine)

    print("CREATING TABLES >>>> ")
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    session.merge(User_group(
        id=1,
        group_name="admins"
    ))
    session.merge(User_group(
        id=2,
        group_name="users"
    ))
    session.merge(User_group(
        id=3,
        group_name="banned"
    ))
    session.commit()

    sqlgroup = (
        select(User_group).where(User_group.group_name == "users")
    )
    group = session.scalars(sqlgroup).one()

    session.merge(User(
        telegram_id=415131308,
        first_name="Nikita",
        last_name="main Admin",
        username='nkt_tyupin',
        is_bot=False,
        language_code='ru',

        groups=[group]
    ))
    session.commit()


    '''
    Session = sessionmaker(bind=engine)
    session = Session()

    # Создаем записи в таблице users_groups
    admins_group = User_group(group_name='admins')
    users_group = User_group(group_name='users')
    banned_group = User_group(group_name='banned')

    session.add_all([admins_group, users_group, banned_group])
    session.commit()
'''