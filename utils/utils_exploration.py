# -*- coding: utf-8 -*-
"""
En este archivo se encuentran los códigos para generar los plots de la data
sin procesar proveniente de los 17 sensores.

"""
#%% Imports
import numpy as np
import matplotlib.pyplot as plt
import random
#%% ConditionsLabels_dict
"""
Load the dict that contains the name of the five  hydraulic system's
conditions as keys and another dict as values. Values dicts contains the name
of each class as keys and the labels of the classes as values. 
"""
ConditionsLabels_dict = {
    'Cooler condition':{
        'Close to total failure':3,
        'Reduced effifiency':20,
        'Full efficiency':100
    },
    'Valve condition':{
        'Optimal switching behavior':100,
        'Small lag':90,
        'Severe lag':80,
        'Close to total failure':73
    },
    'Pump leakage':{
        'No leakage':0,
        'Weak leakage':1,
        'Severe leakage':2
    },
    'Accumulator condition':{
        'Optimal pressure':130,
        'Slightly reduced pressure':115,
        'Severely reduced pressure':100,
        'Close to total failure':90
    },
    'Stable flag':{
        'Stable' : 0, # Conditions were stable
        'Not stable' : 1 # Static conditions might not have been reached yet
    }    
}
#%% 
def get_classes_idx(condition_name, condition_labels):
    """
    Por cada clase perteneciente a la respectiva condición del activo físico,
    se elige de forma aleatoria un índice del array que contiene los labels y
    se guarda en un diccionario.
    --------------------------------------------------------------------------
    Parameters
        
    condition_name: {'Cooler condition','Valve condition','Pump leakage',
                    'Accumulator condition','Stable flag'}
        Name of hydraulic system's condition to be clasified.  

    condition_labels: np.array with shape (2205,)
        Array that contains the class label for each instance.   
    --------------------------------------------------------------------------
    Returns
    out: dictionary
        Class indexes stored as {class_name : class_index}.
    """    
    indexes = {}
    #Iter over condition classes
    for class_name , class_label in ConditionsLabels_dict[condition_name].items():        
        class_labels_idxs = []
        for label_idx in range(2205):
            label = condition_labels[label_idx]
            if int(label) == class_label:
                class_labels_idxs.append(label_idx)
            else:
                pass    
        #Get 1 random indx for each class
        indexes[class_name] = random.choice(class_labels_idxs)
    return indexes
#%%
def get_MeasureUnit(sensor_name):
    """
    Returns a str with the sensor's measurement unit.
    --------------------------------------------------------------------------
    Parameters
    
    sensor_name: {'Temperature sensor 1','Temperature sensor 2',
                  'Temperature sensor 3','Temperature sensor 4',
                  'Vibration sensor','Cooling efficiency','Cooling power',
                  'Efficiency factor','Flow sensor 1','Flow sensor 2',
                  'Pressure sensor 1','Pressure sensor 2','Pressure sensor 3',
                  'Pressure sensor 4','Pressure sensor 5','Pressure sensor 6',
                  'Motor power'}
        sensor's name as str to be matched to their corresponding
        measurement unit.
    
    --------------------------------------------------------------------------
    Returns
    out: str
        measurement unit as str.
    
    """
    measurement_units_dict = {
          'Temperature sensor 1' : 'Temperature [°C]',
          'Temperature sensor 2' : 'Temperature [°C]',
          'Temperature sensor 3' : 'Temperature [°C]',
          'Temperature sensor 4' : 'Temperature [°C]',
          'Vibration sensor' : 'Speed [mm/s]',
          'Cooling efficiency' : 'Efficiency [%]',
          'Cooling power' : 'Power [kW]',
          'Efficiency factor' : 'Efficiency [%]',
          'Flow sensor 1' : 'Water flow [L/min]',
          'Flow sensor 2' : 'Water flow [L/min]',
          'Pressure sensor 1' : 'Pressure [bar]',
          'Pressure sensor 2' : 'Pressure [bar]',
          'Pressure sensor 3' : 'Pressure [bar]',
          'Pressure sensor 4' : 'Pressure [bar]',
          'Pressure sensor 5' : 'Pressure [bar]',
          'Pressure sensor 6' : 'Pressure [bar]',
          'Motor power' : 'Power [W]'
          }
    for key in measurement_units_dict.keys():
        if key == sensor_name:
            return measurement_units_dict[sensor_name]
