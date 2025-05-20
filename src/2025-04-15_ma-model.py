# Re-import necessary libraries after environment reset
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import minimize

print('test')

# Simulate an MA(1) process step by step to visualize residual propagation
np.random.seed(1)
n_steps = 20
theta = 0.7
mu = 0.0
eps = np.random.normal(0, 1, n_steps)
x_vals = np.zeros(n_steps)

# Build the MA(1) process one step at a time
x_vals[0] = mu + eps[0]
for t in range(1, n_steps):
    x_vals[t] = mu + eps[t] + theta * eps[t - 1]

# To show the difference, here's an AR(1) process built in the same way:
x_vals_ar = np.zeros(n_steps)
phi = theta
x_vals_ar[0] = mu + eps[0]
for t in range(1, n_steps):
    x_vals_ar[t] = phi * x_vals_ar[t - 1] + eps[t]

# Plotting: showing how each shock (eps) contributes to the next value
plt.figure(figsize=(12, 6))
plt.stem(
    range(n_steps), eps, linefmt="r-", markerfmt="ro", basefmt="k", label="Shock (ε)"
)
plt.plot(x_vals, label="X_t (MA Value)", marker="o", linestyle="-", color="blue")
plt.plot(x_vals_ar, label="X_t (AR Value)", marker="o", linestyle="-", color="green")
plt.title(f"AR(1) and MA(1) Processes \ntheta={theta}; phi={phi}")
plt.xlabel("Time Step")
plt.ylabel("Value / Shock")
plt.legend()
plt.grid(True)
plt.show()


# Manual MA(1) model fitting using numerical optimization (MLE approach)
# Step 1: Simulated MA(1) data (already generated)

# Step 2: Define the negative log-likelihood function for MA(1)
def neg_log_likelihood_ma1(params, x):
    mu, theta, sigma = params
    n = len(x)
    eps = np.zeros(n)
    eps[0] = x[0] - mu
    for t in range(1, n):
        eps[t] = x[t] - mu - theta * eps[t - 1]

    # Log-likelihood under normal assumption
    ll = -0.5 * n * np.log(2 * np.pi * sigma**2) - np.sum(eps**2) / (2 * sigma**2)
    return -ll  # minimize negative log-likelihood


# Step 3: Initial parameter guesses
init_params = [0.0, 0.0, 1.0]  # mu, theta, sigma
bounds = [(-5, 5), (-0.99, 0.99), (1e-3, 5)]  # reasonable bounds

# Step 4: Run the optimizer
result = minimize(neg_log_likelihood_ma1, init_params, args=(x_vals,), bounds=bounds)

# Step 5: Extract fitted parameters
mu_fit, theta_fit, sigma_fit = result.x

# Step 6: Reconstruct residuals using fitted parameters
eps_fitted = np.zeros(n_steps)
eps_fitted[0] = x_vals[0] - mu_fit
for t in range(1, n_steps):
    eps_fitted[t] = x_vals[t] - mu_fit - theta_fit * eps_fitted[t - 1]

# Show results
fit_summary_df = pd.DataFrame(
    {"X_t": x_vals, "True ε_t": eps, "Fitted ε_t": eps_fitted}
)

params_summary = {
    "Estimated μ": mu_fit,
    "Estimated θ": theta_fit,
    "Estimated σ": sigma_fit,
    "True θ": theta,
}

print("done")
