import numpy as np
import sklearn
from sklearn.preprocessing import scale
from sklearn.datasets import load_digits
from sklearn.cluster import KMeans
from sklearn import metrics

digits = load_digits()

data = scale(digits.data)
y = digits.target

k = 10
samples, features = data.shape


def bench_k_means(estimator, name, dt):
    estimator.fit(dt)
    print('%-9s\t%i\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f'
          % (name, estimator.inertia_,
             metrics.homogeneity_score(y, estimator.labels_),
             metrics.completeness_score(y, estimator.labels_),
             metrics.v_measure_score(y, estimator.labels_),
             metrics.adjusted_rand_score(y, estimator.labels_),
             metrics.adjusted_mutual_info_score(y, estimator.labels_),
             metrics.silhouette_score(dt, estimator.labels_, metric='euclidean')))


clf = KMeans(n_clusters=k, init='random', n_init=10, max_iter=300)
bench_k_means(clf, "clf#1", data)

prediction = clf.predict(digits, sample_weight=0.1)
for x in range(len(prediction)):
    print()
