import pandas as pd
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import os
import pickle
import datetime
import re
from os import listdir

UPLOAD_FOLDER = os.path.join(os.getcwd() ,"uploads")

app = Flask(__name__, template_folder = 'templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

@app.route('/upload')
def upload_page():
   return render_template("upload.html")
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join("uploads", secure_filename(f.filename)))
      return render_template('process.html')
		

@app.route('/process', methods = ['GET', 'POST'])
def process_page():
   # gets the X_test csv file 
   filename = os.path.join('./uploads/', listdir('./uploads')[0])
   X_test = pd.read_csv(filename, index_col=0)
   loaded_model = pickle.load(open('./models/model_new_features_balanced.sav', 'rb'))
   result = loaded_model.predict(X_test)
   result = pd.DataFrame(result, index=X_test.index, columns=['prediction'])
   txt = str(datetime.datetime.now())
   current_timestamp = re.sub('[- :]', '', txt)[:14]
   filename = os.path.join('./results/', current_timestamp + '.' + 'csv')
   result.to_csv(filename)
   return "See the results folder."

if __name__ == '__main__':
   app.run()