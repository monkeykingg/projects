'''
Michael Dimmick
hw3
Q1
CSC2515
'''

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_boston

# helper function for plotting
def compute_squared_error_loss(y,t):
	return np.power(0.5*(y-t),2)

# compute the huber loss for a given a and delta
def compute_huber_loss(a, delta):

	huber_loss = np.copy(a)

	# y_idx_1: y indexes for |a| <= delta
	# y_idx_2: y indexes for |a| > delta
	y_idx_1 = np.where(np.absolute(a) <= delta)
	y_idx_2 = np.where(np.absolute(a) > delta)

	huber_loss[y_idx_1] = 0.5*np.power((a)[y_idx_1],2)
	huber_loss[y_idx_2] = delta*(np.absolute((a)[y_idx_2])-0.5*delta)

	return huber_loss

# compute the gradient of the huber loss function for a given a and delta
def compute_huber_gradient(a, delta):
	huber_loss_gradient = np.copy(a)

	# y_idx_1: y indexes for |a| <= delta
	# y_idx_2: y indexes for |a| > delta
	y_idx_1 = np.where(np.absolute(a) <= delta)
	y_idx_2 = np.where(np.absolute(a) > delta)

	huber_loss_gradient[y_idx_1] = a[y_idx_1]
	huber_loss_gradient[y_idx_2] = delta*a[y_idx_2]/np.absolute(a[y_idx_2])

	return huber_loss_gradient

# plot squared error for Q1a)
def plot_squared_error_loss():
	plot_points = 100
	y = np.linspace(-10,10,plot_points,endpoint=True)
	squared_error_loss = compute_squared_error_loss(y,0)
	plt.plot(y,squared_error_loss)
	plt.ylabel('squared error loss')
	plt.xlabel('y')
	plt.title('Squared Error Loss, t = 0')
	plt.show()

# plot huber loss for Q1a)
def plot_huber_loss():
	plot_points = 100
	delta_values = [2,4,8]
	for delta_value in delta_values:
		y = np.linspace(-10,10,plot_points,endpoint=False)
		huber_loss = compute_huber_loss(y-np.zeros(len(y)),delta_value)
		plt.plot(y,huber_loss,label='delta = {}'.format(delta_value))
		plt.legend(loc='best')
		plt.ylabel('huber loss')
		plt.xlabel('y')
		plt.title('Huber Loss, t = 0')
	plt.axvline(x=2, color = 'blue')
	plt.axvline(x=4, color = 'orange')
	plt.axvline(x=8, color = 'green')
	plt.show()

# gradient descent implementation for linear model
def huber_gradient_descent(data, labels, epochs, learning_rate, delta):
	w = np.zeros(len(data[0]))
	b = 0
	N = data.shape[0]
	cost_history = np.zeros(epochs)

	for iteration in range(0,epochs):
		# current estimates
		y = np.dot(data, w) + b

		# compute gradients
		huber_loss_gradient = compute_huber_gradient(y - labels, delta)
		dJ_dw = (1/N)*np.dot(np.transpose(data), huber_loss_gradient)
		dJ_db = (1/N)*np.sum(huber_loss_gradient)

		# update parameters
		w -= learning_rate*dJ_dw
		b -= learning_rate*dJ_db

		# record cost function
		L = compute_huber_loss(y - labels, delta)
		J = (1/N)*np.sum(L)
		cost_history[iteration] = J

	# plot cost vs epochs
	plt.plot(cost_history)
	plt.ylabel('huber loss')
	plt.xlabel('epoch')
	plt.title('Huber Loss vs Epochs, alpha = {}, delta = {}'.format(learning_rate, delta))
	plt.show()

def main():

	#  part a) plots
	plot_squared_error_loss()
	plot_huber_loss()

	# load dataset
	boston = load_boston()
	data = boston.data
	labels = boston.target

	# learning parameters
	epochs = 60
	learning_rate = 0.00001
	delta = 2

	huber_gradient_descent(data, labels, epochs, learning_rate, delta)

if __name__ == "__main__":
    main()
