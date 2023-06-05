import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle as pkl

train_data = pd.read_csv("train.csv")
test_data = pd.read_csv("test.csv")
train_data.head()

x_train = train_data.drop(["presence_of_dyslexia"], axis= "columns")
x_test = test_data.drop(["presence_of_dyslexia"], axis= "columns")
y_train = train_data.presence_of_dyslexia
y_test = test_data.presence_of_dyslexia

model_rfc = RandomForestClassifier(n_estimators=100)
model_rfc.fit(x_train.values, y_train.values)

pkl.dump(model_rfc, open("ImageModel.pkl", 'wb'))