import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.gaussian_process.kernels import RBF
from sklearn.gaussian_process import GaussianProcessRegressor

"""
This script aims to simulate a robotic system that collects data points iteratively,
using Gaussian Process Regression (GPR) to make predictions and improve its model
based on uncertainty estimates. The robot collects initial data, fits a GPR model,
and iteratively gathers more data in regions of high uncertainty.
"""

def collect_initial_data():
    """
    Collect initial set of data points.
    :return: Tuple containing initial x and y data points.
    """
    x_init = np.random.uniform(0, 10, 5).reshape(-1, 1)
    y_init = np.sin(x_init).ravel() + np.random.normal(0, 0.1, x_init.shape[0])
    return x_init, y_init

def collect_more_data(gp, x_current, threshold=0.1):
    """
    Collect more data points based on high uncertainty regions.
    :param gp: Trained Gaussian Process model.
    :param x_current: Current set of x data points.
    :param threshold: Uncertainty threshold to determine high uncertainty regions.
    :return: Tuple containing new x and y data points.
    """
    y_mean, sigma = gp.predict(x_current, return_std=True)
    high_uncertainty_points = x_current[sigma > threshold]

    # Return new x data points around high uncertainty regions
    new_points = high_uncertainty_points + np.random.uniform(-0.5, 0.5, high_uncertainty_points.shape)
    y_new = np.sin(new_points).ravel() + np.random.normal(0, 0.1, new_points.shape[0])
    return new_points, y_new

def robot_simulation(max_iterations=20, uncertainty_threshold=0.1):
    """
    Simulate the robot's data collection process.
    :param max_iterations: Maximum number of iterations for the simulation.
    :param uncertainty_threshold: Threshold for determining high uncertainty regions.
    """
    x_train, y_train = collect_initial_data()

    # Define the RBF kernel for Gaussian Process
    kernel = RBF(length_scale=1)

    # Create a Gaussian Process Regressor with the specified kernel
    gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10)

    # Iterate to collect more data based on model predictions
    for iteration in range(max_iterations):
        gp.fit(x_train, y_train)

        # Generate test points for predictions
        x_test = np.linspace(0, 10, 100).reshape(-1, 1)

        # Make predictions with the Gaussian Process model
        y_mean, sigma = gp.predict(x_test, return_std=True)

        # Plot the results
        plt.figure(figsize=(10, 6))
        plt.plot(x_train, y_train, 'r.', markersize=10, label='Training data')
        plt.plot(x_test, y_mean, 'b-', label='Prediction')
        plt.fill_between(x_test.ravel(), y_mean - 1.96 * sigma, y_mean + 1.96 * sigma,
                         alpha=0.2, color='k', label='95% confidence interval')
        plt.title(f'Gaussian Process Regression - Iteration {iteration + 1}')
        plt.xlabel("Input (x)")
        plt.ylabel("Predicted Output (y)")
        plt.legend()
        plt.show()

        # Collect more data based on uncertainty
        x_new, y_new = collect_more_data(gp, x_test, threshold=uncertainty_threshold)
        if len(x_new) == 0:
            print("No high uncertainty points found. Stopping the iteration.")
            break
        x_train = np.vstack((x_train, x_new))
        y_train = np.hstack((y_train, y_new))

# Run the robot simulation with specified parameters
robot_simulation(max_iterations=20, uncertainty_threshold=0.1)