#%%
def plt_RawSignals(RawData_dict, condition_name, condition_labels,
                   fig_sz=(14,9), dpi=200, subplt=(6,3)):
    """
    Plots the raw signal for each sensor, for a certain condition.
    --------------------------------------------------------------------------
    Parameters
    
    RawData_dict: dict
         Dict with the raw data from the sensors, in the form
         {sensor_name : data_raw}.
     
    condition_name: {'Cooler condition','Valve condition','Pump leakage',
                     'Accumulator condition','Stable flag'}
        Name of hydraulic system's condition to be clasified.       

    condition_labels: np.array with shape (2205,)
        Array that contains the class label for each instance.
    
    fig_sz: tuple (heigth,width), default=(14,9)
        Tuple that contains the heigth and the width for the figure to plot.
    
    dpi: int, default=200
        Number of pixels for the figure to plot.
    
    subplt: tuple (number_rows,number_cols), default=(6,3)
        Number of rows and colums for the subplots in the figure.
    --------------------------------------------------------------------------
    Returns
    out: plots
    """
    plt.figure(figsize=fig_sz , dpi=dpi)  
    #Get random indxs for each class
    indexes = get_classes_idx(condition_name,condition_labels)
    #Subplots
    for sensor_name in list(RawData_dict): 
        sensor_data = RawData_dict[sensor_name] 
        #Time vector
        len_TimeVector = sensor_data.shape[1]
        dt = 60/len_TimeVector
        t = np.linspace(0,dt*(len_TimeVector-1),len_TimeVector)
        #Subplot position
        i = list(RawData_dict).index(sensor_name) + 1
        m,n = subplt
        plt.subplot(m,n,i)
        #Iter over classes        
        for class_name , class_idx in indexes.items():
            plt.plot(t,sensor_data[class_idx,:],label=class_name)
        #FigText
        title = 'Raw signal ' + condition_name + '\n{}'.format(sensor_name)
        plt.title(title,size=12)
        plt.xlabel('Time [seconds]',size=11)
        plt.ylabel(get_MeasureUnit(sensor_name),size=11)
        plt.legend()      
    plt.tight_layout()
    plt.show()
