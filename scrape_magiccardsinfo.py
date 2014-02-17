import os
import sqlalchemy

from sqlalchemy import orm

from pymtgoracle.model import base
from pymtgoracle.scrapers import magiccardsinfo

def main():
  db_location = './mtgoracle.sqlite'
  db_filename = os.path.expanduser(db_location)
  dbbak_filename = db_filename + '.bak'
  
  if os.path.exists(dbbak_filename):
    os.remove(dbbak_filename)
  if os.path.exists(db_filename):
    os.rename(db_filename, dbbak_filename)
    
  engine = sqlalchemy.create_engine('sqlite:///%s' % db_filename, echo=False)
  base.Base.metadata.create_all(engine)
  
  session_factory = orm.sessionmaker(
      bind=engine, autoflush=True, autocommit=False)
  session = orm.scoped_session(session_factory)
  
  try:
    scraper = magiccardsinfo.MagicCardsInfoScraper(session, verbose=True)
    scraper.scrape_setlist()
    #scraper.scrape_set('ME3')
    scraper.scrape_all()
  except:
    session.rollback()
    raise
  else:
    session.commit()
  finally:
    session.close()

if __name__ == '__main__':
  main()
