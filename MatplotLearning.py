import matplotlib.pyplot as plt
import numpy as np

"""
xpoints = np.array([1, 8])
ypoints = np.array([3, 10])

plt.plot(xpoints, ypoints)
#plt.plot(xpoints, ypoints, 'o')
plt.show()
"""

"""
xpoints = np.array([1, 2, 6, 8])
ypoints = np.array([3, 8, 1, 10])

plt.plot(xpoints, ypoints)
plt.show()
"""

#ypoints = np.array([3, 8, 1, 10, 5, 7])

#plt.plot(ypoints, marker = 'o')
#plt.plot(ypoints, marker = '*')
#plt.plot(ypoints, 'o:r')
#plt.plot(ypoints, 'o-.')
#plt.plot(ypoints, 'om-.')
#plt.plot(ypoints, marker = 'o', ms = 20)
#plt.plot(ypoints, marker = 'o', ms = 20, mec = 'r')
#plt.plot(ypoints, marker = 'o', ms = 20, mfc = 'r')
"""
plt.plot(ypoints, 
         color = 'blue', 
         marker = 'o', 
         ms = 20, 
         linewidth = '8',
         linestyle = 'dashed', 
         mec = 'black', mfc = 'green'
         )
"""
#plt.plot(ypoints, ls = ':')
#plt.plot(ypoints, c = '#4CAF50')

#plt.show()

"""
y1 = np.array([3, 8, 1, 10])
y2 = np.array([6, 2, 7, 11])

plt.plot(y1)
plt.plot(y2)

plt.show()

"""

"""
x1 = np.array([0, 1, 2, 3])
y1 = np.array([3, 8, 1, 10])
x2 = np.array([0, 1, 2, 3])
y2 = np.array([6, 2, 7, 11])

plt.plot(x1, y1, x2, y2)
plt.show()

"""

"""
x = np.array([80, 85, 90, 95, 100, 105, 110, 115, 120, 125])
y = np.array([240, 250, 260, 270, 280, 290, 300, 310, 320, 330])

plt.plot(x, y)

plt.title("Sports Watch Data")
plt.xlabel("Average Pulse")
plt.ylabel("Calorie Burnage")

plt.show()

"""

"""
x = np.array([80, 85, 90, 95, 100, 105, 110, 115, 120, 125])
y = np.array([240, 250, 260, 270, 280, 290, 300, 310, 320, 330])

font1 = {'family':'serif','color':'blue','size':20}
font2 = {'family':'serif','color':'darkred','size':15}

plt.title("Sports Watch Data", fontdict = font1, loc = 'left')
plt.xlabel("Average Pulse", fontdict = font2)
plt.ylabel("Calorie Burnage", fontdict = font2)

plt.plot(x, y)
plt.grid()

plt.show()

"""

"""
x = np.array([80, 85, 90, 95, 100, 105, 110, 115, 120, 125])
y = np.array([240, 250, 260, 270, 280, 290, 300, 310, 320, 330])

plt.title("Sports Watch Data")
plt.xlabel("Average Pulse")
plt.ylabel("Calorie Burnage")

plt.plot(x, y)
#plt.grid(axis = 'x')
#plt.grid(axis = 'y')
plt.grid(color = 'green', linestyle = '--', linewidth = 0.5)

plt.show()

"""

"""
#plot 1:
x = np.array([0, 1, 2, 3])
y = np.array([3, 8, 1, 10])

plt.subplot(1, 2, 1)
plt.plot(x,y)

#plot 2:
x = np.array([0, 1, 2, 3])
y = np.array([10, 20, 30, 40])

plt.subplot(1, 2, 2)
plt.plot(x,y)

plt.show()

"""

"""
#plot 1:
x = np.array([0, 1, 2, 3])
y = np.array([3, 8, 1, 10])

plt.subplot(2, 1, 1)
plt.plot(x,y)

#plot 2:
x = np.array([0, 1, 2, 3])
y = np.array([10, 20, 30, 40])

plt.subplot(2, 1, 2)
plt.plot(x,y)

plt.show()

"""

