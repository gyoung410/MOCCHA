"""
Functions to calculate physical properties
==============================

"""

import numpy as np

def calcAirDensity(temperature, pressure):

    """
    Function to calculate air density from temperature and pressure
    ==============================

    """

        #### EXAMPLE OF USE:
        #### data = calcAirDensity(data['temperature'][:], data['pressure'][:])

    R = 2.8704  #### hPa kg-1 K-1

    print 'Calculating air density profile:'
    print ''
    rho = np.zeros([np.size(temperature)])
    for k in range(0,np.size(temperature)):
        rho[k] = pressure[k] / (R * temperature[k])

    # print rho

    return rho


def calcThetaE(temperature, pressure, q, time, height):

    """
    Function to calculate equivalent potential temperature
    ==============================

    """

        #### EXAMPLE OF USE:
        #### data = calcThetaE(data_um, time_um, height)

    L_vap = 2.5e6    # J/kg
    L_sub = 2.836e6  # J/kg
    cp = 1004.6      # J/kg.K

    print 'Calculating theta:'
    theta = np.zeros([len(time),len(height)])
    for k in range(0,len(height)):
        theta[:,k] = temperature[:,k] * np.power(1e5 / pressure[:,k], 0.2854)

    print 'Calculating theta_e:'
    thetaE = np.zeros([len(time),len(height)])
    for k in range(0,len(height)):
        thetaE[:,k] = theta[:,k] + ((theta * L_vap * q[:,k]) / (cp * temperature[:,k]))

    return theta, thetaE