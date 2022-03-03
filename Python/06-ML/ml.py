
import numpy as np
import matplotlib.pyplot as plt


result1 = np.random.uniform(0.0, 100.0, 100)

result1 = np.random.normal(5.0, 1.0, 1000)
result2 = np.random.normal(5.0, 1.0, 1000)


# plt.hist(result1, 100)
plt.scatter(result1, result2)
plt.show()