"""
#plot 1:
x = np.array([0, 1, 2, 3])
y = np.array([3, 8, 1, 10])
plt.subplot(2, 2, 1)
plt.plot(x,y)

#plot 2:
x = np.array([0, 1, 2, 3])
y = np.array([10, 20, 30, 40])
plt.subplot(2, 2, 2)
plt.plot(x,y)

#plot 3:
x = np.array([0, 1, 2, 3])
y = np.array([10, 50, 15, 30])
plt.subplot(2, 2, 3)
plt.plot(x,y)

#plot 4:
x = np.array([0, 1, 2, 3])
y = np.array([5, 8, 4, 1])
plt.subplot(2, 2, 4)
plt.plot(x,y)

plt.show()

"""

"""
x = np.array([0, 1, 2, 3])
y = np.array([3, 8, 1, 10])
plt.subplot(2, 3, 1)
plt.plot(x,y)
plt.title("SALES")

x = np.array([0, 1, 2, 3])
y = np.array([10, 20, 30, 40])
plt.subplot(2, 3, 2)
plt.plot(x,y)
plt.title("INCOME")

x = np.array([0, 1, 2, 3])
y = np.array([3, 8, 1, 10])
plt.subplot(2, 3, 3)
plt.plot(x,y)

x = np.array([0, 1, 2, 3])
y = np.array([10, 20, 30, 40])
plt.subplot(2, 3, 4)
plt.plot(x,y)

x = np.array([0, 1, 2, 3])
y = np.array([3, 8, 1, 10])
plt.subplot(2, 3, 5)
plt.plot(x,y)

x = np.array([0, 1, 2, 3])
y = np.array([10, 20, 30, 40])
plt.subplot(2, 3, 6)
plt.plot(x,y)

plt.suptitle("MY SHOP")
plt.show()

"""

"""
x = np.array([5,7,8,7,2,17,2,9,4,11,12,9,6])
y = np.array([99,86,87,88,111,86,103,87,94,78,77,85,86])

plt.scatter(x, y)
plt.show()

"""

"""
#day one, the age and speed of 13 cars:
x = np.array([5,7,8,7,2,17,2,9,4,11,12,9,6])
y = np.array([99,86,87,88,111,86,103,87,94,78,77,85,86])
plt.scatter(x, y, color = 'blue')

#day two, the age and speed of 15 cars:
x = np.array([2,2,8,1,15,8,12,9,7,3,11,4,7,14,12])
y = np.array([100,105,84,105,90,99,90,95,94,100,79,112,91,80,85])
plt.scatter(x, y, color = "#2f9c4c")

plt.show()

"""

"""
x = np.array([5,7,8,7,2,17,2,9,4,11,12,9,6])
y = np.array([99,86,87,88,111,86,103,87,94,78,77,85,86])
#colors = np.array(["red","green","blue","yellow","pink","black","orange","purple","beige","brown","gray","cyan","magenta"])
colors = np.array([0, 10, 20, 30, 40, 45, 50, 55, 60, 70, 80, 90, 100])
sizes = np.array([20,50,100,200,500,1000,60,90,10,300,600,800,75])

plt.scatter(x, y, c=colors, cmap='viridis', s=sizes, alpha=0.5)
plt.colorbar()

plt.show()

"""

"""
x = np.random.randint(100, size=(100))
y = np.random.randint(100, size=(100))
colors = np.random.randint(100, size=(100))
sizes = 10 * np.random.randint(100, size=(100))

plt.scatter(x, y, c=colors, s=sizes, alpha=0.5, cmap='nipy_spectral')

plt.colorbar()

plt.show()

"""

"""
x = np.array(["A", "B", "C", "D"])
y = np.array([3, 8, 1, 10])

plt.bar(x, y, width = 0.1, color = "red")
#plt.barh(x, y)

plt.show()

"""

x = np.random.normal(170, 10, 250)
y = np.array([35, 25, 25, 15])
mylabels = ["Apples", "Bananas", "Cherries", "Dates"]
myexplode = [0.2, 0, 0, 0]
mycolors = ["Red", "Green", "b", "#C5C741"]


plt.figure(figsize=(10,4))

# Subplot 1: Histogram
plt.subplot(1, 2, 1)
plt.hist(x)
plt.title("Histogram")

# Subplot 2: Pie chart
plt.subplot(1, 2, 2)
plt.pie(y, 
        labels = mylabels, 
        startangle = 90,
        explode = myexplode,
        shadow = True,
        colors = mycolors
        )
plt.title("Pie Chart")
plt.legend(title = "Four Fruits:")

plt.show()