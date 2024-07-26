import numpy as np
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF

"""
This script demonstrates higher-dimensional Gaussian Process Regression (GPR) using numpy, matplotlib, and sklearn.
It simulates a robotic system collecting data iteratively and improving predictions based on model uncertainty.
"""

def collect_initial_data():
    
    """
    Generate initial 2D data points and their corresponding target values.
    """
    np.random.seed(42)
    X = np.random.rand(10, 2) * 10  # 10 points in 2D space [0, 10] x [0, 10]
    y = np.sin(X[:, 0]) * np.cos(X[:, 1]) + np.random.normal(0, 0.1, X.shape[0])
    return X, y

def collect_more_data(gp, X_current, threshold=0.1):
    """
    Collect additional data points where model uncertainty is high.
    """
    Y_mean, sigma = gp.predict(X_current, return_std=True)
    high_uncertainty_points = X_current[sigma > threshold]
    if len(high_uncertainty_points) == 0:
        return np.array([]), np.array([])

    new_points = high_uncertainty_points + np.random.uniform(-0.5, 0.5, high_uncertainty_points.shape)
    y_new = np.sin(new_points[:, 0]) * np.cos(new_points[:, 1]) + np.random.normal(0, 0.1, new_points.shape[0])
    return new_points, y_new

def robot_simulation(max_iterations=2, uncertainty_threshold=0.1):
    """
    Run the simulation, update the model iteratively, and visualize predictions and uncertainties.
    """
    X_train, y_train = collect_initial_data()
    kernel = RBF(length_scale=1)
    gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=4, alpha=0.1)

    for iteration in range(max_iterations):
        gp.fit(X_train, y_train)

        x1 = np.linspace(0, 10, 100)
        x2 = np.linspace(0, 10, 100)
        x1x2 = np.meshgrid(x1, x2)
        X_grid = np.vstack([x1x2[0].ravel(), x1x2[1].ravel()]).T

        y_pred, sigma = gp.predict(X_grid, return_std=True)

        plt.figure(figsize=(10, 5))
        plt.contourf(x1, x2, y_pred.reshape(x1x2[0].shape), cmap='magma', alpha=1)
        plt.colorbar(label='Mean prediction')
        plt.scatter(X_train[:, 0], X_train[:, 1], c='red', label='Data points')
        plt.xlabel('X1')
        plt.ylabel('X2')
        plt.title(f'GPR Mean Prediction - Iteration {iteration + 1}')
        plt.legend()
        plt.show()

        plt.figure(figsize=(10, 5))
        plt.contourf(x1, x2, sigma.reshape(x1x2[0].shape), cmap='viridis', alpha=1)
        plt.colorbar(label='Uncertainty (Std Dev)')
        plt.scatter(X_train[:, 0], X_train[:, 1], c='red', label='Data points')
        plt.xlabel('X1')
        plt.ylabel('X2')
        plt.title(f'GPR Uncertainty - Iteration {iteration + 1}')
        plt.legend()
        plt.show()

        X_new, y_new = collect_more_data(gp, X_grid, threshold=uncertainty_threshold)
        if len(X_new) == 0:
            print("No high uncertainty points found. Stopping the iteration.")
            break

        X_train = np.vstack((X_train, X_new))
        y_train = np.hstack((y_train, y_new))

robot_simulation(max_iterations=20, uncertainty_threshold=0.1)
