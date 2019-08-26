import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import Adam, Adagrad, RMSprop, SGD
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import GridSearchCV

# Just disables the TF warning, doesn't enable AVX/FMA
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def load_datasets(filename):
    # load datasets (filename without -0.csv / -1.csv
    # our convention: 0 is for training data sets, 1 is for test data sets
    train_file = filename + "-0.csv"
    test_file = filename + "-1.csv"
    ds_train = pd.read_csv(train_file, header=None)
    ds_test = pd.read_csv(test_file, header=None)
    ds_train.drop(ds_train.head(1).index, inplace=True)  # drop colnames
    ds_test.drop(ds_test.head(1).index, inplace=True)    # drop colnames

    return ds_train, ds_test


def vrfy_ds(ds):
    # print infos of dataset
    last_col = ds.shape[1] - 1      # get last col of dataset dynamically
    print("Dataset:\n", ds.head())
    print("Dataset types:", ds.dtypes)
    print("Dataset shape:", ds.shape)
    print("'is_bot' column:", ds.groupby([last_col]).size())


def create_features_and_labels(ds):
    # creates features and labels from dataset
    # output / is_bot column must be the last column
    features = ds.iloc[:, 0:-1]     # features from 0 to second last column
    label = ds.iloc[:, -1:]         # last column is label (is_bot)

    # verify
    #print("features:\n", features.head())
    #print("labels:\n", label.head())
    #print("feature shape:", features.shape, "label shape:", label.shape)
    return features, label


def plot_hst(hst):
    # plot history of accuracy and loss of training and eval dataset
    fig, axarr = plt.subplots(2, sharex=True, figsize=(7,7))

    # first subplot (accuracy)
    axarr[0].plot(hst["acc"])
    axarr[0].plot(hst['val_acc'])
    axarr[0].set_title('Model Accuracy and Loss')
    axarr[0].set_ylabel('Accuracy')
    axarr[0].legend(['train', "eval"], loc='upper left')
    axarr[0].grid()

    # second subplot (loss)
    axarr[1].plot(hst['loss'])
    axarr[1].plot(hst['val_loss'])
    axarr[1].set_ylabel('Loss')
    axarr[1].set_xlabel('Epoch')
    axarr[1].grid()

    # set x values to integer again
    plt.xticks(np.arange(len(hst["loss"])))

    # display plot or save in file
    #fig.savefig("loss_acc_training")
    plt.show()


def write_ph(prm, hst):
    # writes best parameters and their history to file param_hists seperated by " = "
    f = open("param_hists", "a")
    f.write("%s = %s\n" % (prm, hst))
    f.close()


def print_results(clf):
    # write mean training accuracy and the parameters of each fit into file
    means = clf.cv_results_['mean_test_score']
    stds = clf.cv_results_['std_test_score']
    params = clf.cv_results_['params']

    # prints and writes mean accuracy and parameters of each fit into file "train_accs" (seperated by " = ")
    f = open("train_accs", "a")
    for mean, stdev, param in zip(means, stds, params):
        print("mean acc %.3f (stdev: %.3f) with: %s" % (mean, stdev, param))
        f.write("%f = %s\n" % (mean, param))
    f.close()
    print("Best Accuracy: %.3f using %s" % (clf.best_score_, clf.best_params_))


