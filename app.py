from flask import Flask,render_template,request
import pickle

popularProducts = pickle.load(open('productNames.pkl','rb'))
recommendModel = pickle.load(open('model.pkl','rb'))

# Open APP API
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


app = Flask(__name__)

# Home Page Route
@app.route('/')
def home():
    return render_template('index.html',
                            stock_code = list(popularProducts['StockCode'].values),
                            product= list(popularProducts['Description'].values)
    )

# recommendation Search page route
@app.route('/recommend')
def recommend():
    return render_template('recommendProdu.html')

# Recommending Products Route
@app.route('/recommendProd',methods=['POST'])
def recommendProd():
    userPd = request.form.get('userPd') 
    userPd = str(userPd)
    top_10_similar_items = list(recommendModel.loc[userPd].sort_values(ascending=False).iloc[:4].index)
    
    data = []
    for stock_code in top_10_similar_items:
        item_info = popularProducts[popularProducts['StockCode'] == stock_code][['StockCode', 'Description']]
        if not item_info.empty:
            item = {
                'StockCode': stock_code,
                'Description': item_info['Description'].values[0]  # Assuming there's only one unique description per stock_code
            }
            data.append(item)

    return render_template('recommendProdu.html',data = data)

  


if __name__ == '__main__':
    app.run(debug=True)
