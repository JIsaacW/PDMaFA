import sys
import time
import os
import vtk
import numpy as np
from vtk.util import numpy_support as vtknp

def readvtu(filename):
    reader = vtk.vtkXMLUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.Update()
    vtudata = reader.GetOutput()
    NoP = vtudata.GetNumberOfPoints()
    temp_vtk_array = vtudata.GetPoints().GetData()
    coord = vtknp.vtk_to_numpy(temp_vtk_array)
    return vtudata,coord

def GetSampleSN(allCoord,pointsList,tol):
    SamplesSN = []
    Dis = []
    for point in pointsList:
        diff = allCoord - point
        diffnorm = np.linalg.norm(diff,axis=1)
        dis = np.min(diffnorm)
        if dis <= tol:
            SampleSN = np.argmin(diffnorm)
        else:
            SampleSN = 'NaN'
            print('Minimun distance exceed the tolerence!')
            sys.exit()
        Dis.append(dis)
        SamplesSN.append(SampleSN)
    Dis = np.array(Dis)
    # print('Real sample points:\n{:}'.format(allCoord[SamplesSN]))
    # print('\nReal sample SN:\n{}'\n''.format(SamplesSN))
    return SamplesSN,Dis

def GetSampleVal(scrdata,keyword,SamplesSN):
    if keyword == "Pressure":
        temp_vtk_array = scrdata.GetPointData().GetScalars(keyword)
    elif keyword in ["Traction","Velocity","Vorticity","WSS","Strain","Stress","Displacement"]:
        temp_vtk_array = scrdata.GetPointData().GetVectors(keyword)
    else:
        print('Cannot find goal keyword!')
        sys.exit()
    fieldValue = vtknp.vtk_to_numpy(temp_vtk_array)
    SamplesVal = fieldValue[SamplesSN]
    return SamplesVal

def pointsSample(startT,endT,freq,keyword,pointsList,srcDir,tol):
    NoT = int((endT-startT)/freq+1)
    pointsValue = []
    for i in range(NoT):
        ntime = startT + i*freq
        if ntime < 100:
            fname = "{}/result_{:03d}.vtu".format(srcDir,ntime)
        else:
            fname = "{}/result_{:d}.vtu".format(srcDir,ntime)
        scrdata,coord = readvtu(fname)
        if i == 0:
            SamplesSN,Dis = GetSampleSN(coord,pointsList,tol)
            SamplesVal = GetSampleVal(scrdata,keyword,SamplesSN)
            pointsValue.append(SamplesVal)
        else:
            SamplesVal = GetSampleVal(scrdata,keyword,SamplesSN)
            print("\rReading "+keyword+": {:.2f} %".format((i+1)/NoT*100),end="")
            pointsValue.append(SamplesVal)
    pointsValue = np.array(pointsValue)
    return pointsValue,Dis

# ------------------------------------------------------------------ #

def sample(startT,endT,freq,keywords,pointsList,srcDir,outputdir,tol):
    t1 = time.time()
    keysPointsValue = []
    print('\n * Sample Message')
    isExits=os.path.exists(outputdir)
    if not isExits:
        os.makedirs(outputdir)
    pathmessage = []
    for keyword in keywords:
        pointsValue,Dis = pointsSample(startT,endT,freq,keyword,pointsList,srcDir,tol)
        outputfilename = keyword+'Data'
        if pointsValue.ndim == 2:
            np.savetxt(outputdir+outputfilename,pointsValue)
            pathmessage.append(outputdir+outputfilename)
        else:
            np.save(outputdir+outputfilename,pointsValue)
            pathmessage.append(outputdir+outputfilename+'.npy')
        keysPointsValue.append(pointsValue)
        print('\n{} data shape:{}'.format(keyword,np.shape(pointsValue)))
    t2 = time.time()
    print('Sample error:',Dis)
    print('Done! Used time: {:.3f} s\n'.format(t2-t1))
    return keysPointsValue, Dis