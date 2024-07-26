import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.gaussian_process.kernels import RBF
from sklearn.gaussian_process import GaussianProcessRegressor

'''''
- A simple simulation to demonstrate Gaussian Process Regression (GPR) using synthetic data.
- The kernel used is Radial Basis Function (RBF). This example includes:
- Generation of synthetic data points with noise
- Fitting a Gaussian Process model to the data
- Making predictions over a range of values
- Visualizing the original data, predictions, and confidence intervals
 
 '''

# Seed the random number generator for reproducibility
np.random.seed(42)

# Generate 100 random data points between 0 and 10
X = np.random.rand(100, 1) * 10
# Define the true function as sine of X and add noise to the observations
y = np.sin(X).ravel()
y += 0.2 * (0.5 - np.random.rand(100))  # Adding noise to the data

# Define the kernel as Radial Basis Function (RBF)
kernel = RBF(length_scale=1.0)
# Initialize the Gaussian Process Regressor with the RBF kernel and 10 restarts for optimizer
gpr = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10)

# Fit the Gaussian Process model to the synthetic data
gpr.fit(X, y)

# Generate predictions over a range of input values from 0 to 10
X_ = np.linspace(0, 10, 1000).reshape(-1, 1)
# Obtain the mean and standard deviation of the predictions
y_mean, y_std = gpr.predict(X_, return_std=True)

# Plot the results
plt.figure(figsize=(10, 5))
# Plot the original noisy observations
plt.plot(X, y, 'r.', markersize=10, label='Observations')
# Plot the predicted mean
plt.plot(X_, y_mean, 'b-', label='Prediction')
# Plot the confidence interval (mean ± standard deviation)
plt.fill_between(X_[:, 0], y_mean - y_std, y_mean + y_std, alpha=0.2, color='k')
plt.title("Gaussian Process Regression")
plt.xlabel("Input")
plt.ylabel("Output")
plt.legend()
plt.show()
