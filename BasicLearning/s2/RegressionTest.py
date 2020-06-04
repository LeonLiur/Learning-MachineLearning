import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
import matplotlib.pyplot as pyplot
from matplotlib import style
import pickle

data = pd.read_csv("student-mat.csv", sep=";")

data = data[["G1", "G2", "G3", "studytime", "absences", "failures"]]
# data = data[["G1", "G3"]]
# print(data.head())

predicted_term = "G3"
# "G3" -> 'lable' in this case

x = np.array(data.drop([predicted_term], 1))
y = np.array(data[predicted_term])

'''best = 0
for _ in range(100):
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)
    linear = linear_model.LinearRegression()

    # Find the best fitting line
    linear.fit(x_train, y_train)

    accuracy = linear.score(x_test, y_test)

    # Saving the model
    if accuracy > best:
        with open("studentmodel.pickle", "wb") as f:
            pickle.dump(linear, f)
        best = accuracy
        print("Best accuracy: " + str(best))'''


# Printing the model
pickle_in = open("studentmodel.pickle", "rb")
linear = pickle.load(pickle_in)

# print("\nProcess complete, final accuracy: " + str(accuracy))
print("Coefficient found: " + str(linear.coef_) + "\n")
print("Y-intercept found: " + str(linear.intercept_) + "\n")

predictions = linear.predict(x_test)

for x in range(len(predictions)):
    print("\nPrediction:" + str(predictions[x]) + "\t")
    print("Data used to train: " + str(x_test[x]) + "\t")
    print("Real G3 value: " + str(y_test[x]))

p = 'G1'
style.use("ggplot")
pyplot.scatter(data[p],data["G3"])
pyplot.xlabel(p)
pyplot.ylabel("Final Grade")
pyplot.show()
