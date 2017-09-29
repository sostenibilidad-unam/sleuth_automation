from flask import Flask, send_from_directory
from flask import jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename


import sleuth_automation as sleuth
from os.path import join, dirname, abspath

# test these thusly https://alvinalexander.com/web/using-curl-scripts-to-test-restful-web-services

app = Flask(__name__, static_url_path='')
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
CORS(app)

BASE_DIR = dirname(dirname(abspath(__file__)))

UPLOAD_FOLDER = join(BASE_DIR, 'uploads')

ALLOWED_EXTENSIONS = set(['json', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/sleuth/new_batch/', methods=['POST'])
def new_batch():
    """
    Start webservice session. One session per qgis-plugin client.
    """
    batch_id = 1
    # use hashlib to create batch hash for unguessable dirname
    hash = hashlib.sha224("batch id %s with random %s" % (batch_id, random())).hexdigest()

    return jsonify(batch_id)


@app.route('/sleuth/<batch_id>/add_location/',  methods=['POST'])
def add_location(batch_id):
    """
    Add location to region package for group submission.
    """

    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'status': 'no files?'})

    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        return jsonify({'status': 'no filenames?'})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(join(app.config['UPLOAD_FOLDER'],
                       filename))
    return jsonify({'status': 'ok'})


@app.route('/sleuth/<batch_id>/submit/',  methods=['POST'])
def submit_batch(batch_id):
    """
    Submit batch to condor
    """
    # predict_start, predict_end, montecarlo_iterations <- get these
    # from request

    # parser.add_argument('--sleuth_path', required=True,
    #                     help='path to SLEUTH directory')
    # parser.add_argument('--locations_dir',
    #                     required=True,
    #                     help='path to regions dir')
    # parser.add_argument('--mpi_cores', default=0,
    #                     help="""number of cores available for MPI,
    #                     if 0 (default) don't use mpi""")

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


@app.route('/sleuth/<batch_id>/submit/', methods=['GET'])
def run_status(region_id):
    """
    Update run status from logs to db.
    Return status from db.
    """
    return jsonify({'status': 'ok'})


def batch_rm(batch_id, methods=['GET']):
    return jsonify({'status': 'ok'})


@app.route('/static/<path:path>')
def send(path):
    return send_from_directory('static', path)
