import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Classes.utils import parent_dir
from Classes.utils import gridsize_utils as gridsize
import re
import os

# To run this code you must be in the parent folder of agent-based-cancer

def getCoordsForPlot(step, allCellsCsvPath):
    df = pd.read_csv(allCellsCsvPath)
    df = df[["Step", "Total cells", "Position", "Phenotype"]]

    # Select the step you want to plot, from 0 to 24000 (~11 days)
    df_step0 = df.loc[df["Step"] == step]

    mPoints = df_step0.loc[df_step0["Phenotype"] == "mesenchymal"]["Position"] # Series object
    ePoints = df_step0.loc[df_step0["Phenotype"] == "epithelial"]["Position"]
    #vPoints = df_step0.loc[(df_step0["Agent Type"] == "vessel") & (df_step0["Ruptured"] == False)]
    #vRupturedPoints = df_step0.loc[(df_step0["Agent Type"] == "vessel") & (df_step0["Ruptured"] == True)]

    mPoints = list(mPoints.map(eval)) # [(104, 101), (101, 97), (101, 95)]
    ePoints = list(ePoints.map(eval))

    Xm, Ym = [i[0] for i in mPoints], [i[1] for i in mPoints]
    Xe, Ye = [i[0] for i in ePoints], [i[1] for i in ePoints]

    return [Xm, Ym, Xe, Ye]

def plotGrowthData(fig_index, allCellsCsvPath, imagesFolder):
    # get data at each step
    df = pd.read_csv(allCellsCsvPath)
    df = df[["Step", "Total cells", "Phenotype"]]

    plt.figure(fig_index)

    # For mesenchymal
    stepsize = 3000 #doubling rate
    df_m = df.loc[(df["Step"] % stepsize == 0)]
    # create arrays with the step number and number of cells
    steps = np.arange(0, max(df_m["Step"]) + 1, stepsize)
    numberMesenchymalEachStep = [df_m.loc[(df_m["Step"] == step) & (df_m["Phenotype"] == "mesenchymal")].shape[0] for step in steps]
    plt.plot(steps*11/24000, numberMesenchymalEachStep, label="Mesenchymal cells")

    # For epithelial
    stepsize = 2000 #doubling rate
    df_e = df.loc[(df["Step"] % stepsize == 0)]
    # create arrays with the step number and number of cells
    steps = np.arange(0, max(df_e["Step"]) + 1, stepsize)
    numberEpithelialEachStep = [df_e.loc[(df_e["Step"] == step) & (df_e["Phenotype"] == "epithelial")].shape[0] for step in steps]
    
    plt.plot(steps*11/24000, numberEpithelialEachStep, label="Epithelial cells")

    plt.title('Cells growth')
    plt.xlabel('Days')
    plt.ylabel('Number of cells')
    plt.legend(loc="upper left")

    # save the figure
    figure_path = os.path.join(CellsImagesPath, f'Cells growth.png')
    plt.savefig(figure_path)
    


def plotCancer(coordsList, i, imagesFolder):

    Xm, Ym, Xe, Ye = coordsList[0], coordsList[1], coordsList[2], coordsList[3]
    plt.figure(i, figsize=(6, 5))
    
    plt.scatter(Xm, Ym, marker='o', alpha=0.10, label="Mesenchymal cells")
    plt.scatter(Xe, Ye, marker='h', alpha=0.05, label="Epithelial cells")
    plt.xlim(0, gridsize)
    plt.ylim(0, gridsize)

    xticks = np.arange(0, gridsize, step=int(gridsize/6)) # 6 ticks
    xticklabels = [str(round(j,1)) for j in np.arange(0, 2.1, step = 2/201*(gridsize/6))]
    plt.xticks(xticks, xticklabels)
    plt.yticks(xticks, xticklabels)
    plt.xlabel("mm")
    plt.ylabel("mm")

    # save the figure
    figure_path = os.path.join(TumorImagesPath, f'{step}steps - Tumor size at {11/24000 * step:.2f} days.png')
    plt.savefig(figure_path)


    
    #plt.style.use("seaborn")

#NOT WORKING
def plotMMP2orECM(i, step, files_path, figCounter, type="Mmp2"):
    df = pd.read_csv(files_path[i], index_col=0)
    plt.figure(i+figCounter, figsize=(6, 5))

    if type=="Mmp2":
        plt.imshow(df) #plt.imshow(df, vmin=0, vmax=3)
        #print(f'mmp2 max at step {step} is {df.values.max()}')
    elif type == "Ecm":
        plt.imshow(df) #plt.imshow(df, vmin=0, vmax=1)
        #print(f'ecm min at step {step} is {df.values.min()}')
        
    plt.colorbar()

    plt.xlim(0, gridsize)
    plt.ylim(0, gridsize)

    xticks = np.arange(0, gridsize, step=int(gridsize/6)) # 6 ticks
    xticklabels = [str(round(j,1)) for j in np.arange(0, 2.1, step = 2/201*(gridsize/6))]
    plt.xticks(xticks, xticklabels)
    plt.yticks(xticks, xticklabels)
    plt.xlabel("mm")
    plt.ylabel("mm")

    plt.title(f'{type} at {11/24000 * step:.2f} days ({step} steps)')
    

    # save the figure
    if type=="Mmp2":
        figure_path = os.path.join(Mmp2ImagesPath, f'{step}steps - Mmp2 degradation at {11/24000 * step:.2f} days.png')
    elif type=="Ecm":
        figure_path = os.path.join(EcmImagesPath, f'{step}steps - Ecm evolution at {11/24000 * step:.2f} days.png')
    plt.savefig(figure_path)

