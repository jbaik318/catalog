from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

class Category(Base):
    __tablename__ = 'category'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    
    
    @property
    def serialize(self):
        item = Item()
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'item': []
        }

class Item(Base):
    __tablename__ = 'item'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    description = Column(String(250))
    catType = Column(String(80))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    
    @property
    def serialize(self):
        category = Category()
        """Return object data in easily serializeable format"""        
        return {
                'Name': self.name,
                'Id': self.id,
                'Description': self.description,
                'Category': self.catType,
                'catid': self.category_id
        }
        


engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)