#%%
def plt_RawSignalsES(RawData_dict, condition_name, condition_labels,
                     fig_sz=(10,13.5), dpi=200, subplt=(6,3), tit_sz = 15, 
                     subplt_tit_sz = 12, subplt_XYlabel_sz = 12,
                     save_fig = False, tail = '.png', bbox = (0.75, 0.9)):
    """
    Plotea las señales en raw para cada sensor, en español.
    --------------------------------------------------------------------------
    Returns
    out: plots
    """
    Nombres_clases = {
        'Cooler condition':{
            'Close to total failure': 'Cerca de la falla total',
            'Reduced effifiency':'Eficiencia reducida',
            'Full efficiency':'Eficiencia total'
        },
        'Valve condition':{
            'Optimal switching behavior': 'Comportamiento óptimo del switch',
            'Small lag': 'Pequeño retraso del switch',
            'Severe lag': 'Retraso severo del switch',
            'Close to total failure':'Cerca de la falla total'
        },
        'Pump leakage':{
            'No leakage': 'Sin fuga',
            'Weak leakage': 'Fuga leve',
            'Severe leakage': 'Fuga severa'
        },
        'Accumulator condition':{
            'Optimal pressure': 'Presión óptima',
            'Slightly reduced pressure': 'Presión ligeramente reducida',
            'Severely reduced pressure': 'Presión severamente reducida',
            'Close to total failure':'Cerca de la falla total'
        },
        'Stable flag':{
            'Stable' : 'Sistema estable',
            'Not stable' : 'Sistema no estable'
        }    
    }
    condiciones = {
        'Cooler condition' : 'estado del enfriador',
        'Valve condition' : 'estado de la válvula',
        'Pump leakage' : 'fuga en la bomba',
        'Accumulator condition' : 'estado del acumulador',
        'Stable flag' : 'estabilidad del sistema'
        }
    Unidades_de_medida = {
          'Temperature sensor 1' : 'Temperatura [°C]',
          'Temperature sensor 2' : 'Temperatura [°C]',
          'Temperature sensor 3' : 'Temperatura [°C]',
          'Temperature sensor 4' : 'Temperatura [°C]',
          'Vibration sensor' : 'Velocidad [mm/s]',
          'Cooling efficiency' : 'Eficiencia [%]',
          'Cooling power' : 'Potencia [kW]',
          'Efficiency factor' : 'Eficiencia [%]',
          'Flow sensor 1' : 'Flujo [L/min]',
          'Flow sensor 2' : 'Flujo [L/min]',
          'Pressure sensor 1' : 'Presión [bar]',
          'Pressure sensor 2' : 'Presión [bar]',
          'Pressure sensor 3' : 'Presión [bar]',
          'Pressure sensor 4' : 'Presión [bar]',
          'Pressure sensor 5' : 'Presión [bar]',
          'Pressure sensor 6' : 'Presión [bar]',
          'Motor power' : 'Potencia [W]'
          }
    Nombre_sensores = {
          'Temperature sensor 1' : 'Sensor de temperatura 1',
          'Temperature sensor 2' : 'Sensor de temperatura 2',
          'Temperature sensor 3' : 'Sensor de temperatura 3',
          'Temperature sensor 4' : 'Sensor de temperatura 4',
          'Vibration sensor' : 'Sensor de vibración',
          'Cooling efficiency' : 'Eficiencia del enfriador',
          'Cooling power' : 'Potencia del enfriador',
          'Efficiency factor' : 'Factor de eficiencia',
          'Flow sensor 1' : 'Sensor de flujo 1',
          'Flow sensor 2' : 'Sensor de flujo 2',
          'Pressure sensor 1' : 'Sensor de presión 1',
          'Pressure sensor 2' : 'Sensor de presión 2',
          'Pressure sensor 3' : 'Sensor de presión 3',
          'Pressure sensor 4' : 'Sensor de presión 4',
          'Pressure sensor 5' : 'Sensor de presión 5',
          'Pressure sensor 6' : 'Sensor de presión 6',
          'Motor power' : 'Potencia del motor'
          }
    
    fig = plt.figure(figsize=fig_sz , dpi=dpi)
    suptitle = 'Datos sin procesar de ' + condiciones[condition_name]
    fig.suptitle(suptitle + '\n'+'\n'+'\n', size = tit_sz)
    #Get random indxs for each class
    indexes = get_classes_idx(condition_name,condition_labels)
    #Subplots
    for sensor_name in list(RawData_dict): 
        sensor_data = RawData_dict[sensor_name] 
        #Time vector
        len_TimeVector = sensor_data.shape[1]
        dt = 60/len_TimeVector
        t = np.linspace(0,dt*(len_TimeVector-1),len_TimeVector)
        #Subplot position
        i = list(RawData_dict).index(sensor_name) + 1
        m, n = subplt
        plt.subplot(m, n, i)
        #Iter over classes
        Labels = []
        for class_name , class_idx in indexes.items():
            plt.plot(t, sensor_data[class_idx,:])
            Labels.append(Nombres_clases[condition_name][class_name])
        #FigText
        plt.title(Nombre_sensores[sensor_name], size = subplt_tit_sz )
        plt.xlabel('Tiempo [segundos]', size = subplt_XYlabel_sz)
        plt.ylabel(Unidades_de_medida[sensor_name ], size = subplt_XYlabel_sz)
    
    if len(indexes) == 3:
        Ncol = 3
    else:
        Ncol = 2
    #bbox_to_anchor = (x, y, width, height)
    fig.legend(labels = Labels, ncol = Ncol, fancybox=True, fontsize = 'large',
               bbox_to_anchor = bbox)
    plt.tight_layout()
    if save_fig == True:
        head = 'images/RawData/RawData_' + condition_name.split(' ')[0]
        plt.savefig(head + tail)
    else:
        pass
    plt.show()