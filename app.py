from flask import Flask, request, render_template
import os  # for os.path functions

app = Flask(__name__)

# Configure upload folder (adjust as needed)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Outside static folder

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Check if a file is uploaded
        if 'file' not in request.files:
            return {'error': 'No file uploaded'}, 400

        file = request.files['file']
        # Check if the filename extension is .csv
        if not file.filename.endswith('.csv'):
            return {'error': 'Only CSV files are allowed'}, 415

        #filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

        # Save the file to the uploads folder
        file.save(filepath)

        # Process the uploaded file using pandas or other libraries (optional)
        # ...

        return {'message': 'File uploaded successfully'}, 200

    return {'error': 'Invalid request method'}, 405 



@app.route('/analysis/<fileName>', methods = ['GET'])
def analyse(fileName):
    #print(fileName)

    return render_template('analysis.html', data = {'fileName': fileName})







if __name__ == '__main__':
    app.run(debug=True)
