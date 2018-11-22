import sys
from numpy import NaN, Inf, arange, isscalar, asarray, array
import numpy as np

def peakdet(v, delta, x = None):
    maxtab = []
    mintab = []
       
    if x is None:
        x = arange(len(v))
    
    v = asarray(v)
    
    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')
    
    if not isscalar(delta):
        sys.exit('Input argument delta must be a scalar')
    
    if delta <= 0:
        sys.exit('Input argument delta must be positive')
    
    mn, mx = Inf, -Inf
    mnpos, mxpos = NaN, NaN
    
    lookformax = True
    
    for i in arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]
        
        if lookformax:
            if this < mx-delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn+delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return array(maxtab), array(mintab)

if __name__=="__main__":
    from matplotlib.pyplot import plot, scatter, show
    
    series = []
    for read in range(5) :
        with open('C:/Users/H-Com/Desktop/Project A10A_AtLast/Data_read To Recommend/data/data_' + str(read + 1) + '.txt', 'r') as f :
            data = f.read().split(',')
            for int_data in range(len(data)) :
                data[int_data] = int(data[int_data])
            series.append(data)
            
    f.close()

    for iteration in range(len(series)) :
        maxtab, mintab = peakdet(series[iteration],.3)
        
        x_val = list(mintab[:, 1])
        y_val = list(maxtab[:, 1])

        i = 1

        print(len(x_val))
        print(len(y_val))
        print("")
        if len(x_val) != len(y_val) :
            while True :
                if series[iteration][maxtab[0][0] - i] == y_val[0] :
                    i += 1
                else :
                    x_val.insert(0, series[iteration][maxtab[0][0] - i])
                    break

        print(list(x_val))
        print(len(x_val))
        print("")
        print(list(y_val))
        print(len(y_val))
        print("")
        
        with open('peak_' + str(iteration) + '.txt', 'w') as W :
            W.write(str(x_val))
            W.write("\n")
            W.write(str(y_val))
            
        W.close()
        
        plot(series[iteration])
        scatter(array(maxtab)[:,0], array(maxtab)[:,1], color='blue')
        scatter(array(mintab)[:,0], array(mintab)[:,1], color='red')
        show()
