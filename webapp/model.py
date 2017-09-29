from pony.orm import db_session, Database, Required, Json, Set
from datetime import datetime
from os.path import join


db = Database()


class Experiment(db.Entity):
    name = Required(str)
    batch = Required(Batch)
    condor_job_id = Optional(id)

    def get_location(self):
        return join(UPLOAD_PATH, self.id)
            

class Batch(db.Entity):
    status = Required(str)
    client_signature = Required(str)
    locations = Set('Location')
    date_created = Required(datetime)
    date_submited = Optional(datetime)
    date_completed = Optional(datetime)
    

    def __repr__(self):
        return "<bike %s %s %s>" % (self.id, self.lon, self.lat)