# model build function with default variables
def build_model(units= [100, 50, 1],
                input_dimension= 100,
                layer_act_fn= "relu",
                dropout= 0.5,
                k_init= "random_uniform",
                b_init="zeros",
                output_act_fn= "sigmoid",
                optimizer= "SGD",
                learning_rate= 0.01,
                momentum= 0.9,
                decay= 0.2,
                nesterov= False,
                loss_fn= "binary_crossentropy",
                metrics= ["accuracy"],
                custom_verbose= 2):
    """Builds and returns Sequential model"""

    # printfunctions for verbosity
    if custom_verbose == 1:
        # print model backbone details
        print("==================================================================================")
        print("Building sequential model with %d hidden layers:" % len(units[1:-1]))

        # input layer
        print("# Input layer:\t\t%d neurons, activation function %s, dropout %f and input dimension %d" %
              (units[0], layer_act_fn, dropout, input_dimension))

        # hidden layers
        hl_number = 1   # iterator in for loop
        for u in units[1:-1]:
            print("# Hidden layer %d:\t%d neurons, activation function %s, dropout %f" %
                  (hl_number, u, layer_act_fn, dropout))
            hl_number += 1

        # output layer
        print("# Output layer:\t\t%d neurons, activation function %s" %
              (units[-1], output_act_fn))

        # model compiling details
        print("# Optimizer:\t\t%s with learning rate %f" % (optimizer, learning_rate))
        print("# Loss function:\t%s" % (loss_fn))
        print("# Metrics:\t\t\t%s" % (metrics))
        print("==================================================================================")

    if custom_verbose == 2:
        # only print the units of the current model (output in training is nice and small)
        print("creating %s" % units, file=sys.stdout)    # change to stderr if "tee" doesn't print this

    # create model
    model = Sequential()

    # add input layer
    model.add(Dense(units[0], input_dim=input_dimension, kernel_initializer=k_init, bias_initializer=b_init))
    model.add(Activation(layer_act_fn))
    model.add(Dropout(dropout))

    # add hidden layers
    for u in units[1:-1]:
        model.add(Dense(u, kernel_initializer=k_init, bias_initializer=b_init))
        model.add(Activation(layer_act_fn))
        model.add(Dropout(dropout))

    # add output layer
    model.add(Dense(units[-1], kernel_initializer=k_init, bias_initializer=b_init))
    model.add(Activation(output_act_fn))

    # select keras optimizer with learning rate from optimizer input string
    # note: only SGD has momentum, decay and nesterov
    optzd = {"Adam": Adam(lr=learning_rate),
             "Adagrad": Adagrad(lr=learning_rate),
             "RMSprop": RMSprop(lr=learning_rate),
             "SGD": SGD(lr=learning_rate, momentum=momentum, decay=decay, nesterov=nesterov)}
    opt = optzd[optimizer]

    # compile model
    model.compile(optimizer= opt, loss= loss_fn, metrics= metrics)
    return model



################################## actual shit is happening here ###########################################

# load datasets and create train / test examples
filename = "8k"
ds_train, ds_test = load_datasets(filename)                 # create training and test data sets
X_train, y_train = create_features_and_labels(ds_train)     # create training features
X_test, y_test = create_features_and_labels(ds_test)        # create test features

############################
### GRIDSEARCH VARIABLES ###
####################################################################################
### shape, epochs, batchsize stuff ###
units = [[100, 30, 1]]
epochs = [5]
batchsizes = [10]

### neuron stuff ###
activations = ['relu']
dropouts = [0.5]
kernel_initializers = ["random_uniform"]
bias_initializers = ["zeros"]

### optimizer stuff ###
optimizers = ['SGD']
learn_rates = [0.01]
momentums = [2.0]#, 1.0, 0.5]
decays = [1.0, 0.5, 0.2, 0.1]
nesterovs = [False]
####################################################################################


# specify param grid dictionary
# all of the variables specified in the dictionary are used for gridsearch
param_grid = dict(units= units,
                  decay= decays)

# create model
# all additional parameters overwrite model default parameters of build function
model = KerasClassifier(build_fn=build_model, input_dimension=X_train.shape[1], verbose=0)

# create gridsearch classifier
# all specified gridsearch params overwrite default params of build function
# set n_jobs to -1 for maximum parallel computation
clf = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=1, verbose=1, cv=2)

# run gridsearch on model (last 20% of training data used for evaluation)
clf.fit(X_train, y_train, validation_split=0.2, epochs=10, verbose=0)

# print training results
print_results(clf)


# run model with best parameters on test data
score = clf.score(X_test, y_test)
print("testscore: %.3f" % score)

# plot history graph / save history and best parameters in file
params = clf.best_params_
hstry_dct = clf.best_estimator_.model.history.history
plot_hst(hstry_dct)
#write_ph(params, hstry_dct)