import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt

def monitorPlot(keywords,NoT,NoP,T,keysPointsValue,outputdir):
    size = 150
    AVR = []
    ### Merge images
    for num,name in enumerate(keywords):
        fignum = num + 1
        var = keysPointsValue[num]
        if var.ndim == 3:
            pltvar = []
            for m in range(NoT):
                pltvar.append(np.linalg.norm(var[m],axis=1))
            pltvar = np.array(pltvar)
            name = name + ' Magnitude'
        else:
            pltvar = var
        plt.figure(dpi=size)
        for m in range(NoP):
            plt.plot(T,pltvar[:,m])
        plt.title('Fig'+str(fignum)+':'+name+' - t')
        plt.xlabel('Sample Time (s)')
        plt.ylabel(name)
        plt.legend(['P'+str(m+1) for m in range(NoP)])
        plt.savefig(outputdir+'Fig'+str(fignum)+'_'+name+' - t')
    ### Seperate images
    for num,name in enumerate(keywords):
        keyavr = []
        fignum = num + 1
        var = keysPointsValue[num]
        if var.ndim == 3:
            pltvar = []
            for m in range(NoT):
                pltvar.append(np.linalg.norm(var[m],axis=1))
            pltvar = np.array(pltvar)
            name = name + ' Magnitude'
        else:
            pltvar = var
        for m in range(NoP):
            plt.figure(dpi=size)
            plt.plot(T,pltvar[:,m])
            averagevalue = np.mean(pltvar[:,m])
            keyavr.append(averagevalue)
            plt.axhline(y=averagevalue,linestyle='--')
            plt.title('Fig'+str(fignum)+'-'+str(m+1)+':'+name+' - t')
            plt.xlabel('Sample Time (s)')
            plt.ylabel(name)
            plt.legend([str(m+1)])
            plt.savefig(outputdir+'Fig'+str(fignum)+'-'+str(m+1)+'_'+name+' - t')
        AVR.append(keyavr)
    AVR = np.array(AVR)
    np.savetxt(outputdir+'AverageValue',AVR)
    return AVR