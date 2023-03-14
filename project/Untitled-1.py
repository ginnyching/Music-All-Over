import matplotlib.pyplot as plt
fig = plt.figure()

ax1 = fig.add_axes([0, 0, .5, .5], aspect=1)
ax1.pie(category1.values(), labels=category1.keys(), autopct='%1.1f%%',shadow=False, startangle=90)

ax2 = fig.add_axes([.5, .0, .5, .5], aspect=1)
ax2.pie(category2.values(), labels=category2.keys(), autopct='%1.1f%%',shadow=False, startangle=90)
ax1.set_title('Title for ax1')
ax2.set_title('Title for ax2')
plt.show()