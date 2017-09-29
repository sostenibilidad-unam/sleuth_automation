from pony.orm import Database, Required, Set, Optional
from datetime import datetime
from os.path import join


db = Database()


UPLOAD_PATH = './'


class Batch(db.Entity):
    status = Required(str)
    client_signature = Required(str)
    locations = Set('Location')
    date_created = Required(datetime)
    date_submited = Optional(datetime)
    date_completed = Optional(datetime)

    def __repr__(self):
        return "<bike %s %s %s>" % (self.id, self.lon, self.lat)


class Experiment(db.Entity):
    name = Required(str)
    batch = Required(Batch)
    condor_job_id = Optional(id)

    def get_location(self):
        return join(UPLOAD_PATH, self.id)
