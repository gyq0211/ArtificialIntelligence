# Artificial Neural Networks

import numpy as np

class Neural_Network(object):
    def __init__(self):
        # Layer Info. There are 4 inputs (sepal length, sepal width, petal
        # length, petal width), 1 ouput (predicted class), and 3 hidden neurons
        # in a single layer.
        self.inputSize = 4
        self.outputSize = 1
        self.hiddenSize = 3
        # Weights
        self.W1 = np.random.randn(self.inputSize, self.hiddenSize)
        self.W2 = np.random.randn(self.hiddenSize, self.outputSize)

    # Feed forward algorithm with Signoids function as the activation function
    def forward(self, train):
        self.z = np.dot(train, self.W1)
        self.z2 = self.sigmoid(self.z)
        self.z3 = np.dot(self.z2, self.W2)
        o = self.sigmoid(self.z3)
        return o

    # Signoid function
    def sigmoid(self, x):
        return 1/(1 + np.exp(-x))

    # Signoid derivitive
    def sigmoid_der(self, x):
        return x * (1-x)

    # Backward propagation using signoid derivitive, squared loss, and delta
    # output sum
    def backward(self, train, act, out):
        self.o_error = act - out
        self.o_delta = self.o_error * self.sigmoid_der(out)

        self.z2_error = self.o_delta.dot(self.W2.T)
        self.z2_delta = self.z2_error * self.sigmoid_der(self.z2)

        self.W1 += train.T.dot(self.z2_delta)
        self.W2 += self.z2.T.dot(self.o_delta)

    def train(self, train, act):
        o = self.forward(train)
        self.backward(train, act, o)

labels = {
        "Iris-setosa": 1,
        "Iris-versicolor": 2,
        "Iris-virginica": 3
}

training_set = []
training_set_l = []
validation_set = []
validation_set_l = []
testing_set = []
testing_set_l = []

def main():
    # Read data from text file into lists
    read_data()
    # Convert list in numpy arrays for calculations
    np_train = np.asarray(training_set, float)
    np_train_l = np.asarray(training_set_l, float)
    np_val = np.asarray(validation_set, float)
    np_val_l = np.asarray(validation_set_l, float)
    np_test = np.asarray(testing_set, float)
    np_test_l = np.asarray(testing_set_l, float)
    # Scale arrays so they work in error correction with sigmoid function
    np_train = np_train/10 # Assume that max is 10 cm flower
    np_train_l = np_train_l/3 # Max label value is 3
    np_val = np_val/10
    np_val_l = np_val_l/3
    np_test = np_test/10
    np_test_l = np_test_l/3

    # Initialize the ANN and its associated functions
    Model = Neural_Network()
    # Run the training for a set number of cycles
    print_stats(np_train, np_train_l, Model, True)
    for epoch in range(10000):
        Model.train(np_train, np_train_l)
    err = print_stats(np_train, np_train_l, Model, False)

    # Model is now fully trained and validation begins
    np_val = Model.forward(np_val)
    if check_val(np_val, np_val_l, err):
        return

    # Model is now validated to be trained correctly and testing begins
    np_test = Model.forward(np_test)
    print_tests(np_test, np_test_l)

    # Option for user inputed data
    man = input("Do you want to manually enter data? [y, n]\n")
    while man == 'y':
        print("Max length or width of a petal or speal is 10cm.\n")
        sep_len = input("Enter sepal length in cm\n")
        sep_wid = input("Enter sepal width in cm\n")
        pet_len = input("Enter petal length in cm\n")
        pet_wid = input("Enter petal width in cm\n")
        user_in = []
        user_in.append(float(sep_len))
        user_in.append(float(sep_wid))
        user_in.append(float(pet_len))
        user_in.append(float(pet_wid))
        np_u = np.asarray([user_in], float)
        np_u = np_u/10
        #print(np_u)
        np_u = Model.forward(np_u)
        #print(np_u)
        flow = classify(np_u[0])
        print("That is an " + flow + ".\n")
        man = input("Do you want to enter another? [y, n]")


# To check the error rate of model to see if it is within desired range
def check_val(predict, actual, train_err):
    correct = 0
    for i in range(len(predict)):
        pre_flow = classify(predict[i])
        act_flow = classify(actual[i])
        if pre_flow == act_flow:
            correct += 1
    percent_corr = round(((correct/30.00) * 100.00), 2)
    err = round((np.mean(np.square(actual - predict))) * 100.00, 2)
    print("----------------Validation Phase----------------")
    print("Accuracy: " + str(percent_corr) + "%\n")
    print("Training has an error rate of " + str(train_err) + "% and validation has error rate of " + str(err) + "%\n")
    if err <= 5.00 and train_err <= 5.00:
        print("This is acceptable error rates (<= 5%). Continuing to testing\n")
        return False
    else:
        print("One error rate exceeded threshold (> 5%). Terminating. Please run again to retrain data.\n")
        return True

# Given the results of model testing it will classify and output the accuracy
def print_tests(predict, actual):
    print("-----------------Testing Phase------------------")
    print("Testing ANN on unseen data\n")
    print(str(len(predict)) + " total tests run\n")
    correct = 0
    for i in range(len(predict)):
        pre_flow = classify(predict[i])
        act_flow = classify(actual[i])
        if pre_flow == act_flow:
            correct += 1
        print("Test " + str(i+1) + " ---> Predicted: " + pre_flow + ", Actual: " + act_flow + "\n")
    percent_corr = round(((correct/30.00) * 100.00), 2)
    print("Accuracy: " + str(percent_corr) + "%\n")
    
# Based off output from learned model it returns what the predicted flower is
def classify(num):
    if num < 0.505:
        return "Iris Setosa"
    if num >= 0.505 and num < 0.835:
        return "Iris Versicolor"
    if num > 0.835:
        return "Iris Virginica"

# Used before and after learning to show the change in predictions and errors
def print_stats(unlab, lab, Mod, before):
    if before:
        print("----------------Before Learning-----------------")
        print("Input: \n" + str(unlab))
        print("Actual Output: \n" + str(lab))
    else:
        print("----------------After Learning------------------")
    print("Predicted Output: \n" + str(Mod.forward(unlab)))
    err = round((np.mean(np.square(lab - Mod.forward(unlab)))) * 100.00, 2)
    print("Error: \n" + str(err))
    print("------------------------------------------------\n")
    return err

# Given a line from the text file and what set it belong to it splits it up
# and adds it to the right list
def add_data(sets, line):
    dats = line.split(',')
    dats[-1] = dats[-1].strip()
    data = dats[:4]
    label = dats[-1]
    if sets == 'tr':
        training_set.append(data)
        training_set_l.append([labels[label]])
    elif sets == 'va':
        validation_set.append(data)
        validation_set_l.append([labels[label]])
    elif sets == 'te':
        testing_set.append(data)
        testing_set_l.append([labels[label]])

# Reads the data from text file. Allocates 30 for testing, 10 for validation,
# and 10 for testing from each flower so total breakdown is 90:30:30.
def read_data():
    file = open("irisData.txt", "r")
    for count, line in enumerate(file):
        ct = int(count)
        if (ct <= 29) or (ct >= 50 and ct < 80) or (ct >= 100 and ct < 130):
            add_data('tr', line)
        elif (ct >= 30 and ct < 40) or (ct >= 80 and ct < 90) or (ct >= 130 and ct < 140):
            add_data('va', line)
        elif (ct >= 40 and ct < 50) or (ct >= 90 and ct < 100) or (ct >= 140 and ct < 150):
            add_data('te', line)
    file.close()


main()
