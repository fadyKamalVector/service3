
# this code for learn 

import numpy as np
import matplotlib.pyplot as plt

"""
if 5 > 2:
   print("Five is greater than two!")
"""

"""
This is a comment
written in
more than just one line
"""

"""
x = 5 
y = "hello world"
z = 2

print("result = " , x - z)
print("y is " , y)


for i in range(2, 30, 3):
  print("i = ",i)
  
"""

"""
for x in range(6):
  print(x)
else:
  print("Finally finished!")
  
"""  

"""
for x in range(6):
  if x == 3: 
      break
  print(x)
else:
  print("Finally finished!")
  
"""

"""
adj = ["red", "big", "tasty"]
fruits = ["apple", "banana", "cherry"]

for x in adj:
  for y in fruits:
    print(x, y)
    
"""

"""
for i in [0, 1, 2]:
  pass

"""

"""
x = lambda a : a + 10
print(x(2))

print("Hello, World!")
"""

"""
if 5 > 1:
    print("Eman mtl3a 3naia")
    print("Eman gnenetne")
   
"""
   
"""
    This is a code im 
    gonna say somthing again to reham.    
"""
"""
x = 5 # int
y = "ante reham walla eman mtt3bnash b2a" # str

print(x)
print(y)

"""
"""
x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0

print(x)
print(y)
print(z)
"""


"""
a = 3
b = "Eman"

print("a ", type(a))
print("b ", type(b))

"""

"""
a = 4

A = "Eman"
print(a)

"""

"""
customerName = "reham" # camal
# CustomerName = "Eman" # upper case
customer_name = "Fady" # DataBase

print(customerName)

"""

"""
x, y, z = "Orange", "Banana", "Cherry"

print(x)
print(y)
print(z)
"""

"""
x = y = z = "Orange"
print(x)
print(y)
print(z)
"""

"""
fruits = ["apple", "banana", "cherry"] #array list
print(fruits)
x, y, z = fruits
print(x)
print(y)
print(z)

"""

"""
x = "Reham"
y = "mtl3a"
z = "3naia"
print(x, y, z)
print(x + y + z)
"""

"""
x = 5
y = 10
print(x + y)
"""

"""
x = 5
y = "John"

print(x , y)
#print(x + y) unsupported operand type(s) for +: 'int' and 'str'

#https://www.w3schools.com/python/python_variables_global.asp

"""

"""
x = "eman"
y = "reham"

def func1():
  v0 = "htshl"
  v1 = "ya nas"  
  print("men mtl3 3ene : " + v0)
  print("men mgnene : " + v1)

# func1(x, y)
func1()

# https://www.w3schools.com/python/python_variables_global.asp

x = lambda a : a + 10
print(x(5))

"""
"""
x = "awesome"
y = ""
c = 0


def myfunc():
  x = "fantastic"
  print("Python is " + x)

def myfunc1():
  
  print("y is " + x)

def myfunc2():
  
  print("c is " + c)

def myfunc3():
  global a
  a = "rkze"

myfunc1()
myfunc()
myfunc3()

print("ya Iman " + a)
"""

'''
a= 5
a= 6

x = "awesome"

def myfunc():
  global x 
  x = "fantastic"
  
myfunc()
print("Python is " + x)
print (a)  
'''

"""
#arr = np.array([1, 2, 3, 4, 5])
arr = np.array((1, 2, 3, 4, 5))
print(arr)
print(np.__version__)  
print(type(arr))
"""

"""
a = np.array(12)
b = np.array([1, 2, 3, 4, 5])
c = np.array([[1, 2, 3], [4, 5, 6]])
d = np.array([[[1, 2, 3], [4, 5, 6]], [[1, 2, 3], [4, 5, 6]]])

print(a.ndim)
print(b.ndim)
print(c.ndim)
print(d.ndim)

arr = np.array([1, 2, 3, 4], ndmin=5)

print(arr)
print('number of dimensions :', arr.ndim)

"""

"""
def square(x):
    return x**2

nums = [1,2,3]
result = map(square, nums)  # ده Map object
print(result)  # <map object at 0x...>

nums_squared = list(result)
print(nums_squared) 

"""

"""

# Sample data
x = np.array([0, 1, 2, 3, 4, 5])
y = np.array([0, 0.8, 0.9, 0.1, -0.8, -1])

# Fit a 2nd-degree polynomial
coefficients = np.polyfit(x, y, 2)
print(f"Polynomial coefficients: {coefficients}")

# Create a polynomial function from the coefficients
p = np.poly1d(coefficients)

# Generate points for plotting the fitted curve
x_fit = np.linspace(min(x), max(x), 100)
y_fit = p(x_fit)

# Plot the original data and the fitted curve
plt.scatter(x, y, label='Original Data')
plt.plot(x_fit, y_fit, color='red', label='Fitted Polynomial')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Polynomial Fit with numpy.polyfit')
plt.legend()
plt.grid(True)
plt.show()

"""

"""
# Create a polynomial from coefficients
p = np.poly1d([2, -3, 1]) # Represents x^2 - 3x + 2

print("P === ", p)
print("p(4):", p(4))

"""

"""
# Evaluate the polynomial at x=4
print("p(4):", p(4))

# Get the roots of the polynomial
print("Roots of p:", p.roots)

# Get the derivative of p
p_prime = p.deriv()
print("Derivative of p:", p_prime)

# Integrate p
p_integral = p.integ()
print("Integral of p:", p_integral)

"""

# x = 41451415j
x = "KF480160"

#display x:
print(x)

#display the data type of x:
print(type(x)) 

