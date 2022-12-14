# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 19:57:05 2020
@author: fcosta

Francisco Costa García
University of Stuttgart(c) 

###############################################################################
###################### __ Classes __ ##########################################
  
Creating components, modules and lidar classes. 
The command class is used to create digital "objects", representing the lidar 
components, and store necessary information to calculate uncertainties coming 
from hardware and data processing methods. 

`unc_func` contains the functions calculating the uncertainty for each
component, module and/or lidar system.
It is defined as a python module, so users can define their own uncertainty 
functions and implement them easily just pointing towards a different python 
module. 

Flags, general constants and atmospheric scenarios used along the calculations 
are also treated as classes. User should instantiate all, but the general 
constants.


How is the code working?

If user wants to implement another component/module s/he should create a class. 

For example, we might want build up a lidar and user wants to include a 'power'
module which, in turn contains an UPS (uninterruptible power supply) with 
certain parameter values, e.g. output power and output voltage. Let's call them
Pout and Vout. 

1) Create the `classes`:
    
So we create the class `UPS`:
    
def UPS():
    def __init__(self,PowerOutput,VoltageOutput,Uncertainty)
        
        self.Pout     = PowerOutput
        self.Vout     = VoltageOutput
        self.unc_func = Uncertainty

And also the class `power`, including the UPS component:

def power():
    def __init__UPS (self, U_PowerSupply,Uncertainty)
        self.UPS     = U_PowerSupply
        self.unc_fun = Uncertainty 

Then, the lidar is created (in this simple example) by including the module in 
a lidar class:

class lidar():
      def __init__ (self, Power_Module,Uncertainty)
          self.PowerMod = Power_Module
          self.unc_fun  = Uncertainty

Setting an atmospheric scenario is also needed:
class atmos_sc():
    def __init__ (self, Temperature, Humidity):
        self.T = Temperature
        self.H = Humidity
    
2) Instantiate the classes

Instantiating the component class:
UPS_1 = UPS(Pout     = 500, % in watts
            Vout     = 24,  % in volts
            unc_func = function calculating uncertainties)

Instantiating the module class to create the `Power` object:
Power_1 = power(Power_Module = UPS_1,
                unc_func      = function calculating uncertainties) 
        

Instantiating the lidar class:
Lidar_1 = lidar(Power_Module = Power_1,
                unc_func     = function calculating uncertainties)

So we have created a lidar digital twin with its first module, the `power` 
module, which in turn contains a component, the uninterruptible power supply.

Qlunc uses GUM (Guide to the expression of Uncertainties in Measurement) 
suggestions to calculate uncertainty expansion.  
  
