from jinja2 import Environment, FileSystemLoader
from flask import Flask, send_from_directory
from flask import jsonify, Response
from flask_cors import CORS


import sleuth_automation as sleuth
from os.path import join


app = Flask(__name__, static_url_path='')
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
CORS(app)



@app.route('/sleuth/new_batch/')
def new_batch():
    """
    Start webservice session. One session per qgis-plugin client.
    """
    batch_id = 1
    return jsonify(batch_id)


@app.route('/sleuth/<batch_id>/add_location/')
def add_location(batch_id):
    """
    Add location to region package for group submission.
    """
    pass

@app.route('/sleuth/<batch_id>/submit/')
def submit_batch(batch_id):
    """
    Submit batch to condor
    """
    # predict_start, predict_end, montecarlo_iterations <- get these from request

    
    # parser = argparse.ArgumentParser(description=description)

    # parser.add_argument('--sleuth_path', required=True,
    #                     help='path to SLEUTH directory')
    # parser.add_argument('--locations_dir',
    #                     required=True,
    #                     help='path to regions dir')
    # parser.add_argument('--mpi_cores', default=0,
    #                     help="""number of cores available for MPI,
    #                     if 0 (default) don't use mpi""")

    env = Environment(loader=PackageLoader('sleuth_automation',
                                           'templates'))

    list_of_regions = []
    for thisFile in os.listdir(args.locations_dir):
        if os.path.isdir(join(args.locations_dir, thisFile)):
            list_of_regions.append({"name": thisFile,
                                    "path": abspath(join(args.locations_dir,
                                                         thisFile)) + '/'})

    template = env.get_template("sleuth_template.condor")

    with open(join(args.locations_dir, 'submit.condor'), 'w') as f:
        f.write(template.render({'executable': which('sleuth_run.py'),
                                 'list_of_regions': list_of_regions,
                                 'predict_start': args.predict_start,
                                 'predict_end': args.predict_end,
                                 'sleuth_path': args.sleuth_path,
                                 'mpi_cores': args.mpi_cores,
                                 'montecarlo_iterations': args.montecarlo_iterations,
                                 'virtualenv': os.environ.get('VIRTUAL_ENV',
                                                              None)}))

    # condor_submit submit.condor
    return jsonify({'status': 'ok'})

@app.route('/sleuth/<batch_id>/submit/')
def run_status(region_id):
    """
    Update run status from logs to db.
    Return status from db.
    """
    pass


def batch_rm(batch_id):
    pass
