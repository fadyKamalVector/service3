from numpy import random
from scipy import stats
from sklearn.metrics import r2_score

import numpy
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#import matplotlib

"""

speed = [99,86,87,88,111,86,103,87,94,78,77,85,86]
speed2 = [99,86,87,88,86,103,87,94,78,77,85,86]
speed3 = [86,87,88,86,87,85,86]
speed4 = [32,111,138,28,59,77,97]
ages = [5,31,43,48,50,41,7,11,15,39,80,82,32,2,8,6,25,36,27,61,31]


x = numpy.mean(speed)
print(x)

# its arranges the numbers then takes the median number
x2 = numpy.median(speed)
print(x2)

# If there are two numbers in the middle, divide the sum of those numbers by two
x3 = numpy.median(speed2)
print(x3)

x4 = stats.mode(speed)
print(x4)

# Standard Deviation
x5a = numpy.var(speed3)
print(x5a) #variance
x5 = numpy.std(speed3)
print(x5)

x6a = numpy.var(speed4)
print(x6a) #variance
x6 = numpy.std(speed4)
print(x6)

# Percentiles
sorted_ages = sorted(ages)
print(sorted_ages)
x7 = numpy.percentile(ages, 75)
print(x7)

"""

"""
RandomData = numpy.random.uniform(0.0, 5.0, 250)
#print('RandomData', RandomData)

plt.figure(figsize=(10,4))

plt.subplot(2, 2, 1)
plt.scatter(range(len(RandomData)), RandomData)

plt.subplot(2, 2, 2)
counts, bin_edges = numpy.histogram(RandomData)
print("Y = counts:", counts)
print("X = bin edges:", bin_edges)
plt.hist(RandomData)

plt.subplot(2, 2, 3)
plt.plot(RandomData)

plt.show()

"""

"""
x = numpy.random.normal(5.0, 1.0, 100000)
print('x', x)
plt.hist(x, 100)
plt.show()
"""

"""
#sns.displot(random.normal(loc=1, scale=100, size=1000), kind="kde")
sns.displot(random.normal(1, 100, 1000), kind="kde")

plt.show()

"""

"""

x = numpy.random.normal(5.0, 1.0, 1000)
y = numpy.random.normal(10.0, 2.0, 1000)

plt.scatter(x, y)
plt.show()

"""

'''

x = [5,7,8,7,2,17,2,9,4,11,12,9,6]
y = [99,86,87,88,111,86,103,87,94,78,77,85,86]

slope, intercept, r, p, std_err = stats.linregress(x, y)

"""

1) slope

ميل الخطّ المستقيم (m)

يمثل:
كم تزيد y لو زادت x بمقدار 1.

معادلة الخط:

𝑦
=
𝑚
𝑥
+
𝑏
y=mx+b
2) intercept

المقطوع (b)

هي قيمة y لما تكون x = 0.

3) r

معامل الارتباط (Correlation Coefficient)

مداه من:

+1 ارتباط موجب كامل

-1 ارتباط سالب كامل

0 مفيش ارتباط

كل ما يقرب من ±1 → العلاقة أقوى.

4) p

p-value لاختبار الفرضية

تقيس:

هل الميل فعلاً له معنى إحصائي؟
لو p صغيرة جدًا → الميل مهم.

5) std_err

الخطأ المعياري للميل

يقيس دقة تقدير الميل.
كلما قلّ → تقدير الميل أدق.

"""

#print(stats.linregress(x, y))
print(r)

def myfunc(x):
  return slope * x + intercept

speed = myfunc(10)
print(speed)

mymodel = list(map(myfunc, x))

plt.scatter(x, y)
plt.plot(x, mymodel)
plt.show()

'''

"""

x = [89,43,36,36,95,10,66,34,38,20,26,29,48,64,6,5,36,66,72,40]
y = [21,46,3,35,67,95,53,72,58,10,26,34,90,33,38,20,56,2,47,15]

slope, intercept, r, p, std_err = stats.linregress(x, y)

print(r)

def myfunc(x):
  return slope * x + intercept

mymodel = list(map(myfunc, x))

plt.scatter(x, y)
plt.plot(x, mymodel)
plt.show()

"""

"""

x = [1,2,3,5,6,7,8,9,10,12,13,14,15,16,18,19,21,22]
y = [100,90,80,60,60,55,60,65,70,70,75,76,78,79,90,99,99,100]

mymodel = np.poly1d(np.polyfit(x, y, 3))

myline = np.linspace(1, 22, 100)
print(myline)

plt.scatter(x, y)
plt.plot(myline, mymodel(myline))
plt.show()

"""

"""

x = [1,2,3,5,6,7,8,9,10,12,13,14,15,16,18,19,21,22]
y = [100,90,80,60,60,55,60,65,70,70,75,76,78,79,90,99,99,100]

mymodel = numpy.poly1d(numpy.polyfit(x, y, 3))

print(r2_score(y, mymodel(x)))

"""

"""
x = [1,2,3,5,6,7,8,9,10,12,13,14,15,16,18,19,21,22]
y = [100,90,80,60,60,55,60,65,70,70,75,76,78,79,90,99,99,100]

mymodel = numpy.poly1d(numpy.polyfit(x, y, 3))

speed = mymodel(17)
print(speed)

"""

x = [89,43,36,36,95,10,66,34,38,20,26,29,48,64,6,5,36,66,72,40]
y = [21,46,3,35,67,95,53,72,58,10,26,34,90,33,38,20,56,2,47,15]

mymodel = numpy.poly1d(numpy.polyfit(x, y, 3))

print(r2_score(y, mymodel(x)))

myline = numpy.linspace(2, 95, 100)

plt.scatter(x, y)
plt.plot(myline, mymodel(myline))
plt.show()