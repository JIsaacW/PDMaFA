import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt


def FFT (T,data):
    AMP = np.abs(np.fft.fft(data))
    n = AMP.size
    timestep = T[1]-T[0]
    Fre = np.fft.fftfreq(n,d=timestep)
    return Fre[Fre>0], AMP[Fre>0]

def pressFreAnalysis(fluP,outputdir,T,L,U,rho):
    plt.figure(dpi=200)
    plt.title('Frequency Analysis for Pressure Fluctuation')
    plt.xlabel('St')
    plt.ylabel('Ep')
    plt.xscale("log")
    plt.yscale("log")
    allSt = []
    allEp = []
    for num,pointVal in enumerate(np.transpose(fluP)):
        Fre, AMP = FFT(T,pointVal)
        St = Fre*L/U[num]
        Ep = AMP/(rho*U[num]**2)/2
        plt.plot(St,Ep,linewidth=0.5)
        allSt.append(St)
        allEp.append(Ep)
    plt.legend(['P'+str(m+1) for m in range(len(np.transpose(fluP)))])
    plt.savefig(outputdir+'Pressure Frequency Analysis')
    allSt = np.array(allSt)
    allEp = np.array(allEp)
    np.savetxt(outputdir+"St Data",allSt)
    np.savetxt(outputdir+"Ep Data",allEp)
    return allSt,allEp

def pressFlu(path,T,dt,freq):
    P = np.loadtxt(path)
    cycle = T[-1]
    TAvrP = np.sum(P,axis = 0)*dt*freq/cycle
    fluP = P - TAvrP
    if fluP.ndim == 1:
        fluP = np.expand_dims(fluP, axis=1)
    return fluP

def analysis(outputdir,T,dt,freq,L,U,rho):
    path = outputdir+"PressureData"
    fluP = pressFlu(path,T,dt,freq)
    allSt,allEp= pressFreAnalysis(fluP,outputdir,T,L,U,rho)
    print('Done without any error!')