from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open("popular_df.pkl",'rb'))
books = pickle.load(open("books.pkl",'rb'))
pt = pickle.load(open("pt.pkl",'rb'))
similarity_score = pickle.load(open("similarity_score.pkl",'rb'))

app = Flask(__name__)

@app.route('/')

def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_rating'].values),
                           rating=list(popular_df['avg_rating'].values))


@app.route('/recommend')

def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods = ['POST'])

def recommend_books():

    user_input = request.form.get('user_input')
    index = np.where(pt.index==user_input)[0][0]    
    similar_items = sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1],reverse=True)[1:6]
    data = []
    for i in similar_items:
        item = []
        # print(pt.index[i[0]])
        recom_temp =  books[books['Book-Title']==pt.index[i[0]]].drop_duplicates('Book-Title')
        item.extend(list(recom_temp['Book-Title'].values))
        item.extend(list(recom_temp['Book-Author'].values))
        item.extend(list(recom_temp['Publisher'].values))
        item.extend(list(recom_temp['Image-URL-M'].values))
        data.append(item)
    
    # print(data)
    return render_template('recommend.html',data=data)

app.run(debug=True)