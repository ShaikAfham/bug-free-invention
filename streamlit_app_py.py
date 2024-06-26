# -*- coding: utf-8 -*-
"""streamlit_app.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1udEcn0m49NmlremyRMJQyTITYYmrLJ_h
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np

import matplotlib.pyplot as plt

from sklearn.datasets import load_digits

from sklearn.preprocessing import StandardScaler

from sklearn.model_selection import train_test_split

from sklearn.svm import SVC

from sklearn.neighbors import KNeighborsClassifier

from sklearn.tree import DecisionTreeClassifier

from sklearn.ensemble import AdaBoostClassifier

from sklearn.neural_network import MLPClassifier

from sklearn.metrics import accuracy_score , confusion_matrix , classification_report

# %matplotlib inline

digits = load_digits()

print(digits.DESCR)

digits.data.shape

digits.target.shape

digits.images.shape

img = list(zip(digits.images , digits.target))

for i , (image,label) in enumerate(img[:10]):

    plt.subplot(2,5,i+1)

    plt.axis('off')

    plt.imshow(image,cmap=plt.cm.gray_r,interpolation='nearest')

    plt.title('Value %i' % label)

X_train , X_test , Y_train , Y_test = train_test_split(digits.data , digits.target , test_size = 0.3 , random_state = 2018)

sc = StandardScaler()

X_train_std = sc.fit_transform(X_train)

X_test_std = sc.transform(X_test)

svm_clf = SVC(kernel='rbf' , gamma = 0.001 , C = 1)

knn_clf = KNeighborsClassifier(n_neighbors = 3)

dt = DecisionTreeClassifier(max_depth = 3 , criterion = 'entropy' , random_state = 2018)

ada = AdaBoostClassifier(base_estimator = dt , n_estimators = 1000 , learning_rate = 0.1 , random_state = 2018)

mlp = MLPClassifier(activation = 'logistic' , solver = 'sgd' , learning_rate_init = 0.001 , learning_rate = 'constant' , alpha = 1e-4 , hidden_layer_sizes = (100,) , max_iter = 5000 , shuffle = True , random_state = 2018 )

svm_clf.fit(X_train_std , Y_train)

knn_clf.fit(X_train_std , Y_train)

ada.fit(X_train_std , Y_train)

mlp.fit(X_train_std , Y_train)

svm_pred = svm_clf.predict(X_test_std)

knn_pred = knn_clf.predict(X_test_std)

ada_pred = ada.predict(X_test_std)

mlp_pred = mlp.predict(X_test_std)

print("Accuracy Score SVM" , accuracy_score(Y_test , svm_pred))

print("Accuracy Score KNN" , accuracy_score(Y_test , knn_pred))

print("Accuracy Score AdaBoost" , accuracy_score(Y_test , ada_pred))

print("Accuracy Score MLP" , accuracy_score(Y_test , mlp_pred))

from sklearn.model_selection import GridSearchCV

knn1 = KNeighborsClassifier()

clf_knn1 = GridSearchCV(knn1 , {'n_neighbors':[i for i in range(1,100)]})

clf_knn1.fit(X_train_std , Y_train)

print(clf_knn1.best_params_)

from sklearn.ensemble import VotingClassifier

from sklearn.pipeline import Pipeline

pipe_knn = Pipeline([['sc', StandardScaler()], ['knn_clf' , knn_clf]])



pipe_svm = Pipeline([['sc', StandardScaler()], ['svm_clf' , svm_clf]])



mv = VotingClassifier(estimators = [('ada',ada),('knn',pipe_knn),('svm' , pipe_svm)] , voting = 'hard')



mv.fit(X_train_std , Y_train)



mv_pred = mv.predict(X_test_std)



print("Accuracy Score Majority Voting" , accuracy_score(Y_test , mv_pred))

pipe_mlp = Pipeline([['sc', StandardScaler()], ['mlp' , mlp]])



mv1 = VotingClassifier(estimators = [('ada',ada),('knn',pipe_knn),('svm' , pipe_svm),('mlp' , pipe_mlp)] , voting = 'hard')



mv1.fit(X_train_std , Y_train)



mv1_pred = mv1.predict(X_test_std)



print("Accuracy Score Majority Voting including MLP" , accuracy_score(Y_test , mv1_pred))

from PIL import Image

import numpy as np

from sklearn import datasets



# Load the image

img = Image.open('/content/image.png')



# Resize the image

img = img.resize((8, 8))



# Convert the image to grayscale

img = img.convert('L')



# Load the digits dataset

digits = datasets.load_digits()



# Convert the PIL Image object to a NumPy array

img = np.array(img)



# Convert the image to the same data type as the digits images

img = img.astype(digits.images.dtype)



# Flatten the image array

arr = []

for eachRow in img:

    for eachPixel in eachRow:

        arr.append(eachPixel)



# Predict the digit

print("Prediction is:")

print(knn_clf.predict([arr]))