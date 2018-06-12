"""
[CLASS] MachineLearningTest

Date:       Tuesday June 12th, 2018
Author:     Yousef Zoumot

Object responsible for generating test outputs
by multiplying the new data matrix with our
calculated column weights in our Machine Learning
model
"""


class MachineLearningTest(object):

    """
    Sigmoid maps a number between 1 and 0
    Sigmoid function:
                    1
    sigmoid(x)= ----------
                1 + e^(-x)
    """
    def sigmoid(temp_in):
        return np.float64(1 / (1 + np.exp( - temp_in)))

    """
    By multiplying the new inputs with our calculated
    column weights, we generate a column of prediction
    values to determine whether or not an action occured
    """
    def get_predictions(inputs, weights):
        return sigmoid(np.matmul(inputs, weights))
