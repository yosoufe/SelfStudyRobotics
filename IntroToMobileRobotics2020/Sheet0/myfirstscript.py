import numpy as np
import matplotlib.pyplot as plt

# exercise 2

def f(x):
    return np.cos(x) * np.exp(x)

x = np.linspace(-2*np.pi,2*np.pi, 100)
plt.figure()
plt.plot(x, f(x))
plt.savefig("graph.png")

# exercise 3
# np.random.seed(1)
normal_random = np.random.normal(loc = 5.0, scale = 2.0, size = 100000)
print(normal_random)

uniform_random = np.random.uniform(0.0, 10.0, size = 100000)
print(uniform_random)

print("mean and std of normal_random: {}, {}".format(np.mean(normal_random), np.std(normal_random)))
print("mean and std of uniform_random: {}, {}".format(np.mean(uniform_random), np.std(uniform_random)))

plt.figure()
plt.hist(normal_random, bins=100)

plt.figure()
plt.hist(uniform_random, bins=100)
plt.show()