from flask import Flask, request, render_template, jsonify
import os  # for os.path functions
from dotenv import load_dotenv

#Below function runs and load environment variables into os
load_dotenv()

#Creation of app
app = Flask(__name__)

# Configure upload folder (adjust as needed)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Outside static folder

@app.route('/')
def index():
    #get data about nifty performance
    #get data about market performance distribution
    #get data about different other things
    #pack all the data into json format and sent to index.html
    #at index.html, frontend will seperate the data using js and do the neccesary.
    sample_data = {
    'dates': ['2024-06-01', '2024-06-02', '2024-06-03', '2024-06-04', '2024-06-05'],
    'open': [100, 105, 102, 108, 107],
    'high': [110, 107, 105, 112, 109],
    'low': [95, 100, 101, 105, 104],
    'close': [105, 102, 108, 107, 106]
    }
    return render_template('index.html', data=sample_data)


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



PORT_NO = int(os.getenv('PORT', 5000))#Default to 5000 if PORT not found
if __name__ == '__main__':
    app.run(port = PORT_NO, debug=True)
