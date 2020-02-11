import json

from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import tokenizer_from_json
import numpy as np
from nltk.corpus import stopwords

model=load_model('best_model2.hdf5')
twt=["he is not good at coding."]
print(twt)


#tk.fit_on_text

msg=[]
msg.append(twt)
with open('tokenizer.json') as f:
    data = json.load(f)
    tk = tokenizer_from_json(data)
    twt = tk.texts_to_sequences(msg)
print(twt)

#padding the tweet to have exactly the same shape as `embedding_2` input
twt = pad_sequences(twt, maxlen=50, dtype='int32', value=0)
print(twt)
sentiment = model.predict(twt,batch_size=1,verbose=2)[0]
print(sentiment)
if(np.argmax(sentiment)==0):
    print("negative")
elif (np.argmax(sentiment)==1):
    print("positive")
