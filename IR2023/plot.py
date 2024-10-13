import matplotlib.pyplot as plt


plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 17
plt.rcParams["lines.linewidth"] = 1
plt.plot([0, 0.36, 0.71, 1, 1], [1, 1, 1, 0.93, 0.7], marker='o', color='blue')
plt.xlabel("Recall")
plt.ylabel("Precision")

plt.show()