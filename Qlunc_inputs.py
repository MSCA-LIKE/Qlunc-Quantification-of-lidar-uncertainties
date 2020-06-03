# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 09:14:00 2020

@author: fcosta
"""
#%% Header:
#04272020 - Francisco Costa
#SWE - Stuttgart
#LiUQ inputs for different modules:
#Here the user can introduce parameters to calculate the uncertainty of the different modules and components.. Must be note units of the uncertainties: either dB or watts

# Inputs:
#    Modules can be: 'amplifier', 'telescope', 'photodetector'
#    Data processing methods can be: 'LOS', 'filtering methods'
#    Temperature= [-15,0,15] for example
#    Humidity = [0,25,50,75]% for example
#    rain        = False
#    fog         = False  #for rain and fog intensity intervals might be introduced [none,low, medium high]
#    Values of uncertainties will be introduced in dB (for now)
#%% Inputs:.

#import Data:
import pandas as pd
import sys,inspect
from functools import reduce
from operator import getitem
# Which modules introduce incertalistinties?:
#flag_unc_amplifier     = True # if True I include amplifier uncertainty
#flag_unc_photodetector = True # if True I include photodetector uncertainty
#flag_unc_telescope     = True # if True I include telescope uncertainty
# Want to execute LiUQ?
#flag_exec_LiUQ         = True
flag_plot_signal_noise  = True


#%%Directories Class:
class direct():
    Main_directory='../Qlunc-master/' # For now all data is stored here

#%% Inputs class where are stored all inputs:
class inputs():
    
    
    # Modules is a dictionary containing the lidar modules as a key. As values there is a nested dictionary containing components as keys and type of uncertainty as values.
    # Each of this values is related with a function which calculates this specific uncertainty. The relation between type of unc. and function calculating it is in LiUQ_core when defining methods.
    modules = {
               'power'     : {'power_source' :['power_source_noise'],                    # for now: 'power_source_noise',...
                              'converter'    :['converter_losses','converter_noise']},                     # for now:'converter_noise', 'converter_losses'...
    
               'photonics' : {'photodetector':['photodetector_noise'],                   # for now:'photodetector_noise',....
                              'amplifier'    :[],                       #for now:  'amplifier_noise',... If user includes amplifier component in dictionary 'modules', figure noise is automatically included in calculations(if don't want to include it have to put 0 in 'Amplifier_uncertainty_inputs')
                              'laser_source' :['laser_source_noise']} ,                  # for now:'laser_source_noise',...
                              
               'optics'    : {'telescope'    :['telescope_noise']}                       # for now:'telescope_noise', 'telescope_losses'...
               }
#    DP      = ['los'] # data processing methods we want to assess

     
#%% Atmospheric inputs:
    class atm_inp():
        TimeSeries=False  # This defines whether we are using a time series (True) or single values (False) to describe the atmosphere (T, H, rain and fog) 
                          # If so we obtain a time series describing the noise implemented in the measurement.
        if TimeSeries:
            Atmos_TS_FILE           = 'AtmosphericScenarios.csv'
            AtmosphericScenarios_TS = pd.read_csv(direct.Main_directory+Atmos_TS_FILE,delimiter=';',decimal=',')
            Atmospheric_inputs={'temperature' : list(AtmosphericScenarios_TS.loc[:,'T']),
                                'humidity'    : list(AtmosphericScenarios_TS.loc[:,'H']),
                                'rain'        : list(AtmosphericScenarios_TS.loc[:,'rain']),
                                'fog'         : list(AtmosphericScenarios_TS.loc[:,'fog']),
                                'time'        : list(AtmosphericScenarios_TS.loc[:,'t'])} #for rain and fog intensity intervals might be introduced [none,low, medium high]
        else:    
            Atmospheric_inputs={'temperature' : [25,30],
                                'humidity'    : [35,27],
                                'rain'        : [True],
                                'fog'         : [False]}#for rain and fog intensity intervals might be introduced [none,low, medium high]
#%% General lidar layout inputs:
    class lidar_inp():
        Lidar_inputs = {'Wavelength' : [1532,1560]}
#        BW=  #Band width (MHz)
#        laser_input_power =  #[W]
        
#%% Power Modules inputs:
    class power_inp():
        PowerSource_uncertainty_inputs = {'power_source_noise'       : [.8],
                                          'power_source_OtherChanges': [.09]}
        Converter_uncertainty_inputs   = {'converter_noise'          : [4],
                                          'converter_OtherChanges'   : [.005885],
                                          'converter_losses'         :[0.056]}

    
    
#%% Photonics module inputs:
    class photonics_inp():
        Amplifier_uncertainty_inputs      = {'amplifier_noise'            : [0.7777],
                                             'amplifier_OtherChanges'     : [.005],
                                             'amplifier_fignoise'         : 'NoiseFigure.csv'}##
        LaserSource_uncertainty_inputs    = {'laser_source_noise'         : [.855],
                                             'laser_source_OtherChanges'  : [.07709]}
        Photodetector_uncertainty_inputs  = {'photodetector_noise'        : [0.2],
                                             'photodetector_OtherChanges' : [.105],
                                             'photodetector_Noise_FILE'   :'Noise_Photodetector.csv'}
    
#%% Optics module inputs    
    class optics_inp():
        Telescope_uncertainty_inputs      = {'telescope_curvature_lens' : [.01],
                                             'telescope_OtherChanges'   : [.006],
                                             'telescope_aberration'     : [.0004],
                                             'telescope_losses'         : [.099]}


#%%
    class VAL():
            [VAL_T,VAL_H,VAL_WAVE,
             VAL_NOISE_CONVERTER,VAL_OC_CONVERTER,VAL_CONVERTER_LOSSES,
             VAL_NOISE_POWER_SOURCE,VAL_OC_POWER_SOURCE,
             VAL_NOISE_AMPLI,VAL_OC_AMPLI,VAL_NOISE_FIG,
             VAL_NOISE_LASER_SOURCE,VAL_OC_LASER_SOURCE,
             VAL_NOISE_PHOTO,VAL_OC_PHOTO,
             VAL_CURVE_LENS_TELESCOPE,VAL_OC_TELESCOPE,VAL_ABERRATION_TELESCOPE,VAL_LOSSES_TELESCOPE]=[None]*19

class user_inputs():
    user_imodules=list(inputs.modules.keys())
    user_icomponents=[list(reduce(getitem,[i],inputs.modules).keys()) for i in inputs.modules.keys()]
    user_itype_noise= [list(inputs.modules[module].get(components,{})) for module in inputs.modules.keys() for components in inputs.modules[module].keys()]
