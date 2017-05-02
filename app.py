import os
import csv
import StringIO
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import (Flask, render_template, request, redirect, url_for,
                   send_from_directory, make_response)
from werkzeug import secure_filename

# Initialize the Flask application
app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', ])

# For a given file, return whether it's an allowed type or not


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation


@app.route('/')
def index():
    return render_template('index.html')


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        temp = file.read().splitlines()
        data_line = 0
        parsed = []
        for item in temp:
            if 'Data' in item:
                data_line += 1
            else:
                if 1 <= data_line <= 9:
                    result = item.split()
                    if len(result) > 12:
                        parsed.append(result[1:])
                    data_line += 1
        output_fn = filename.split('.')[0] + '.csv'
        index = 1
        si = StringIO.StringIO()
        cw = csv.writer(si)
        for j in range(12):
            for i in range(8):
                cw.writerow([index, parsed[i][j]])
                index += 1
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=%s" % output_fn
    output.headers["Content-type"] = "text/csv"
    return output


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )
