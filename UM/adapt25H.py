###
###
### SCRIPT TO READ IN UM MODEL DATA IN NETCDF FORMAT AS IRIS CUBE
###
###

# from __future__ import print_function
import time
import datetime
import numpy as np
from netCDF4 import Dataset
import numpy as np
import pandas as pd
import diags_MOCCHA as diags
import diags_varnames as varnames
import cartopy.crs as ccrs
import iris
import matplotlib.pyplot as plt
import matplotlib.cm as mpl_cm
import os

def readfile(filename):

    import pandas as pd

    # print '******'
    print ''
    print 'Reading .txt file with pandas'
    print ''

    data = pd.read_csv(filename, sep = " ")
    values = data.values

    return data

def assignColumns(data):

    columns = ['Year', 'Month', 'Day', 'Hour', 'Minutes', 'Seconds', 'Longitude', 'Latitude']

    return columns

def iceDrift(data):

    ###################################
    ## Define ice drift period
    ###################################

    Aug_drift_index = np.where(np.logical_and(data.values[:,2]>=14,data.values[:,1]==8))
    Sep_drift_index = np.where(np.logical_and(np.logical_and(data.values[:,2]<=14,data.values[:,1]==9),data.values[:,3]<=22))
    drift_index = range(Aug_drift_index[0][0],Sep_drift_index[0][-1])

    print '******'
    print ''
    # print 'Aug drift: ' + str(data.values[Aug_drift_index[0][0],0:3]) + ' - ' + str(data.values[Aug_drift_index[0][-1],0:3])
    # print 'Sep drift: ' + str(data.values[Sep_drift_index[0][0],0:3]) + ' - ' + str(data.values[Sep_drift_index[0][-1],0:3])
    print 'Whole drift: ' + str(data.values[drift_index[0],0:4]) + ' - ' + str(data.values[drift_index[-1],0:4])
    print ''

    return drift_index

def inIce(data):

    ###################################
    ## DEFINE IN ICE PERIOD
    ###################################
    Aug_inIce = np.where(np.logical_and(data.values[:,2]>=3,data.values[:,1]==8))
    Sep_inIce = np.where(np.logical_and(data.values[:,2]<20,data.values[:,1]==9))
    inIce_index = np.arange(Aug_inIce[0][0],Sep_inIce[0][-1])

    ###################################
    ## DEFINE METUM PERIOD (CLOUDNET COMPARISON)
    ###################################
    # Aug_inIce = np.where(np.logical_and(np.logical_and(data.values[:,2]>=12,data.values[:,1]==8),data.values[:,3]>=0))
    # # Sep_inIce = np.where(np.logical_and(np.logical_and(data.values[:,2]>=13,data.values[:,1]==8),data.values[:,3]>=0))
    # # Sep_inIce = np.where(np.logical_and(data.values[:,2]<=20,data.values[:,1]==9))
    # # Sep_inIce = np.where(np.logical_and(np.logical_and(data.values[:,2]<=20,data.values[:,1]==9),data.values[:,3]<=1))
    # inIce_index = range(Aug_inIce[0][0],Sep_inIce[0][-1])

    print '******'
    print ''
    # print 'Aug drift: ' + str(data.values[Aug_inIce[0][0],0:3]) + ' - ' + str(data.values[Aug_inIce[0][-1],0:3])
    # print 'Sep drift: ' + str(data.values[Sep_inIce[0][0],0:3]) + ' - ' + str(data.values[Sep_inIce[0][-1],0:3])
    # print 'In ice: ' + str(data.values[inIce_index[0],0:4]) + ' - ' + str(data.values[inIce_index[-1],0:4])
    print 'CloudNET: ' + str(data.values[inIce_index[0],0:4]) + ' - ' + str(data.values[inIce_index[-1],0:4])
    print ''
    print 'Mean lon/lat of ship track: (' + str(np.nanmedian(data.values[inIce_index,6])) + ', ' + str(np.nanmedian(data.values[inIce_index,7])) + ')'
    print 'Lon/lat of start point: (' + str(data.values[inIce_index[0],6]) + ', ' + str(data.values[inIce_index[0],7]) + ')'
    print 'Lon/lat of end point: (' + str(data.values[inIce_index[-1],6]) + ', ' + str(data.values[inIce_index[-1],7]) + ')'
    print 'Min/max longitude: ' + str(np.nanmin(data.values[inIce_index,6])) + ', ' + str(np.nanmax(data.values[inIce_index,6]))
    print 'Min/max latitude: ' + str(np.nanmin(data.values[inIce_index,7])) + ', ' + str(np.nanmax(data.values[inIce_index,7]))
    print ''

    return inIce_index

def trackShip(data, date):
    ###################################
    ## DEFINE METUM PERIOD (CLOUDNET COMPARISON)
    ###################################
    trackShip_start = np.where(np.logical_and(np.logical_and(data.values[:,2]==14,data.values[:,1]==8),data.values[:,3]>=0))
    trackShip_end = np.where(np.logical_and(np.logical_and(data.values[:,2]==25,data.values[:,1]==8),data.values[:,3]==1))
    # trackShip_start = np.where(np.logical_and(np.logical_and(data.values[:,2]==int(date[-2:]),data.values[:,1]==int(date[-4:-2])),data.values[:,3]>=0))
    # trackShip_end = np.where(np.logical_and(np.logical_and(data.values[:,2]==(int(date[-2:]) + 1),data.values[:,1]==int(date[-4:-2])),data.values[:,3]==1))
    trackShip_index = range(trackShip_start[0][0],trackShip_end[0][-1])

    print '******'
    print ''
    # print 'Mean lon/lat of ship track: (' + str(np.nanmedian(data.values[inIce_index,6])) + ', ' + str(np.nanmedian(data.values[inIce_index,7])) + ')'
    print 'Lon/lat of start point: (' + str(data.values[trackShip_index[0],6]) + ', ' + str(data.values[trackShip_index[0],7]) + ')'
    print 'Lon/lat of end point: (' + str(data.values[trackShip_index[-1],6]) + ', ' + str(data.values[trackShip_index[-1],7]) + ')'
    # print 'Start: ' + str(data.values[trackShip_start[0][0],0:4])
    # print 'End: ' + str(data.values[trackShip_end[0][-1],0:4])
    print 'trackShip: ' + str(data.values[trackShip_index[0],0:4]) + ' - ' + str(data.values[trackShip_index[-1],0:4])
    print ''

    return trackShip_index

def combineNC(nc1, nc2, filename1, filename2):

    '''
    Load in two netCDF files at a time, then join to make nc1 25h long
    for compatibility with Cloudnet
    '''

    #################################################################
    ## MAKE BESPOKE LIST FOR DIAGS WITH RADIATION TIMESTEPS
    #################################################################
    radlist = ['surface_net_SW_radiation','surface_net_LW_radiation','IWP','LWP']

    #################################################################
    ## CREATE NEW NETCDF
    #################################################################
    nc = Dataset(filename1[-22:-3] + '_25h.nc', 'w', format ='NETCDF4_CLASSIC')
    print ''
    print nc.file_format
    print ''

    ###################################
    ## Data dimensions
    ###################################
    forecast_time = nc.createDimension('forecast_time', 25)
    height = nc.createDimension('height', np.size(nc1.variables['height']))

    ###################################
    ## Dimensions variables
    ###################################
    #### forecast_period
    timem = nc.createVariable('forecast_time', np.float64, ('forecast_time',), fill_value='-9999')
    timem.scale_factor = float(1)
    timem.add_offset = float(0)
    timem.comment = 'Hours since 0000 UTC.'
    timem.units = 'hours'
    timem.long_name = 'forecast_time'
    timem[0:24] = nc1.variables['forecast_time'][0:]
    timem[24] = 24.0    ### hard code since nc2[0] = 0.0
    print 'time shape = ' + str(timem.shape)

    #### height
    height = nc.createVariable('height', np.float64, ('height',), fill_value='-9999')
    height.scale_factor = float(1)
    height.add_offset = float(0)
    height.comment = ''
    height.units = 'm'
    height.long_name = 'height'
    height[:] = nc1.variables['height'][:]      ### forecast time (ignore first 12h)

    ###################################
    ## Create DIAGNOSTICS
    ###################################
    ###################################
    ## Write pbXXX stream diagnostics
    ###################################
    for diag in nc1.variables:
    # diag = 'sfc_pressure'
    # if diag == 'sfc_pressure':
        print 'Writing ' + diag
        print ''
        ### 1Dimension
        if np.size(np.shape(nc1.variables[diag])) == 1:
            if diag == 'forecast_time':
                print 'Diagnostic is forecast_time which is already defined... skipping.'
                continue
            if diag == 'height':
                print 'Diagnostic is height which is already defined... skipping.'
                continue
            if diag in radlist:
                dat = nc.createVariable(diag, np.float64, ('forecast_time',), fill_value='-9999')
                dat.scale_factor = float(1)
                dat.add_offset = float(0)
                if 'units' in nc1.variables[diag].ncattrs(): dat.units = nc1.variables[diag].units
                if 'STASH' in nc1.variables[diag].ncattrs(): dat.um_stash_source = nc1.variables[diag].STASH
                if 'um_stash_source' in nc1.variables[diag].ncattrs(): dat.um_stash_source = nc1.variables[diag].um_stash_source
                if 'standard_name' in nc1.variables[diag].ncattrs(): dat.standard_name = nc1.variables[diag].standard_name
                if 'long_name' in nc1.variables[diag].ncattrs(): dat.long_name = nc1.variables[diag].long_name
                dat[0:23] = nc1.variables[diag][0:-1]
                dat[23:25] = nc2.variables[diag][0:2]
            else:
                dat = nc.createVariable(diag, np.float64, ('forecast_time',), fill_value='-9999')
                dat.scale_factor = float(1)
                dat.add_offset = float(0)
                if 'units' in nc1.variables[diag].ncattrs(): dat.units = nc1.variables[diag].units
                if 'STASH' in nc1.variables[diag].ncattrs(): dat.um_stash_source = nc1.variables[diag].STASH
                if 'um_stash_source' in nc1.variables[diag].ncattrs(): dat.um_stash_source = nc1.variables[diag].um_stash_source
                if 'standard_name' in nc1.variables[diag].ncattrs(): dat.standard_name = nc1.variables[diag].standard_name
                if 'long_name' in nc1.variables[diag].ncattrs(): dat.long_name = nc1.variables[diag].long_name
                dat[0:24] = nc1.variables[diag][0:]
                dat[24] = nc2.variables[diag][0]

        ### 2Dimensions
        elif np.size(np.shape(nc1.variables[diag])) == 2:
            dat = nc.createVariable(diag, np.float64, ('forecast_time','height',), fill_value='-9999')
            dat.scale_factor = float(1)
            dat.add_offset = float(0)
            if 'units' in nc1.variables[diag].ncattrs(): dat.units = nc1.variables[diag].units
            if 'STASH' in nc1.variables[diag].ncattrs(): dat.um_stash_source = nc1.variables[diag].STASH
            if 'um_stash_source' in nc1.variables[diag].ncattrs(): dat.um_stash_source = nc1.variables[diag].um_stash_source
            if 'standard_name' in nc1.variables[diag].ncattrs(): dat.standard_name = nc1.variables[diag].standard_name
            if 'long_name' in nc1.variables[diag].ncattrs(): dat.long_name = nc1.variables[diag].long_name
            dat[0:24,:] = nc1.variables[diag][0:,:]
            dat[24,:] = nc2.variables[diag][0,:]

        ### 0Dimensions
        else:
            if diag == 'horizontal_resolution':
                print 'Diagnostic is horizontal_resolution which needs to be defined separately...'
                dat = nc.createVariable('horizontal_resolution', np.float32, fill_value='-9999')
                dat.comment = 'Horizontal grid size of nested region.'
                dat.units = 'km'
                dat[:] = 1.5
                continue

    ###################################
    ## Add Global Attributes
    ###################################
    nc.conventions = nc1.Conventions
    nc.title = nc1.title
    nc.description = nc1.description
    nc.history = nc1.history
    nc.source = nc1.source
    nc.references = nc1.references
    nc.project = nc1.project
    nc.comment = nc1.comment
    nc.institution = nc1.institution
    nc.initialization_time = nc1.initialization_time
    nc.um_version = nc1.um_version

    nc.close()

def callback(cube, field, filename):
    '''
    rename cube diagnostics per list of wanted stash diags
    '''

    iStash = cube.attributes['STASH'].__str__()
    if diags.findfieldName(iStash):
        if cube.name() != diags.findfieldName(iStash):
            cube.rename(diags.findfieldName(iStash))

def makeGlobalStashList():
    '''
    make a list of all the stash code we want to load
    '''

    GlobalStashList = diags.returnWantedStash()

    # print GlobalStashList
    # print GlobalStashList[0]

    return GlobalStashList

def main():

    START_TIME = time.time()
    print '******'
    print ''
    print 'Start: ' + time.strftime("%c")
    print ''

    ### CHOOSE PLATFORM (OPTIONS BELOW)
    platform = 'LAPTOP'

    ### JASMIN
    ### LAPTOP
    ### MONSOON
    ### DESKTOP

    if platform == 'JASMIN':
        root_dir = '/gws/nopw/j04/ncas_weather/gyoung/MOCCHA/UM/'
        ship_filename = '~/GWS/MOCCHA/ODEN/2018_shipposition_1hour.txt'
    if platform == 'LAPTOP':
        root_dir = '/home/gillian/MOCCHA/UM/DATA/'
        obs_root_dir = '/home/gillian/MOCCHA/ODEN/'
        ship_filename = '~/MOCCHA/ODEN/DATA/2018_shipposition_1hour.txt'
    if platform == 'MONSOON':
        root_dir = '~/cylc-run/u-bg610/share/cycle/20160401T0000Z/HighArctic/1p5km/RA2M_CON/um/'
    if platform == 'DESKTOP':
        root_dir = '/nfs/a96/MOCCHA/working/gillian/UM/DATA/'
        ship_filename = '/nfs/a96/MOCCHA/working/gillian/ship/2018_shipposition_1hour.txt'
        position_filename = 'AUX_DATA/POSITION_UNROTATED.csv'

    ### CHOSEN RUN
    out_dir = '4_u-bg610_RA2M_CON/OUT_R1/papbpc_combined/'
    out_dir3 = 'MET_DATA/'

    ### TESTING/domain_tests/umnsaa_pa000
    ### 4_u-bg610_RA2M_CON/OUT_R1/papbpc_combined/
    ### 5_u-bl661_RA1M_CASIM/OUT/
    ### 6_u-bm410_RA1M_CASIM/OUT/

    print '******'
    print ''
    print 'Identifying .nc file: '
    print ''

    # -------------------------------------------------------------
    # Load ship track
    # -------------------------------------------------------------
    print '******'
    print ''
    print 'Load in ship track file:'
    print ''
    ship_data = readfile(ship_filename)
    columns = assignColumns(ship_data)

    # -------------------------------------------------------------
    # Load observations
    # -------------------------------------------------------------
    print 'Loading observations:'
    filename_obs = obs_root_dir + out_dir3 + 'MetData_Gillian_wTemp1p5m.nc'
    cube_obs = iris.load(filename_obs)#, global_con, callback)
    print '...'

    # -------------------------------------------------------------------------
    # make global stash list and constraint
    # -------------------------------------------------------------------------
    print '******'
    print ''
    print 'Make stash list for cube read in at ' + time.strftime("%c")
    print ' '
    GlobalStashList = makeGlobalStashList()
    global_con = iris.AttributeConstraint(
        STASH=lambda stash: str(stash) in GlobalStashList)
            ### defines which stash variables to load - should be within a loop

    # # -------------------------------------------------------------
    # # Load cube
    # # -------------------------------------------------------------
    print '******'
    print ''
    print 'Begin cube read in at ' + time.strftime("%c")
    print ' '

    ### -------------------------------------------------------------------------
    ### define input filename
    ### -------------------------------------------------------------------------
    # tempnames = ['umnsaa_pa012_r0.nc','umnsaa_pb012_r0.nc','umnsaa_pc011_r0.nc','umnsaa_pd011_r0.nc','20180812_oden_metum.nc']
    Aug_names = ['20180813_oden_metum.nc','20180814_oden_metum.nc','20180815_oden_metum.nc','20180816_oden_metum.nc',
            '20180817_oden_metum.nc','20180818_oden_metum.nc','20180819_oden_metum.nc','20180820_oden_metum.nc',
            '20180821_oden_metum.nc','20180822_oden_metum.nc','20180823_oden_metum.nc','20180824_oden_metum.nc',
            '20180825_oden_metum.nc','20180826_oden_metum.nc','20180827_oden_metum.nc','20180828_oden_metum.nc',
            '20180829_oden_metum.nc','20180830_oden_metum.nc','20180831_oden_metum.nc']

    Sep_names = ['20180901_oden_metum.nc','20180902_oden_metum.nc','20180903_oden_metum.nc','20180904_oden_metum.nc',
            '20180905_oden_metum.nc','20180906_oden_metum.nc','20180907_oden_metum.nc','20180908_oden_metum.nc',
            '20180909_oden_metum.nc','20180910_oden_metum.nc','20180911_oden_metum.nc','20180912_oden_metum.nc',
            '20180913_oden_metum.nc','20180914_oden_metum.nc']

    moccha_names = ['20180813_oden_metum.nc','20180814_oden_metum.nc','20180815_oden_metum.nc','20180816_oden_metum.nc',
            '20180817_oden_metum.nc','20180818_oden_metum.nc','20180819_oden_metum.nc','20180820_oden_metum.nc',
            '20180821_oden_metum.nc','20180822_oden_metum.nc','20180823_oden_metum.nc','20180824_oden_metum.nc',
            '20180825_oden_metum.nc','20180826_oden_metum.nc','20180827_oden_metum.nc','20180828_oden_metum.nc',
            '20180829_oden_metum.nc','20180830_oden_metum.nc','20180831_oden_metum.nc','20180901_oden_metum.nc',
            '20180902_oden_metum.nc','20180903_oden_metum.nc','20180904_oden_metum.nc','20180905_oden_metum.nc',
            '20180906_oden_metum.nc','20180907_oden_metum.nc','20180908_oden_metum.nc','20180909_oden_metum.nc',
            '20180910_oden_metum.nc','20180911_oden_metum.nc','20180912_oden_metum.nc','20180913_oden_metum.nc',
            '20180914_oden_metum.nc']

    Aug_missing_files = ['20180812_oden_metum.nc']

    Sep_missing_files = []

    moccha_missing_files = []

    doy = np.arange(225,258)        ## set DOY for full moccha figures

    # names = ['umnsaa_pa000','umnsaa_pc000.nc']       ### DEFAULT OUTPUT NAMES FOR TESTING

    ## Choose month:
    names = moccha_names
    missing_files = moccha_missing_files
    month_flag = -1

    # i = 0
    for i in range(0,len(moccha_names) - 1):
        filename1 = root_dir + out_dir + names[i]
        filename2 = root_dir + out_dir + names[i+1]
        print filename1
        print filename2
        print ''

        #### -------------------------------------------------------------
        #### LOAD CUBES
        #### -------------------------------------------------------------
        # cube1 = iris.load(filename1)
        nc1 = Dataset(filename1,'r')
        print nc1
        print ''

        # cube2 = iris.load(filename1)
        nc2 = Dataset(filename2,'r')
        print nc2
        print ''

        # out = combineCubes(cube1, cube2)
        out = combineNC(nc1, nc2, filename1, filename2)
        nc1.close()
        nc2.close()


    # -------------------------------------------------------------
    # FIN.
    # -------------------------------------------------------------
    END_TIME = time.time()
    print '******'
    print ''
    print 'End: ' + time.strftime("%c")
    print ''

    #### DIAGNOSTICS TO CHOOSE FROM:

    ### paXXX
    # 0: northward_wind_at_10m / (m s-1)     (time: 8; grid_latitude: 501; grid_longitude: 500)
    # 1: eastward_wind_at_10m / (m s-1)      (time: 8; grid_latitude: 501; grid_longitude: 500)
    # 2: surface_downwelling_SW_radiation / (W m-2) (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 3: surface_net_LW_radiation / (W m-2)  (time: 8; grid_latitude: 500; grid_longitude: 500)
    # 4: surface_net_SW_radiation / (W m-2)  (time: 8; grid_latitude: 500; grid_longitude: 500)
    # 5: relative_humidity_at_1.5m / (%)     (time: 8; grid_latitude: 500; grid_longitude: 500)
    # 6: surface_downwelling_LW_radiation / (W m-2) (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 7: specific_humidity_at_1.5m / (1)     (time: 8; grid_latitude: 500; grid_longitude: 500)
    # 8: surface_net_SW_radiation / (W m-2)  (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 9: air_temperature_at_1.5m / (K)       (time: 8; grid_latitude: 500; grid_longitude: 500)
    # 10: dew_point_temperature_at_1.5m / (K) (time: 8; grid_latitude: 500; grid_longitude: 500)
    # 11: surface_net_LW_radiation / (W m-2)  (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 12: air_pressure_at_sea_level / (Pa)    (time: 8; grid_latitude: 500; grid_longitude: 500)
    # 13: surface_air_pressure / (Pa)         (time: 8; grid_latitude: 500; grid_longitude: 500)
    # 14: surface_temperature / (K)           (time: 8; grid_latitude: 500; grid_longitude: 500)
    # 15: toa_incoming_shortwave_flux / (W m-2) (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 16: toa_outgoing_longwave_flux / (W m-2) (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 17: toa_outgoing_shortwave_flux / (W m-2) (time: 24; grid_latitude: 94; grid_longitude: 95)

    #### 12 AUG ONLY - NO FULL NEST DIAGNOSTICS
    # <iris 'Cube' of surface_downwelling_longwave_flux_in_air / (W m-2) (time: 24; grid_latitude: 25; grid_longitude: 25)>,
    # <iris 'Cube' of surface_downwelling_shortwave_flux_in_air / (W m-2) (time: 24; grid_latitude: 25; grid_longitude: 25)>,
    # <iris 'Cube' of surface_net_downward_longwave_flux / (W m-2) (time: 24; grid_latitude: 25; grid_longitude: 25)>,
    # <iris 'Cube' of surface_net_downward_shortwave_flux / (W m-2) (time: 24; grid_latitude: 25; grid_longitude: 25)>,
    # <iris 'Cube' of toa_incoming_shortwave_flux / (W m-2) (time: 24; grid_latitude: 25; grid_longitude: 25)>,
    # <iris 'Cube' of toa_outgoing_shortwave_flux / (W m-2) (time: 24; grid_latitude: 25; grid_longitude: 25)>]

    ### pbXXX
    # 0: specific_humidity_at_1.5m / (1)     (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 1: cloud_area_fraction_assuming_maximum_random_overlap / (1) (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 2: cloud_area_fraction_assuming_random_overlap / (1) (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 3: air_temperature_at_1.5m / (K)       (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 4: northward_wind_at_10m / (m s-1)     (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 5: eastward_wind_at_10m / (m s-1)      (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 6: height_of_stratocumulus_cloud_base / (1) (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 7: dew_point_temperature_at_1.5m / (K) (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 8: total_column_q / (1)                (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 9: turbulent mixing height after boundary layer / (m) (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 10: height_of_decoupled_layer_base / (1) (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 11: combined_boundary_layer_type / (1)  (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 12: wet_bulb_freezing_level_altitude / (m) (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 13: relative_humidity_at_1.5m / (%)     (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 14: large_scale_ice_water_path / (1)    (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 15: large_scale_liquid_water_path / (1) (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 16: air_pressure_at_sea_level / (Pa)    (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 17: atmosphere_boundary_layer_thickness / (m) (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 18: high_type_cloud_area_fraction / (1) (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 19: low_type_cloud_area_fraction / (1)  (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 20: medium_type_cloud_area_fraction / (1) (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 21: stratiform_rainfall_flux / (kg m-2 s-1) (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 22: stratiform_snowfall_flux / (kg m-2 s-1) (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 23: surface_air_pressure / (Pa)         (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 24: surface_temperature / (K)           (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 25: surface_upward_latent_heat_flux / (W m-2) (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 26: surface_upward_sensible_heat_flux / (W m-2) (time: 24; grid_latitude: 94; grid_longitude: 95)
    # 27: water_evaporation_amount / (1)      (time: 24; grid_latitude: 94; grid_longitude: 95)


    ### pcXXX
    # 0: total_radar_reflectivity / (unknown) (model_level_number: 70; grid_latitude: 25; grid_longitude: 25)
    # 1: air_pressure / (Pa)                 (model_level_number: 70; grid_latitude: 25; grid_longitude: 25)
    # 2: air_temperature / (K)               (model_level_number: 70; grid_latitude: 25; grid_longitude: 25)
    # 3: eastward_wind / (m s-1)             (model_level_number: 70; grid_latitude: 25; grid_longitude: 25)
    # 4: large_scale_cloud_area_fraction / (1) (model_level_number: 70; grid_latitude: 25; grid_longitude: 25)
    # 5: mass_fraction_of_cloud_ice_in_air / (kg kg-1) (model_level_number: 70; grid_latitude: 25; grid_longitude: 25)
    # 6: mass_fraction_of_cloud_liquid_water_in_air / (kg kg-1) (model_level_number: 70; grid_latitude: 25; grid_longitude: 25)
    # 7: northward_wind / (m s-1)            (model_level_number: 70; grid_latitude: 25; grid_longitude: 25)
    # 8: specific_humidity / (kg kg-1)       (model_level_number: 70; grid_latitude: 25; grid_longitude: 25)
    # 9: upward_air_velocity / (m s-1)       (model_level_number: 70; grid_latitude: 25; grid_longitude: 25)


    ### pdXXX
    # 0: entrainment_rate_for_surface_mixed_layer / (unknown) (grid_latitude: 25; grid_longitude: 25)
    # 1: entrainment_rate_for_boundary_layer / (unknown) (grid_latitude: 25; grid_longitude: 25)
    # 2: obukhov_length / (unknown)          (grid_latitude: 25; grid_longitude: 25)
    # 3: atmosphere_downward_eastward_stress / (Pa) (model_level_number: 69; grid_latitude: 25; grid_longitude: 25)
    # 4: atmosphere_downward_northward_stress / (Pa) (model_level_number: 69; grid_latitude: 25; grid_longitude: 25)
    # 5: turbulent_kinetic_energy / (unknown) (model_level_number: 69; grid_latitude: 25; grid_longitude: 25)
    # 6: air_pressure / (Pa)                 (model_level_number: 70; grid_latitude: 25; grid_longitude: 25)
    # 7: surface_downward_eastward_stress / (Pa) (grid_latitude: 25; grid_longitude: 25)
    # 8: surface_downward_northward_stress / (Pa) (grid_latitude: 25; grid_longitude: 25)
    # 9: surface_upward_water_flux / (kg m-2 s-1) (grid_latitude: 25; grid_longitude: 25)

if __name__ == '__main__':

    main()
