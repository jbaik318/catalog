from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Category
 
engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()



#Menu for UrbanBurger
category1 = Category(name = "Soccer")
session.add(categoryt1)
session.commit()

category2 = Category(name = "Basketball")
session.add(categoryt2)
session.commit()

category1 = Category(name = "Baseball")
session.add(categoryt1)
session.commit()

category1 = Category(name = "Frisbee")
session.add(categoryt1)
session.commit()

category1 = Category(name = "Snowboarding")
session.add(categoryt1)
session.commit()

category1 = Category(name = "Rocking Climbing")
session.add(categoryt1)
session.commit()

category1 = Category(name = "Foosball")
session.add(categoryt1)
session.commit()

category1 = Category(name = "Skating")
session.add(categoryt1)
session.commit()

category1 = Category(name = "Hockey")
session.add(categoryt1)
session.commit()


print "added menu items!"