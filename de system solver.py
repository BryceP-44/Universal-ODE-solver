from math import *
import matplotlib.pyplot as plt

# x' = y
# y' = -sin(x) - y

t=0 #initial time
y=0 #initial y
#x=2*pi+.1 #initial x
x=pi+.1
tf=10 #final time

graph=[] #y list
rang=10000 #total number of points
dt=(tf-t)/rang #time increment
tl=[] #t list
dd=10**-200
t+=dd
xl=[] #x list

#(-log(cos(t)+dd)/log(yp+dd))
for i in range(rang):
    yp=-sin(x)-y #y'
    y+=yp*dt #integrate y'
    xp=y #x'
    x+=xp*dt #int x'
    t=t+dt #increment time
    xl.append(x)
    tl.append(t) 
    graph.append(y) 

print("estimate at t =",round(t,3),"is:",graph[len(graph)-1])

plt.plot(xl,graph)
plt.show()
