import pandas as pd
import sklearn
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing

data = pd.read_csv("car.data")

# Convert data to numerical value
pp = preprocessing.LabelEncoder()
buying = pp.fit_transform(list(data["buying"]))
maint = pp.fit_transform(list(data["maint"]))
doors = pp.fit_transform(list(data["doors"]))
persons = pp.fit_transform(list(data["persons"]))
lug_boot = pp.fit_transform(list(data["lug_boot"]))
safety = pp.fit_transform(list(data["safety"]))
cls = pp.fit_transform(list(data["class"]))

predicted_term = "class"

x = list(zip(buying, maint, doors, persons, lug_boot, safety))
y = list(cls)

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.01)

model = KNeighborsClassifier(n_neighbors=7)

model.fit(x_train, y_train)

accuracy = model.score(x_test, y_test)
print("Accuracy of prediction: " + str(accuracy))

names = ["unacc", "acc", "good", "vgood"]

prediction = model.predict(x_test)


for x in range(len(prediction)):
    print("Data used to train: " + str(x_test[x]))
    print("PRedicted data: " + str(names[prediction[x]]))
    print("Actual data: " + str(names[y_test[x]]))

    # neighbours = model.kneighbors([x_test[x]], 7, True)
    # print("Distance to nearest neighbors: " + str(neighbours) + "\n")
    # print("Indexes of nearest neighbors: " + neighbours)
