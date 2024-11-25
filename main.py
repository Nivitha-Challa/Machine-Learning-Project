from flask import Flask,render_template,request,send_from_directory
import numpy as np
import joblib
import json
import os
import pandas as pd

app = Flask(__name__)


UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER
app.config['DOWNLOADS'] = UPLOAD_FOLDER

rf = joblib.load("random_forest.joblib")

@app.route('/')
def index():
    return render_template("new.html")

@app.route('/hello')
def hello():
    return "hello"
@app.route('/result',methods=['POST'])
def result():
    if request.method == "POST":
        data = request.form
        #print(data)
        req = data['msg']
        req = req.split('&')
        values = []
        for i in req[:-1]:
            i = i.split('=')
            values.append(float(i[1]))
        if req[-1].split('=')[-1] == 'yes':
            values.append(1)
        else:
            values.append(0)
        # print(values)
        
        ar = np.array(values)
        ans = rf.predict([ar])
        resp = ['NOT CKD','CKD']
        # print(resp[ans[0]])
        return json.dumps(
            {
              'data': resp[ans[0]]
            }
        )
@app.route('/files',methods=['POST'])
def file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
          # set the file path
        uploaded_file.save(file_path)
          # save the file
        df=pd.read_csv(UPLOAD_FOLDER+'/'+uploaded_file.filename)
        results = list(rf.predict(df))
        print(results)
        result = [f"{i[0]}:CKD" if i[1] == 1 else f"{i[0]}:NOT CKD" for i in enumerate(results)]
        result = "\n".join(result)
        print(result)
        filename='results.txt'
        with open(UPLOAD_FOLDER+'/results.txt','w') as f:
            f.write(result)
        try:
            return send_from_directory('static/files/',filename,as_attachment=True)
        except FileNotFoundError:
            os.abort(404)
    return render_template('new.html')
if __name__ == "__main__":
    app.run(debug=True)
