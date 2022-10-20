from math import *
import time
import matplotlib.pyplot as plt

#no external libraries

def linspace(start,end,N):
    a=start
    b=end
    n=N
    q=(b-a)/n
    cont=1
    u=a
    x=[]
    while cont==1:
        x.append(round(u,len(str(N))+1))
        u+=q
        if u>b and q>0:
            cont=0
        if u<b and q<0:
            cont=0
    return x

def rsolve(equation,var,it):
    eq=equation.split("=")
    left=str(eq[0])
    right=str(eq[1])
    right="-1*("+right+")"
    expr=left+right
    expr=expr.replace(var,"x[k]")
    spot=0
    maxx=1000
    for j in range(5):
        x=linspace(spot-maxx/10**j,spot+maxx/10**j,100)
        y=[]
        for k in range(len(x)):
            try:
                y.append(abs(eval(expr)))
            except Exception as z:
                print("error:",z)
                print("this is your broken equation. idiot. --> ",equation)
                z=1
            
        minn=10**200
        for i in range(len(y)):
            if y[i]<minn:
                minn=y[i]
                spot=x[i]
    return x[50]


#y'=y'+y''
#y(0)=0
#y'(0)=3

dd=10**-300


def desolve(equation,variable,order):
    print("Solving:",equation,"\n")
    var=variable
    eqog=equation    
    ylist=[]
    t=float(input("Enter initial time: ")) #initial time value
    ti=t
    tf=float(input("Enter final time: ")) #final time
    t=t+dd #just in case its something like using t=0 for 1/t
    for i in range(order):
        string="Enter "+var+str(i)+" value: "
        use="float(input(string))"
        use=eval(use)
        ylist.append(use) #ylist is [y0,y1,y2], planning to solve for y3
    
    r=2500# 1600 takes my computer ~1 min to solve
    recm=1*(tf-t)/r
    #ask user acuracy or runs
    
    #dt=recm
    #dt=.00002 #for exact
    #dt=.1
    #print("Time step -->",dt)
    #r=(tf-t)/dt
    string="Enter time increment ("+str(round(recm,7))+" is recommended): "
    dt=float(input(string))
    

    graph=[] #graph points later
    tlist=[] #also for graph later

    
    hi=var+str(order)
    eq=equation
    
    #dt=.001
    r=(tf-ti)/dt
    runs=abs(r)
    print("Iterations:",r)
    
    ti=time.time()
    it=0
    #start loop
    for i in range(abs(round(runs))):
        it+=1 #add every iteration

        #printing percents
        if i%200==0:
            print(round(100*i/runs),"percent")

         #first run: 
        if i==0:
            for j in range(order): #replace y0 y1 with ylist values
                eq=eval("eq.replace(\""+var+str(j)+"\",str(ylist[j]))")

              
            
            #find spot of t
            #print(eq)
            #if it's "tan(..." then leave alone
            #else, (ex. ty*5) fixes that to (t)y*5
            for j in range(len(eq)):
                #print(eq[j])
                if eq[j]=="t" and eq[j+1]!="a":
                    eq=eq[:j]+"("+str(t)+")"+eq[j+1:]
                    
            #print(eq)

            #put "(.0076)" in for "dt"
            eq=eq.replace("dt","("+str(dt)+")")

            #solve for y3 or y2 for the first time
            yappend=rsolve(eq,hi,it)#solve for highest order
            
            ylist.append(yappend) #puts y3 at the end of y0,y1,y2

            ylistog=[] #create delayed ylist variable
            for j in range(len(ylist)):
                ylistog.append(ylist[j])#copy and keep for later

            tog=t

            #initial time estimate
            mins=runs/60 * (time.time()-ti)
            print("Initial runtime estimate:",round(mins,3),"minutes")


        #after one run  
        if i>0:
            eqn=eqog
            for j in range(order):
                #print("eqn.replace(\""+var+str(j)+"\",str(ylist[j]))")
                #print(eval("eqn.replace(\""+var+str(j)+"\",str(ylist[j]))"))
                
                #replace og ylist value with updated value
                #eqn.replace("y0",1.4) if 1.4 is calculated y0 value
                eqn=eval("eqn.replace(\""+var+str(j)+"\",str(ylist[j]))")
                #good, eqn updates correctly

            eq=eqn
            
            #find spot of t
            #if it's "tan(..." then leave alone
            #else, replace "t" with 1.2004 or whatever time it is
            for j in range(len(eq)):
                #print(eq[j])
                if eq[j]=="t" and eq[j+1]!="a":
                    eq=eq.replace("t",str(t))

            
            eq=eq.replace("dt",str(dt))
            tog=t
            #print(eq)

            for j in range(len(ylist)): #update delayed ylist
                ylistog[j]=ylist[j]

            #print(eq)
            ylist[len(ylist)-1]=rsolve(eq,hi,it) #solve for highest order
            #print(eq)
            
        
        #integration
        for j in range(order): #v+=a*dt integration
            #print(ylist[order-j-1],ylist[order-j])
            ylist[order-j-1]=ylist[order-j-1]+ylist[order-j]*dt #error, a is not being solved for

        tlist.append(t)
        t=t+dt
        graph.append(ylist[0])
        #print(ylist)

    print("estimate at t =",tf,"-->",graph[len(graph)-1])
    plt.plot(tlist,graph)
    #plt.ylim([-100,100])
    plt.show()
    return graph
    
    
#use t as independent variable
#use y0 for y; y1 for y'; y2 for y''; y3 for y'''
#or use x2, x3, x4, x0
#desolve("equation","dependent variable", highest order d)
#a=desolve("t*atan(y2)=sin(y2)-y2+y1","y",2)
desolve("-((y2)**((sin(y2))**5))/(t**4)=y0","y",2)
#make a order=getorder(equation)
#desolve("y0+y1=-y2","y",2)