###########################################################################################################

if __name__ == "__main__":

    # CHANGE THIS LINE according to the simulation you want to plot the graphs
    nameOfTheSimulation = "Sim maxSteps-1000 stepsize-200 N-388 gridsNumber-2"

    # Do not change anything below
    SimulationPath = os.path.join(parent_dir, nameOfTheSimulation)
    print(f'Analyzing data at {SimulationPath}')

    csv_files_name = [f for f in os.listdir(SimulationPath) if os.path.isfile(os.path.join(SimulationPath, f)) and f.endswith(".csv")]
    
    EcmPath = os.path.join(SimulationPath, "Ecm")
    Mmp2Path = os.path.join(SimulationPath, "Mmp2")
    ecm_files_name = [f for f in os.listdir(EcmPath) if os.path.isfile(os.path.join(EcmPath, f)) and f.endswith(".csv")]
    mmp2_files_name = [f for f in os.listdir(Mmp2Path) if os.path.isfile(os.path.join(Mmp2Path, f)) and f.endswith(".csv")]


    if csv_files_name:
        first_csv_name = csv_files_name[0]
        first_csv_path = os.path.join(SimulationPath, first_csv_name)
        all_cells_analysis_path = os.path.join(parent_dir, SimulationPath, first_csv_path)
        print("Using cells data at:", first_csv_path)
    else:
        print("No .csv cell data found in directory:", SimulationPath)

    if ecm_files_name:
        ecm_files_path = [os.path.join(EcmPath, p) for p in ecm_files_name]
        print("Using Ecm data at:", EcmPath)
    else:
        print("No .csv Ecm data found in directory:", EcmPath)

    if mmp2_files_name:
        mmp2_files_path = [os.path.join(Mmp2Path, p) for p in mmp2_files_name]
        print("Using Mmp2 data at:", Mmp2Path)
    else:
        print("No .csv Mmp2 data found in directory:", Mmp2Path)


    # use regex to find the values before 'steps' and 'stepsize'. Ex: 50steps-10stepsize-cells
    max_step = int(re.search(r"(\d+)steps", first_csv_name).group(1))
    step_size = int(re.search(r"(\d+)stepsize", first_csv_name).group(1))

    # Path to save all the images:
    imagesFolder = "Visual analysis"
    imagesPath = os.path.join(SimulationPath, imagesFolder)

    TumorImagesPath = os.path.join(imagesPath, "Tumor growth")
    CellsImagesPath = os.path.join(imagesPath, "Cells growth")
    EcmImagesPath = os.path.join(imagesPath, "Ecm evolution")
    Mmp2ImagesPath = os.path.join(imagesPath, "Mmp2 evolution")

    # Create folder for all the visual analysis
    if not os.path.exists(imagesPath):
        os.makedirs(imagesPath)
        os.makedirs(TumorImagesPath)
        os.makedirs(CellsImagesPath)
        os.makedirs(EcmImagesPath)
        os.makedirs(Mmp2ImagesPath)

    # If there the visual analysis is already done, tell the user
    else:
        print("This visual analysis already exists!")
    

    figCounter = 0
    # Plot the cells graphs
    for id, step in enumerate(reversed(range(0,max_step+1,step_size))):
        plotCancer(getCoordsForPlot(step, first_csv_path), id, imagesFolder)
        if step == 0:
            plt.title(f'Initial Tumor at {11/24000 * step:.2f} days ({step} steps)')
            plt.legend(loc="upper left")
        else:
            plt.title(f'Tumor size at {11/24000 * step:.2f} days ({step} steps)')
    figCounter += id + 1

    
    # Plot the Mmp2 graphs
    for id, step in enumerate(reversed(range(0,max_step+1,step_size))):
        plotMMP2orECM(id, step, mmp2_files_path, figCounter, type="Mmp2")
    figCounter += id + 1

    # Plot the Ecm graphs
    for id, step in enumerate(reversed(range(0,max_step+1,step_size))):
        plotMMP2orECM(id, step, ecm_files_path, figCounter, type="Ecm")
    figCounter += id + 1

    # Plot the growth of ephitelial and mesenchymal cells
    plotGrowthData(figCounter, first_csv_path, imagesFolder)

    plt.show()
    plt.close()




