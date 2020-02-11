
from flask import *

import pickle
from werkzeug.security import generate_password_hash,check_password_hash

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity,
    )


import json

from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import tokenizer_from_json, Tokenizer
import numpy as np
tk=Tokenizer()
with open('tokenizer.json') as f:
    data = json.load(f)
    tk = tokenizer_from_json(data)



from mongodbconfiguration import *

goodmodel = load_model('best_model2.hdf5')



app = Flask(__name__)
app.config['JWT_SECRET_KEY']='secret'
app.config['JWT_TOKEN_LOCATION']=['headers']

JWTManager(app)


@app.route("/",methods=['GET'])
def hello():
    return render_template('login.html')

@app.route("/login",methods=['POST'])
def login():
    if request.method== 'POST':
        jsonreq=request.get_json()
        email=jsonreq['email']
        password=jsonreq['password']
        print(email+" "+password)


        obj= collection.find({"email":email})
        if(obj.count()>0):
            dit={}
            for objdata in obj:
                dit={"email":objdata['email'],"password":objdata['password']}
                passwordfromdatabase=dit.get('password')

                if(not check_password_hash(passwordfromdatabase,password)):
                    return jsonify({"message":"email or password is incorrect"})
                else:
                    token=create_access_token(identity=email)
                    bearertoken=token

                    return jsonify({"message":"successfully logged in","accesstoken":token})


        else:
            return jsonify({"message":"user does not exist"})
@app.route("/register", methods=['POST'])
def register():
    if request.method=='POST':
        requestjson=request.get_json()
        firstname=requestjson['firstname']
        lastname=requestjson['lastname']
        email=requestjson['email']
        password=requestjson['password']

        if firstname and lastname and email and password :
            hashedpassword=generate_password_hash(password)
            collection.insert_one({'firstname':firstname,
                                    'lastname':lastname,
                                    'email':email,
                                    'password':hashedpassword
                                   })
            resp=jsonify('user inserted successfully')
            resp.status_code=200
            return jsonify("user inserted succesfully")
        else:
            return jsonify("error occured")



@app.route('/model',methods=['GET'])
@jwt_required
def model():
    user=get_jwt_identity()
    if(user):
        return jsonify({"message":"logged in as {}".format(user)})
    else:
        return jsonify({"message":"no user"})

@app.route('/getReview',methods=['POST'])
def getReview():
    if(request.method=='POST'):
        requbody=request.get_json()
        review=requbody['review']
        print(review)
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        no_punct = ""
        for char in review:
            if char not in punctuations:
                no_punct = no_punct + char
        msg=[]
        msg.append(no_punct)
        print(msg)
        # tk.fit_on_text
        #print(msg)
        twt=msg
        goodmodel.summary()
        twt = tk.texts_to_sequences(twt)
        twt = pad_sequences(twt, maxlen=50, dtype='int32', value=0)
        print(twt)
        sentiment = goodmodel.predict(twt, batch_size=1, verbose=2)[0]
        print(sentiment)

        negative=sentiment[0]
        positive=sentiment[1]
        negative=round(negative,3)
        positive=round(positive,3)
        print(positive)
        print(negative)
        obj={"msg":review,"result":str(positive-negative)}
        return jsonify(obj)
    else:
        return "null"


@app.route("/modelview",methods=['GET'])
def modelview():
    return render_template('model.html')


if (__name__ == '__main__'):
    app.run(threaded=False)
