from typing import Optional
from modules.user import User
import os
from sqlalchemy.engine import create_engine

# Prepare mysql connection
mysql_url = os.environ.get('SQL_DB_URL', '127.0.0.1:3306')
mysql_user = 'root'
mysql_password = os.environ.get('SQL_DB_PASSWORD')
database_name = 'pymanoDB'
connection_url = 'mysql://{user}:{password}@{url}/{database}'.format(
    user=mysql_user,
    password=mysql_password,
    url=mysql_url,
    database=database_name
)
mysql_engine = create_engine(connection_url)


def login(
    username: Optional[str] = None, password: Optional[str] = None
) -> Optional[User]:
    """Check the username and password and returns the user if succeeded
    """
    
    if not username or not password:
        return None
    
    with mysql_engine.connect() as connection:
        results = connection.execute(
          "SELECT UserName, PublicId FROM Users WHERE UserName = '{}' AND Password = '{}';".format(username, password))
    
    users = [User(i[0],i[1]) for i in results.fetchall()]
    if len(users) == 0:
        return None
    return users[0]


def get_user(public_id: Optional[str] = None) -> Optional[User]:
    """Get the user having the given public id"""
    with mysql_engine.connect() as connection:
        results = connection.execute(
          "SELECT UserName, PublicId FROM Users WHERE PublicId = '{}';".format(public_id))
        
    users = [User(i[0],i[1]) for i in results.fetchall()]
    if len(users) == 0:
        return None
    return users[0]
