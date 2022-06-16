# IO.py is intended to read input control message
# and control the result output

import json
import numpy as np

def loadjson():
    try:
        file = '../input.json'
        f = open(file,'r')
        content = f.read()
        data = json.loads(content)
        f.close()
        return data
    except:
        print('Please examine the input.json.')

def varTips(startT,endT,freq,keywords,dt,NoP):
    print('\n* Control Message ')
    print('Sample Variable: {}'.format(keywords))
    print('Sample Points Number: {}'.format(NoP))
    print('Start Physical Time: {:.6f} s'.format(startT*dt))
    print('End Physical Time: {:.6f} s'.format(endT*dt))
    print('Compute Time Step: {:} s'.format(dt))
    print('Sample Frequency: {} s-1'.format(freq))
    print('Timestep Files Number: {}'.format(int((endT-startT)/freq+1)))

def timeList(startT,endT,freq,dt):
    T = []
    NoT = int((endT-startT)/freq +1)
    for i in range(NoT):
        t = i*freq*dt
        T.append(t)
    T = np.array(T)
    return T,NoT

def readinput():
    data = loadjson()
    startT = data['startT']
    endT = data['endT']
    freq = data['freq']
    dt = data['dt']
    srcDir = data['srcDir']
    keywords = data['keywords']
    pointsList = data['pointsList']
    outputdir = data['outputdir']
    tol = data['tolerance']
    L = data['Length']
    rho = data['density']

    pointsList = np.array(pointsList)
    NoP,_ = np.shape(pointsList)
    varTips(startT,endT,freq,keywords,dt,NoP)
    T,NoT = timeList(startT,endT,freq,dt)
    return startT,endT,dt,freq,NoT,T,keywords,pointsList,tol,NoP,srcDir,outputdir,L,rho
        