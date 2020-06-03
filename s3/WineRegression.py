import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
import matplotlib.pyplot as pyplot
from matplotlib import style
import pickle

data = pd.read_csv("winequality-red.csv", sep=";")
# print(data.head())


predicted_term = "quality"

x = np.array(data.drop([predicted_term], 1))
y = np.array(data[predicted_term])
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)


best = 0
for _ in range(10000):
    model = linear_model.LinearRegression()

    # Find the best fitting line
    model.fit(x_train, y_train)

    accuracy = model.score(x_test, y_test)

    if accuracy > best:
        # Saving the model
        with open("winemodel.pickle", "wb") as f:
            pickle.dump(model, f)
        best = accuracy
        print("Best accuracy: " + str(best))

# Loading the model
pickle_in = open("winemodel.pickle", "rb")
model = pickle.load(pickle_in)

# Printing out he coefficients and the Y- Intercepts
print("\n\n---Process terminated---\nBest accuracy: " + str(best))
print("Coefficients found: " + str(model.coef_) + "\n")
print("Y - Intercept found: " + str(model.intercept_) + "\n")

prediction = model.predict(x_test)

for x in range(len(prediction)):
    print("Data used to train: " + str(x_test[x]))
    print("Prediction: " + str(prediction[x]))
    print("Real result: " + str(y_test[x]) + '\n')
