from database import Base
from sqlalchemy import Column , Integer,String, Boolean , ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
class Post(Base):
    __tablename__ = "posts"

    id = Column('id', Integer, primary_key = True, nullable = False)
    owner_id = Column('owner_id',Integer,ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    title = Column('title', String, nullable = False)
    content = Column('content', String, nullable = False)
    published = Column('published', Boolean, server_default ='TRUE', nullable= False)
    created_at = Column('created_at',TIMESTAMP(timezone=True),nullable = False,
                         server_default =text('now()'))
    owner = relationship("User")
    
class User (Base):
    __tablename__ = "users"
    
    id = Column('id', Integer, primary_key = True, nullable = False)
    name=Column('name',String,nullable=False)
    email = Column('email',String, nullable=False, unique=True)
    password = Column('password',String,nullable=False)
    created_at = Column('created_at',TIMESTAMP(timezone=True),nullable = False,
                         server_default =text('now()'))
    
class Vote (Base):
    __tablename__ = "votes"

    post_id = Column("post_id" , Integer , ForeignKey("posts.id",ondelete="CASCADE"),primary_key = True, nullable = False)
    user_id =Column("user_id" , Integer , ForeignKey("users.id",ondelete="CASCADE"),primary_key = True, nullable = False)