"""

#%% Constants:
class cts():
    k = 1.38064852e-23 # Boltzman constant:[m^2 kg s^-2 K^-1]
    h = 6.6207004e-34 # Plank constant [m^2 kg s^-1]
    e = 1.60217662e-19 # electron charge [C]
    c = 2.99792e8 #speed of light [m s^-1]
    
#%% LIDAR COMPONENTS
  
#Component Classes:
class photodetector():
    def __init__(self,name,Photo_BandWidth,Load_Resistor,Photo_efficiency,Dark_Current,Photo_SignalP,Power_interval,Gain_TIA,V_Noise_TIA,unc_func):
                 self.PhotodetectorID  = name 
                 self.BandWidth        = Photo_BandWidth 
                 self.Load_Resistor    = Load_Resistor 
                 self.Efficiency       = Photo_efficiency
                 self.DarkCurrent      = Dark_Current
                 self.SignalPower      = Photo_SignalP
                 self.Power_interval   = Power_interval
                 self.Gain_TIA         = Gain_TIA
                 self.V_Noise_TIA      = V_Noise_TIA
                 self.Uncertainty      = unc_func
                 print('Created new photodetector: {}'.format(self.PhotodetectorID))
        
class optical_amplifier():
    def __init__(self,name,NoiseFig,OA_Gain,unc_func):
                 self.Optical_AmplifierID = name
                 self.NoiseFig            = NoiseFig
                 self.OA_Gain                = OA_Gain
                 self.Uncertainty         = unc_func
                 print('Created new optical amplifier: {}'.format(self.Optical_AmplifierID))
        
class power_source():
    def __init__(self,name,Inp_power,Out_power,unc_func):
                 self.Power_SourceID = name
                 self.Input_power    = Inp_power
                 self.Output_power   = Out_power
                 self.Uncertainty    = unc_func
                 print('Created new power source: {}'.format(self.Power_SourceID))

class laser():
    def __init__(self,name,Wavelength,e_Wavelength,Out_power,unc_func):
                 self.Power_SourceID = name
                 self.Wavelength     = Wavelength
                 self.e_Wavelength   = e_Wavelength
                 self.Output_power   = Out_power
                 self.Uncertainty    = unc_func
                 print('Created new power source: {}'.format(self.Power_SourceID))        

class converter(): # Not included yet in Version Qlunc v-0.9 calculations
    def __init__(self,name,frequency,Conv_BW,Infinit,unc_func):
                 self.ConverterID = name
                 self.Frequency   = frequency
                 self.BandWidth   = Conv_BW
                 self.Infinit     = Infinit
                 self.Uncertainty = unc_func
                 print('Created new converter: {}'.format(self.ConverterID))

class scanner():
    def __init__(self,name,scanner_type,pattern,origin,sample_rate,focus_dist,cone_angle,azimuth,x,y,z,stdv_focus_dist,stdv_cone_angle,stdv_azimuth,unc_func):
                 self.ScannerID       = name
                 self.scanner_type    = scanner_type
                 self.origin          = origin
                 self.pattern         = pattern
                 self.sample_rate     = sample_rate
                 self.focus_dist      = focus_dist
                 self.cone_angle      = cone_angle
                 self.azimuth         = azimuth
                 self.stdv_focus_dist = stdv_focus_dist
                 self.stdv_cone_angle = stdv_cone_angle
                 self.stdv_azimuth    = stdv_azimuth                 
                 self.x               = x
                 self.y               = y
                 self.z               = z               
                 self.Uncertainty     = unc_func      
                 print('Created new scanner: {}'.format(self.ScannerID))        

class optical_circulator():
    def __init__(self,name, insertion_loss,unc_func):#,isolation,return_loss): 
                 self.Optical_CirculatorID = name
                 self.insertion_loss       = insertion_loss # max value in dB
        #        self.isolation            = isolation
        #        self.return_loss          = return_loss
                 self.Uncertainty          = unc_func
                 print ('Created new optical circulator: {}'.format(self.Optical_CirculatorID))
        
#%% LIDAR MODULES

# Modules classes

class photonics():
    def __init__(self,name,photodetector,optical_amplifier,unc_func):
                 self.PhotonicModuleID   = name
                 self.photodetector      = photodetector
                 self.optical_amplifier  = optical_amplifier
                 self.Uncertainty        = unc_func 
                 print('Created new photonic module: {}'.format(self.PhotonicModuleID))

class power(): # Not included yet in Version Qlunc v-0.9 calculations
    def __init__(self,name,power_source,converter,unc_func):
                 self.PowerModuleID  = name
                 self.power_source  = power_source
                 self.converter     = converter
                 self.Uncertainty   = unc_func  
                 print('Created new power module: {}'.format(self.PowerModuleID))

class optics():
    def __init__(self,name,scanner,optical_circulator,laser,unc_func):
                 self.OpticsModuleID     = name
                 self.scanner            = scanner
                 self.optical_circulator = optical_circulator
                 self.laser              = laser
                 self.Uncertainty        = unc_func 
                 print('Created new optic module: {}'.format(self.OpticsModuleID))
        
#%% Atmosphere object:
class atmosphere():
    def __init__(self,name,temperature):
                 self.AtmosphereID = name
                 self.temperature  = temperature
                 print('Created new atmosphere: {}'.format(self.AtmosphereID))


#%% Creating lidar general data class:
class lidar_gral_inp():
    def __init__(self,name,wave,yaw_error,pitch_error,roll_error,dataframe):
                 self.Gral_InputsID   = name
                 self.Wavelength      = wave
                 self.yaw_error_dep   = yaw_error   # yaw error angle when deploying the lidar device in the grounf or in the nacelle
                 self.pitch_error_dep = pitch_error # pitch error angle when deploying the lidar device in the grounf or in the nacelle
                 self.roll_error_dep  = roll_error  # roll error angle when deploying the lidar device in the grounf or in the nacelle        
                 self.dataframe       = dataframe
                 print('Created new lidar general inputs: {}'.format(self.Gral_InputsID))

#%% Lidar class
class lidar():
    def __init__(self,name,photonics,optics,power,lidar_inputs,unc_func):
                 self.LidarID      = name
                 self.photonics    = photonics
                 self.optics       = optics
                 self.power        = power 
                 self.lidar_inputs = lidar_inputs
                 self.Uncertainty  = unc_func
                 print('Created new lidar device: {}'.format(self.LidarID))



