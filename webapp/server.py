from flask import Flask, send_from_directory
from flask import jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

from os.path import join, dirname, abspath

# test these thusly
# https://alvinalexander.com/web/using-curl-scripts-to-test-restful-web-services

app = Flask(__name__, static_url_path='')
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
CORS(app)

BASE_DIR = dirname(dirname(abspath(__file__)))
UPLOAD_FOLDER = join(BASE_DIR, 'uploads')
ALLOWED_EXTENSIONS = set(['json', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/sleuth/submit/', methods=['POST'])
def job_submit():
    """
    Submit location for sleuth prediction
    """
    batch_id = 1
    # use hashlib to create batch hash for unguessable dirname
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


    return jsonify(batch_id)

    # condor_submit submit.condor
    return jsonify({'status': 'ok'})


@app.route('/sleuth/<job_id>/status/', methods=['GET'])
def job_status(region_id):
    """
    Update run status from logs to db.
    Return status from db.
    """
    return jsonify({'status': 'ok'})


@app.route('/sleuth/<job_id>/delete/', methods=['GET'])
def job_delete(batch_id, methods=['DELETE']):
    return jsonify({'status': 'ok'})


@app.route('/static/<path:path>')
def send(path):
    return send_from_directory('static', path)
