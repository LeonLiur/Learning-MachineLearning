import sklearn
from sklearn import datasets
from sklearn import svm
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier

cancer = datasets.load_breast_cancer()

x = cancer.data
y = cancer.target

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.05)

classes = ['malignant', 'benign']

clf = svm.SVC(kernel="linear", C=2)
clf.fit(x_train, y_train)

y_pred = clf.predict(x_test)

accuracy = metrics.accuracy_score(y_test,y_pred)
print(accuracy)

predictions = clf.predict(x_test)
for x in range(len(predictions)):
    print("Data used to train: " + str(x_test[x]))
    print("Predicted class: " + classes[predictions[x]])
    print("Actual class: " + classes[y_test[x]])
