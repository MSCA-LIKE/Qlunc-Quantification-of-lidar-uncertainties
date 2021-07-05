# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 13:55:41 2020
@author: fcosta

Francisco Costa García
University of Stuttgart(c)

Here we calculate the uncertainty expansion from uncertainties obtained for
each lidar module following GUM (Guide to the expression of Uncertainties in 
Measurement) model. 
 
"""
from Utils.Qlunc_ImportModules import *
import Utils.Qlunc_Help_standAlone as SA

# Calculates the lidar global uncertainty using uncertainty expansion calculation methods:
global da
def sum_unc_lidar(Lidar,Atmospheric_Scenario,cts,Qlunc_yaml_inputs):
    """
    Lidar uncertainty estimation. Location: ./UQ_Functions/UQ_Lidar_Classes.py
    
    Parameters
    ----------
    
    * Lidar
        data...
    * Atmospheric_Scenario
        Atmospheric data. Integer or Time series
    * cts
        Physical constants
    * Qlunc_yaml_inputs
        Lidar parameters data
        
    Returns
    -------
    
    list
    
    """ 
    List_Unc_lidar = []
    
    if Lidar.photonics != 'None':
        try: # ecah try/except evaluates wether the component is included in the module, therefore in the calculations
    #        if Photodetector_Uncertainty not in locals():
            # pdb.set_trace()
            Photonics_Uncertainty,DataFrame = Lidar.photonics.Uncertainty(Lidar,Atmospheric_Scenario,cts,Qlunc_yaml_inputs)
            List_Unc_lidar.append(Photonics_Uncertainty['Uncertainty_Photonics'])
        except:
            Photonics_Uncertainty = None
            print('Error in photonics module calculations!')
    else:
        print('You didn´t include a photonics module in the lidar')
    if Lidar.optics != 'None':
        try:
            Optics_Uncertainty,DataFrame = Lidar.optics.Uncertainty(Lidar,Atmospheric_Scenario,cts,Qlunc_yaml_inputs)
            Optics_Uncertainty           = np.ndarray.tolist(Optics_Uncertainty['Uncertainty_Optics'])*len(Atmospheric_Scenario.temperature)
            List_Unc_lidar.append(np.array([Optics_Uncertainty]))
        except:
            Optics_Uncertainty = None
            print('Error in optics module calculations!')
    else:
        print('You didn´t include an optics module in the lidar')
    if Lidar.power !=0:
        
        try:
            Power_Uncertainty,DataFrame = Lidar.power.Uncertainty(Lidar,Atmospheric_Scenario,cts)
            List_Unc_lidar.append(Power_Uncertainty['Uncertainty_Power']*len(Atmospheric_Scenario.temperature))
        except:
            Power_Uncertainty = None
            print('No power module in calculations!')
    else:
        print('You didn´t include a power module in  the lidar')
    print('Processing lidar uncertainties...')
    Uncertainty_Lidar                     = SA.unc_comb(List_Unc_lidar)[0]
    # pdb.set_trace()
    Final_Output_Lidar_Uncertainty        = {'Lidar_Uncertainty':Uncertainty_Lidar}    
    Lidar.lidar_inputs.dataframe['Lidar'] = Final_Output_Lidar_Uncertainty['Lidar_Uncertainty']*np.linspace(1,1,len(Atmospheric_Scenario.temperature))
    
    # Include time in the dataframe:
    # Lidar.lidar_inputs.dataframe['Time']=Atmospheric_Scenario.time
    ########################################################################################################
    # Create Xarray to store data. Link with Mocalum and yaddum  ###########################################
    
    df=SA.to_netcdf(Lidar.lidar_inputs.dataframe,Qlunc_yaml_inputs,Lidar,Atmospheric_Scenario)

    ########################################################################################################
    ########################################################################################################
        
    print('Lidar uncertainty done')
    return Final_Output_Lidar_Uncertainty,Lidar.lidar_inputs.dataframe,df