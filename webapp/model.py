from pony.orm import db_session, Database, Required, Json, Set
from datetime import datetime

db = Database()


class Location(db.Entity):
    name = Required(str)
    batch = Required(Batch)
    condor_job_id = Optional(id)


class Batch(db.Entity):
    status = Required(str)
    client_signature = Required(str)
    locations = Set('Location')
    date_created = Required(datetime)
    date_submited = Optional(datetime)
    date_completed = Optional(datetime)
    

    def __repr__(self):
        return "<bike %s %s %s>" % (self.id, self.lon, self.lat)
