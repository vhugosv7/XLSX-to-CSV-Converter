import os
from flask import Flask, request, redirect, render_template, url_for
import pandas as pd
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'your_path/XLSX to CSV'

ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#  From Flask documentation.

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    #  To get filename from user selection.
    filename = ""
    # The file uploaded will be stored in the main folder. Change it on line 6.
    if request.method == 'POST':
        # Function to display File datails.
        get_name(filename)
        # If the extension file is not in allowed_extensions
        if 'file' not in request.files:
            return redirect(url_for('error'))
        file = request.files['file']

        # If there is not file selected when the button "upload" is clicked
        # will be redirect to error page.
        if file.filename == '':
            return redirect(url_for('error'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #  Csv function
            to_csv(filename)

        return render_template('upload.html', filename=filename,
                               df=get_name(filename))

    return render_template('upload.html', filename=filename,
                           df=get_name(filename))


#  This function shows the xlsx details
def get_name(filename):
    #  To store column headers.
    headers = []
    if filename:
        print(f" The uploaded file is: {filename}")
        df = pd.read_excel(filename)

        for item in df.axes[1]:
            headers.append(item)
        # Size and empty status detail.
        df_size = df.size
        df_empty = df.empty
        return headers, df_size, df_empty
    else:
        return ""


def to_csv(filename):
    # Reading the excel file.
    df = pd.read_excel(filename)
    # Storing the df as csv file in the static folder (Could be changed).
    csv_file = df.to_csv('static/out_csv.csv', index=False)
    # Test line (Could be omitted).
    print("inside csv function")
    return csv_file


@app.route('/error', methods=['GET', 'POST'])
def error():
    # Error page when the user don't upload any file.
    return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=True)
