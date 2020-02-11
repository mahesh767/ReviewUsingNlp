import gc
import csv
import io
import json

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from nltk import TweetTokenizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense, Input, LSTM, Embedding, Dropout, Activation, Conv1D, GRU, GRU, LSTM, BatchNormalization
from keras.layers import Bidirectional, GlobalMaxPool1D, MaxPooling1D, Add, Flatten
from keras.layers import GlobalAveragePooling1D, GlobalMaxPooling1D, concatenate, SpatialDropout1D
from keras.models import Model, load_model
from keras import initializers, regularizers, constraints, optimizers, layers, callbacks
from keras import backend as K
from keras.engine import InputSpec, Layer
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, TensorBoard, Callback, EarlyStopping
model=load_model('best_model2.hdf5')
#vectorizing the tweet by the pre-fitted tokenizer instance
train = pd.read_csv("train.csv",sep=';')
test = pd.read_csv("test.csv",sep=';',quoting=csv.QUOTE_NONE)
del test['Unnamed: 1']
train['tweet'] = train['tweet'].apply(lambda x : ' '.join([w for w in x.split() if not w.startswith('@') ])  )
test['tweet'] = test['tweet'].apply(lambda x : ' '.join([w for w in x.split() if not w.startswith('@') ])  )
full_text = list(train['tweet'].values) + list(test['tweet'].values)
full_text = [i.lower() for i in full_text if i not in stopwords.words('english') and i not in ['.',',','/','@','"','&amp','<br />','+/-','zzzzzzzzzzzzzzzzz',':-D',':D',':P',':)','!',';']]
model.summary()
tk = Tokenizer(lower = True, filters='')
tk.fit_on_texts(full_text)
tokenizer_json = tk.to_json()
with io.open('tokenizer.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(tokenizer_json, ensure_ascii=False))
twt=["he is very bad at coding but sometimes makes good decision "]
print(twt)

#tk.fit_on_texts(twt)

twt = tk.texts_to_sequences(twt)
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
