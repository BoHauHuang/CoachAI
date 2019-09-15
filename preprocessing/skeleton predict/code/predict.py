import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from sklearn.externals import joblib
from sklearn import svm
from sklearn.metrics import *
from xgboost import XGBClassifier
import itertools
import matplotlib.pyplot as plt

needed = ['ball_round', 'pos_x', 'pos_y', 'next_x', 'next_y', 'hit_height']
test_needed = ['ball_round', 'pos_x', 'pos_y', 'next_x', 'next_y']

def convert_area(area):
	val = {'E': 0, 'C': 4, 'A': 8, 'B': 12, 'D': 16}
	return float(val[area[0]]+float(area[1]))

def LoadData(filename):
	data = pd.read_csv(filename)
	data = data[needed]
	data.dropna(inplace=True)
	x_predict = data[test_needed]

	return x_predict

def plot_Confusion_Matrix(set_now, model_type, cm, groundtruth, grid_predictions, classes):
    plt.imshow(cm, cmap=plt.cm.Blues)
    plt.title('Confusion matrix')
    plt.colorbar()
    plt.xlabel('Actual Class')
    plt.ylabel('Predicted Class')
    plt.xticks(np.arange(len(classes)-1), classes)
    plt.yticks(np.arange(len(classes)-1), classes)
   
    for j, i in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if i == j:
            plt.text(i+0.03, j+0.2, str(format(cm[j, i], 'd'))+'\n'+str( round(precision_score(groundtruth, grid_predictions, average=None)[i]*100,1))+'%', 
            color="white" if cm[j, i] > cm.max()/2. else "black", 
            horizontalalignment="center")
        else:
            plt.text(i, j, format(cm[j, i], 'd'), 
            color="white" if cm[j, i] > cm.max()/2. else "black", 
            horizontalalignment="center")

    plt.savefig(str(model_type)+'_set'+str(set_now)+'_confusion_matrix.png')
    plt.close(0)

def plot_chart(set_now, model_type, model, groundtruth, grid_predictions, labels):
    # feature importance
    #feature_importance(model)
    # confusion matrix
    plot_Confusion_Matrix(set_now, model_type, confusion_matrix(groundtruth, grid_predictions), groundtruth, grid_predictions, labels)
    plt.clf()
    plt.close()

def SVM(filename, x_predict, model_name, xgb_outputname, set_now):
	data = pd.read_csv(filename)
	data = data[needed]
	data.dropna(inplace=True)
	label = [1, 2]

	model = joblib.load(model_name)
	prediction = model.predict(x_predict)

	result = pd.DataFrame([])
	result['Real'] = data['hit_height']
	result['Predict'] = prediction

	result.to_csv(svm_outputname,index=None)

	print("Accuracy: "+str(accuracy_score(data['hit_height'], prediction)))
	print("Precision: "+str(precision_score(data['hit_height'], prediction, labels = label, average=None)))
	print("Recall: "+str(recall_score(data['hit_height'], prediction, labels = label, average=None)))

def XGBoost(filename, x_predict, model_name, xgb_outputname, set_now):
	data = pd.read_csv(filename)
	data = data[needed]
	data.dropna(inplace=True)
	label = [1, 2]

	model = joblib.load(model_name)
	prediction = model.predict(x_predict)

	result = pd.DataFrame([])
	result['Real'] = list(data['hit_height'])
	result['Predict'] = prediction

	result.to_csv(xgb_outputname, index=None)

	print("Accuracy: "+str(accuracy_score(data['hit_height'], prediction)))
	print("Precision: "+str(precision_score(data['hit_height'], prediction, labels = label, average=None)))
	print("Recall: "+str(recall_score(data['hit_height'], prediction, labels = label, average=None)))

	# plot result chart
	plot_chart(set_now, "XGB", model, list(data['hit_height']), prediction, label)


def Run(set_now, filename, svm_option, svm_model_name, svm_outputname, xgboost_option, xgboost_model_name, xgboost_outputname):
	x_predict = LoadData(filename)
	if svm_option and svm_model_name != '':
		print("SVM predicting set"+str(set_now)+"...")
		print("")
		SVM(filename, x_predict, svm_model_name, svm_outputname, set_now)
		print("")
		print("SVM predict set"+str(set_now)+" done!")

	if xgboost_option and xgboost_model_name != '':
		print("XGBoost predicting set"+str(set_now)+"...")
		print("")
		XGBoost(filename, x_predict, xgboost_model_name, xgboost_outputname, set_now)
		print("")
		print("XGBoost predict set"+str(set_now)+" done!")


def exec(predict_set):
	for i in predict_set:
		Run(i, '../data/set'+str(i)+'_with_skeleton.csv', False, 'SVM_skeleton.joblib.dat', 'SVM_set'+str(i)+'_skeleton_out.csv', True, 'XGB_skeleton.joblib.dat', 'XGB_set'+str(i)+'_skeleton_out.csv')
exec([2, 3])