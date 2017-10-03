from pony.orm import db_session
import model


model.db.bind('sqlite', 'jobs.sqlite', create_db=True)
model.db.generate_mapping(create_tables=True)
