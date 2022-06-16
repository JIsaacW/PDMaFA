# README

**PDMaFA v1.0:** Point Data Monitor and Frequency Analysis Program v1.0



This program is to extract the values of specified points, then execute the frequency analysis based on points pressure data.

## Usage

### Dependence

```python
# Python version
python 3.6.9

# standard library
sys 
json 
time
os

# Third party library
numpy 1.19.5
matplotlib 3.3.4
vtk 9.1.0
```

### Program control

The program execute depend on `input.json` , most control variables are defined here.

```json
{
    "Length"   : 12.7,              // Characteristic length
    "density"  : 1,	                // Fluid density
    "startT"   : 1400,              // The first time step which you are intend to start the sampling
    "endT"     : 2800,              // The last time step which you are intednt to end the sampling
    "freq"     : 1,                 // The sampling frequency, usually equal to the increment of VTU files
    "dt"       : 0.002,             // The computing time step length
    "srcDir"   : "/home/isaac/Desktop/2Dtestcase_0615/96-procs",        // The result VTU files path
    "outputdir": "../Output/",                                          // The output directory path,
    "keywords" : ["Pressure","Velocity"],                               // The monitoring physical variables
    "pointsList" : [[128,0,0],[191.5,0,0],[255,0,0]],                   // The goal sampling points coordinates
    "tolerance": 0.7                                                    // Distance between goal points and real sampling points
}
```

### Run

1. Install the dependence packages

2. Modify the `input.json` control file

3. **Enter the following command in terminal to run the program:**

   ```bash
   bash .PDMaFA
   ```

4. The program has two features, one is point data sampling, the other is frequency, so you should choose which to execute when the program is started:

   * **Choose whether to execute  points data monitor, the terminal would prompt:**

     ```bash
     Press 'y' to re-read point data, 'n' to skip point data monitor.
     ```

     * You can press `y` to execute points data monitor, then the program will read the  vtu files and output points data information.

     * If you press `n`, then the program will skip points data monitor and execute frequency analysis directly. 

       > Attention: you can only execute frequency analysis directly when you have done points data monitor(`PressureData` should exist in `Output` directory), or there will come to an error.

   * **Choose whether to execute frequency, the terminal would prompt:**

     ```bash
     Enter 'y' to continue frequency analysis, 'n' to stop:
     ```

     You can press `y` to continue, press `n` to abort the procedure.

   * **When execute frequency analysis, the program will ask you to determine the average velocity which is used to calculated St number automatically or manually.**

     ```bash
     Enter 'A' to auto calculate average U or Enter 'M' to manual input:
     ```

     * You can press `A` to calculate the average velocity automatically, which means the program will calculate the average velocity used the monitoring velocity value in the sampling points.
     * Or you can press `M`, then you should enter the average velocity by yourself. Each sample point needs a average velocity, if you have 4 points here, you should enter 4 average velocity sequentially.

5. The post-process results will be output into `Output` directory commonly.

## Prompt

A typical pattern of prompt like that:

```bash
* Control Message 
Sample Variable: ['Pressure', 'Velocity']
Sample Points Number: 3
Start Physical Time: 2.800000 s
End Physical Time: 5.600000 s
Compute Time Step: 0.002 s
Sample Frequency: 1 s-1
Timestep Files Number: 1401

Press 'y' to re-read point data, 'n' to skip point data monitor.
y

 * Sample Message
Reading Pressure: 100.00 %
Pressure data shape:(1401, 3)
Reading Velocity: 100.00 %
Velocity data shape:(1401, 3, 3)
Sample error: [0.27662064 0.27435281 0.44264839]
Done! Used time: 107.323 s

 * Frequency analysis
Enter 'y' to continue frequency analysis, 'n' to stop:
y
Enter 'A' to auto calculate average U or Enter 'M' to manual input:
A
Auto calculate the average velocity.
Characteristic velocity: [266.83014473 357.09786922 240.96313044]
Done without any error!
```
