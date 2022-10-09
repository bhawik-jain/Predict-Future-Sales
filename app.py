import numpy as np
from flask import Flask, request,render_template
import pickle
import pandas as pd
from xgboost import  XGBRegressor

app = Flask(__name__)
model = pickle.load(open("XGBR_pkl", "rb"))
data = pickle.load(open('data_for_model.7z', 'rb'))
#data = pd.read_pickle('data_for_model.7z')
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    feature1 = int(request.form.get("SHOPID"))
    feature2 = int(request.form.get('ITEMID'))
    query = data.loc[(data['shop_id']==feature1)&(data['item_id']==feature2)]
    if query.empty:
        return render_template('index.html', prediction_text='Please enter valid SHOP ID and ITEM ID. Shop ID :{}/Item ID:{} not found.'.format(f1,f2))
    else:
        #query=query.drop(['ID','shop_id','item_id'],axis=1)
        query = query[query["date_block_num"] > 2]
        query = query[query["date_block_num"] < 33]
        prediction = model.predict(query)

        output = round(prediction[0].clip(0,20))

        return render_template('index.html', prediction_text='Predicted total sales for next month for SHOP ID :{} and ITEM ID :{} is {}'.format(f1,f2,output))


if __name__ == "__main__":
    
    app.run(debug=True)