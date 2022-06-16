# main.py

import IO
import sample
import analysis
import plot

import sys
import numpy as np


startT,endT,dt,freq,NoT,T,keywords,pointsList,tol,NoP,srcDir,outputdir,L,rho = IO.readinput()

PMflag = input("\nPress 'y' to re-read point data, 'n' to skip point data monitor.\n")
if PMflag in ['y','Y','1','T','t']:
    keysPointsValue, Dis = sample.sample(startT,endT,freq,keywords,pointsList,srcDir,outputdir,tol)
    AVR = plot.monitorPlot(keywords,NoT,NoP,T,keysPointsValue,outputdir)
elif PMflag in ['n','N','F','f','0']:
    AVR = np.loadtxt(outputdir+'AverageValue')
    if AVR.ndim == 1:
        AVR = np.expand_dims(AVR, axis=1)
else:
    print('Invalid input.')
    sys.exit()


print('\n * Frequency analysis')
flag = 'True'
failNum = 0
while flag == 'True':
    freflag = input("Enter 'y' to continue frequency analysis, 'n' to stop:\n")
    if freflag in ['y','Y','1','T','t']:
        Uflag = input("Enter 'A' to auto calculate average U or Enter 'M' to manual input:\n")
        flag = 'False'
        if Uflag in ['A','a']:
            print('Auto calculate the average velocity.')
            for num,key in enumerate(keywords):
                if key == 'Velocity':
                    U = AVR[num]
                    break
        elif Uflag in ['M','m']:
            print('Manul enter the average velocity.')
            U = []
            for j in range(NoP):
                U.append(eval(input('Enter average U in point'+str(j+1)+':\n')))
        else:
            flag = 'True'
            failNum += 1
            if failNum == 6:
                print('Fail to choose the determination method of average U.\n')
                Flag = 'False'
            else:
                print("Please press 'A' or 'M' to choose the determination method of average U!\n")
    else:
        flag = 'False'
        print('The frequency analysis has been canceled.')

if freflag in ['y','Y','1','T','t']:
    print('Characteristic velocity:',U)
    analysis.analysis(outputdir,T,dt,freq,L,U,rho)