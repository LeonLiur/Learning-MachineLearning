import pandas as pd
import sklearn
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

data = pd.read_csv("seeds_dataset.csv")
print(data.head())

predicted_term = "class"
x = np.array(data.drop([predicted_term], 1))
y = np.array(data[predicted_term])

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.05)

model = KNeighborsClassifier(n_neighbors=7)

model.fit(x_train, y_train)

accuracy = model.score(x_test, y_test)

class_names = ["Kama", "Rosa", "Canadian"]

predictions = model.predict(x_test)
for x in range(len(predictions)):
    print("Data used to train: " + str(x_test[x]))
    print("Predicted class: " + class_names[predictions[x]-1])
    print("Actual class: " + class_names[y_test[x]-1])
