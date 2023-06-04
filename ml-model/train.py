import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import pickle as pkl


train_data = pd.read_csv("train.csv")
test_data = pd.read_csv("test.csv")
train_data.head()

x_train = train_data.drop(["presence_of_dyslexia"], axis="columns")
x_test = test_data.drop(["presence_of_dyslexia"], axis="columns")
y_train = train_data.presence_of_dyslexia
y_test = test_data.presence_of_dyslexia

# Linear Regression Model
model_logistic = LogisticRegression()
model_logistic.fit(x_train, y_train)

# Decision Tree Model
model_DT = DecisionTreeClassifier()
model_DT.fit(x_train, y_train)

# Support Vector Machine Model
model_svc_linear = SVC(kernel='linear', gamma='scale', shrinking=False,)
model_svc_linear.fit(x_train, y_train)

# Random Forest Model
model_rfc = RandomForestClassifier(n_estimators=100)
model_rfc.fit(x_train.values, y_train.values)

pkl.dump(model_rfc, open("model.pkl", 'wb'))

# model = pkl.load(open("model.pkl", 'rb'))
# print(model.predict([[0.12, 6.2]]))
