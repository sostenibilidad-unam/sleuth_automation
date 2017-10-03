from pony.orm import Database, Required, Optional
from datetime import datetime
from os.path import join
import hashlib
import random
import sleuth_automation as sleuth

sleuth.configure(sleuth_path='/path/to/sleuth',
                 use_mpi=True, mpi_cores=32)


db = Database()

UPLOAD_PATH = './'


class Job(db.Entity):
    status = Required(str)
    # client_signature = Required(str)
    hash = Required(str)
    date_submited = Required(datetime)
    date_completed = Optional(datetime)
    condor_job_id = Optional(int)

    def __repr__(self):
        return "<job %s %s %s>" % (self.id, self.status, self.hash)

    def set_hash(self):
        self.hash = hashlib.sha224("batch id %s with random %s" % (
            self.id,
            random())).hexdigest()

    def get_path(self):
        path = "%s" % self.hash
        return join(UPLOAD_PATH, path)


    def run(self):
        l = sa.Location('my_location',
                        '/path/to/my_location')

        l.calibrate_coarse()
        l.calibrate_fine()
        l.calibrate_final()

        l.sleuth_calibrate()

        l.sleuth_predict(2017, 2060)

        l.gif2tif(2017, 2060)
