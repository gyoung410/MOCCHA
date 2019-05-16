###
###
### SCRIPT TO READ IN UM MODEL DATA IN NETCDF FORMAT AS IRIS CUBE
###
###


import time
import datetime
import numpy as np
from netCDF4 import Dataset
import numpy as np
import diags_MOCCHA as diags
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
    # Aug_inIce = np.where(np.logical_and(data.values[:,2]>=3,data.values[:,1]==8))
    # Sep_inIce = np.where(np.logical_and(data.values[:,2]<=20,data.values[:,1]==9))
    # inIce_index = np.arange(Aug_inIce[0][0],Sep_inIce[0][-1])

    ###################################
    ## DEFINE METUM PERIOD (CLOUDNET COMPARISON)
    ###################################
    Aug_inIce = np.where(np.logical_and(data.values[:,2]>=12,data.values[:,1]==8))
    # Sep_inIce = np.where(np.logical_and(data.values[:,2]<=20,data.values[:,1]==9))
    Sep_inIce = np.where(np.logical_and(np.logical_and(data.values[:,2]<=20,data.values[:,1]==9),data.values[:,3]<=1))
    inIce_index = range(Aug_inIce[0][0],Sep_inIce[0][-1])

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

def plot_cartmap(ship_data, cube, hour, lon, lat):

    import iris.plot as iplt
    import iris.quickplot as qplt
    import iris.analysis.cartography
    import cartopy.crs as ccrs
    import cartopy
        # from matplotlib.patches import Polygon

    ###################################
    ## PLOT MAP
    ###################################

    print '******'
    print ''
    print 'Plotting cartopy map:'
    print ''

    ##################################################
    ##################################################
    #### 	CARTOPY
    ##################################################
    ##################################################

    SMALL_SIZE = 12
    MED_SIZE = 14
    LARGE_SIZE = 16

    plt.rc('font',size=MED_SIZE)
    plt.rc('axes',titlesize=MED_SIZE)
    plt.rc('axes',labelsize=MED_SIZE)
    plt.rc('xtick',labelsize=SMALL_SIZE)
    plt.rc('ytick',labelsize=SMALL_SIZE)
    plt.rc('legend',fontsize=SMALL_SIZE)
    # plt.rc('figure',titlesize=LARGE_SIZE)

    #################################################################
    ## create figure and axes instances
    #################################################################
    plt.figure(figsize=(5,4))
    # ax = plt.axes(projection=ccrs.Orthographic(0, 90))    # NP Stereo
    ax = plt.axes(projection=ccrs.NorthPolarStereo(central_longitude=30))

    ### set size
    # ax.set_extent([0, 60, 87.75, 90], crs=ccrs.PlateCarree())
    ax.set_extent([-180, 190, 80, 90], crs=ccrs.PlateCarree())

    ### DON'T USE PLATECARREE, NORTHPOLARSTEREO (on it's own), LAMBERT

    #################################################################
    ## add geographic features/guides for reference
    #################################################################
    ax.add_feature(cartopy.feature.OCEAN, zorder=0)
    ax.add_feature(cartopy.feature.LAND, zorder=0, edgecolor='black')
    # ax.set_global()
    ax.gridlines()

    #################################################################
    ## plot UM data
    #################################################################
    if np.size(cube.shape) == 4:
        iplt.pcolormesh(cube[hour,0,:,:])
    elif np.size(cube.shape) == 3:
        iplt.pcolormesh(cube[hour,:,:])
    elif np.size(cube.shape) == 2:
        iplt.pcolormesh(cube[:,:])
    # if cube.units in locals():
    plt.title(cube.standard_name + ', ' + str(cube.units))
    # else:
    #     plt.title(cube.standard_name)
    plt.colorbar()

    #################################################################
    ## plot ship track
    #################################################################
    ### DEFINE DRIFT + IN_ICE PERIODS
    drift_index = iceDrift(ship_data)
    inIce_index = inIce(ship_data)

    ### Plot tracks as line plot
    # plt.plot(ship_data.values[:,6], ship_data.values[:,7],
    #          color = 'yellow', linewidth = 2,
    #          transform = ccrs.PlateCarree(), label = 'Whole',
    #          )
    plt.plot(ship_data.values[inIce_index,6], ship_data.values[inIce_index,7],
             color = 'darkorange', linewidth = 3,
             transform = ccrs.PlateCarree(), label = 'In Ice',
             )
    plt.plot(ship_data.values[inIce_index[0],6], ship_data.values[inIce_index[0],7],
             'k^', markerfacecolor = 'darkorange', linewidth = 3,
             transform = ccrs.PlateCarree(),
             )
    plt.plot(ship_data.values[inIce_index[-1],6], ship_data.values[inIce_index[-1],7],
             'kv', markerfacecolor = 'darkorange', linewidth = 3,
             transform = ccrs.PlateCarree(),
             )
    plt.plot(ship_data.values[drift_index,6], ship_data.values[drift_index,7],
             color = 'red', linewidth = 4,
             transform = ccrs.PlateCarree(), label = 'Drift',
             )

    plt.plot(np.nanmin(lon),np.nanmin(lat),'ks')
    plt.plot(np.nanmin(lon),np.nanmax(lat),'ks')
    plt.plot(np.nanmax(lon),np.nanmin(lat),'ks')
    plt.plot(np.nanmax(lon),np.nanmax(lat),'ks')

    plt.legend()

    print '******'
    print ''
    print 'Finished plotting cartopy map! :)'
    print ''

    # plt.savefig('FIGS/Test_AirTemperature_t12_wShipTrack.png', dpi=200)
    plt.show()

def unrotateGrid(cube):
    ##
    ##      ROTATE GRID BACK TO STANDARD
    ##

    import iris.analysis.cartography as ircrt
    import pandas as pd

    ### LAM Configuration from suite u-bg610
    dlat = 0.015714
    dlon = 0.016334
    frst_lat = -5.6112
    frst_lon = 353.0345
    pole_lat = 3.375 # UM SUITE: 37.5000
    pole_lon = 210.0 # UM SUITE: 177.5000

    rot_lat = cube.coord('grid_latitude').points
    rot_lon = cube.coord('grid_longitude').points

    rot_pole = cube.coord('grid_latitude').coord_system.as_cartopy_crs()

    lon, lat = ircrt.unrotate_pole(rot_lon, rot_lat, pole_lon, pole_lat)

    # Print to check conversion
    print '******'
    print 'Test of unrotated coordinate grid: '
    print 'Rotated lon coord = ', rot_lon[250]
    print 'Rotated lat coord = ', rot_lat[250]
    print 'Lon = ', lon[250]
    print 'Lat = ', lat[250]
    print ' '

    # ******
    # write to csv file
    # ******

    # print '******'
    # print 'Writing unrotated coordinate grid to file:'
    # print ''
    # lonp = pd.DataFrame(lon)
    # latp = pd.DataFrame(lat)
    # dat = {'Latitude': lat, 'Longitude': lon}
    # df = pd.DataFrame(dat,columns=['Latitude','Longitude'])
    # df.to_csv('POSITION_UNROTATED.csv',  sep = " ")
    # print '... finished!'
    # print ''
    # print '******'

    return lon, lat

def main():

    START_TIME = time.time()
    print '******'
    print ''
    print 'Start: ' + time.strftime("%c")
    print ''

    ### CHOOSE PLATFORM (OPTIONS BELOW)
    platform = 'JASMIN'

    ### JASMIN
    ### LAPTOP
    ### MONSOON
    ### DESKTOP

    if platform == 'JASMIN':
        root_dir = '/gws/nopw/j04/ncas_weather/gyoung/MOCCHA/UM/'
        ship_filename = '~/GWS/MOCCHA/ODEN/2018_shipposition_1hour.txt'
        position_filename = 'POSITION_UNROTATED.csv'
    if platform == 'LAPTOP':
        root_dir = '~/MOCCHA/UM/DATA/'
        ship_filename = '~/MOCCHA/ODEN/DATA/2018_shipposition_1hour.txt'
    if platform == 'MONSOON':
        root_dir = '~/cylc-run/u-bg610/share/cycle/20160401T0000Z/HighArctic/1p5km/RA2M_CON/um/'
    if platform == 'DESKTOP':
        root_dir = '/nfs/a96/MOCCHA/working/gillian/UM/DATA/'
        ship_filename = '/nfs/a96/MOCCHA/working/gillian/ship/2018_shipposition_1hour.txt'
    position_filename = 'AUX_DATA/POSITION_UNROTATED.csv'

    ### CHOSEN RUN
    out_dir = '2_20180801_61DIAGS_TEST/2_30_86.625/'

    ## 1_20160401_61DIAG_TEST/
    ## 2_20180801_61DIAGS_TEST


    # -------------------------------------------------------------
    # Load ship track
    # -------------------------------------------------------------
    print '******'
    print ''
    print 'Load in ship track file:'
    print ''
    ship_data = readfile(ship_filename)
    columns = assignColumns(ship_data)

    print '******'
    print ''
    print 'Identifying .nc file: '
    print ''

    ### -------------------------------------------------------------------------
    ### define input filename
    ### -------------------------------------------------------------------------
    filename1 = root_dir + out_dir + 'umnsaa_pa012_r0.nc'
    print filename1
    print ''

    # # -------------------------------------------------------------
    # # Load cube
    # # -------------------------------------------------------------
    print '******'
    print ''
    print 'Begin cube read in at ' + time.strftime("%c")
    print ' '
    var = 'surface_net_downward_shortwave_flux'
    cube = iris.load_cube(filename1, var)
    # data = Dataset(filename1,'r')

    print cube
    print ''

    ### paXXX
    # <iris 'Cube' of air_pressure_at_sea_level / (Pa) (time: 8; grid_latitude: 500; grid_longitude: 500)>,
    # <iris 'Cube' of air_temperature / (K) (time: 8; grid_latitude: 500; grid_longitude: 500)>,
    # <iris 'Cube' of dew_point_temperature / (K) (time: 8; grid_latitude: 500; grid_longitude: 500)>,
    # <iris 'Cube' of relative_humidity / (%) (time: 8; grid_latitude: 500; grid_longitude: 500)>,
    # <iris 'Cube' of specific_humidity / (1) (time: 8; grid_latitude: 500; grid_longitude: 500)>,
    # <iris 'Cube' of surface_air_pressure / (Pa) (time: 8; grid_latitude: 500; grid_longitude: 500)>,
    # <iris 'Cube' of surface_downwelling_longwave_flux_in_air / (W m-2) (time: 8; grid_latitude: 500; grid_longitude: 500)>,
    # <iris 'Cube' of surface_downwelling_shortwave_flux_in_air / (W m-2) (time: 8; grid_latitude: 500; grid_longitude: 500)>,
    # <iris 'Cube' of surface_net_downward_longwave_flux / (W m-2) (time: 8; grid_latitude: 500; grid_longitude: 500)>,
    # <iris 'Cube' of surface_net_downward_shortwave_flux / (W m-2) (time: 8; grid_latitude: 500; grid_longitude: 500)>,
    # <iris 'Cube' of surface_temperature / (K) (time: 8; grid_latitude: 500; grid_longitude: 500)>,
    # <iris 'Cube' of toa_incoming_shortwave_flux / (W m-2) (time: 8; grid_latitude: 500; grid_longitude: 500)>,
    # <iris 'Cube' of toa_outgoing_shortwave_flux / (W m-2) (time: 8; grid_latitude: 500; grid_longitude: 500)>,
    # <iris 'Cube' of x_wind / (m s-1) (time: 8; grid_latitude: 501; grid_longitude: 500)>,
    # <iris 'Cube' of y_wind / (m s-1) (time: 8; grid_latitude: 501; grid_longitude: 500)>]


    ### pbXXX
    # 0: Turbulent mixing height after boundary layer / (m) (time: 3; grid_latitude: 121; grid_longitude: 56)
    # 1: Stable boundary layer indicator / (1) (time: 3; grid_latitude: 121; grid_longitude: 56)
    # 2: Stratocumulus over stable boundary layer indicator / (1) (time: 3; grid_latitude: 121; grid_longitude: 56)
    # 3: Well-mixed boundary layer indicator / (1) (time: 3; grid_latitude: 121; grid_longitude: 56)
    # 4: Decoupled stratocumulus not over cumulus indicator / (1) (time: 3; grid_latitude: 121; grid_longitude: 56)
    # 5: Decoupled stratocumulus over cumulus indicator / (1) (time: 3; grid_latitude: 121; grid_longitude: 56)
    # 6: Cumulus capped boundary layer indicator / (1) (time: 3; grid_latitude: 121; grid_longitude: 56)
    # 7: Shear driven boundary layer indicator / (1) (time: 3; grid_latitude: 121; grid_longitude: 56)
    # 8: cloud_area_fraction_assuming_random_overlap / (1) (time: 3; grid_latitude: 121; grid_longitude: 56)
    # 9: cloud_area_fraction_assuming_maximum_random_overlap / (1) (time: 3; grid_latitude: 121; grid_longitude: 56)
    # 10: wet_bulb_freezing_level_altitude / (m) (time: 3; grid_latitude: 121; grid_longitude: 56)
    # 11: air_pressure_at_sea_level / (Pa)    (time: 3; grid_latitude: 121; grid_longitude: 56)
    # 12: atmosphere_boundary_layer_thickness / (m) (time: 3; grid_latitude: 121; grid_longitude: 56)
    # 13: high_type_cloud_area_fraction / (1) (time: 3; grid_latitude: 121; grid_longitude: 56)
    # 14: low_type_cloud_area_fraction / (1)  (time: 3; grid_latitude: 121; grid_longitude: 56)
    # 15: medium_type_cloud_area_fraction / (1) (time: 3; grid_latitude: 121; grid_longitude: 56)
    # 16: stratiform_rainfall_flux / (kg m-2 s-1) (time: 3; grid_latitude: 121; grid_longitude: 56)
    # 17: stratiform_snowfall_flux / (kg m-2 s-1) (time: 3; grid_latitude: 121; grid_longitude: 56)
    # 18: surface_upward_latent_heat_flux / (W m-2) (time: 3; grid_latitude: 121; grid_longitude: 56)
    # 19: surface_upward_sensible_heat_flux / (W m-2) (time: 3; grid_latitude: 121; grid_longitude: 56)
    # 20: water_evaporation_amount / (unknown) (time: 3; grid_latitude: 121; grid_longitude: 56)

    ### pcXXX
    # <iris 'Cube' of cloud_volume_fraction_in_atmosphere_layer / (1) (time: 25; model_level_number: 70; grid_latitude: 121; grid_longitude: 56)>,
    # <iris 'Cube' of m01s04i118 / (1) (time: 25; model_level_number: 70; grid_latitude: 121; grid_longitude: 56)>,
    # <iris 'Cube' of air_pressure / (Pa) (time: 25; model_level_number: 70; grid_latitude: 121; grid_longitude: 56)>,
    # <iris 'Cube' of air_temperature / (K) (time: 25; model_level_number: 70; grid_latitude: 121; grid_longitude: 56)>,
    # <iris 'Cube' of mass_fraction_of_cloud_ice_in_air / (kg kg-1) (time: 25; model_level_number: 70; grid_latitude: 121; grid_longitude: 56)>,
    # <iris 'Cube' of mass_fraction_of_cloud_liquid_water_in_air / (kg kg-1) (time: 25; model_level_number: 70; grid_latitude: 121; grid_longitude: 56)>,
    # <iris 'Cube' of specific_humidity / (kg kg-1) (time: 25; model_level_number: 70; grid_latitude: 121; grid_longitude: 56)>,
    # <iris 'Cube' of upward_air_velocity / (m s-1) (time: 25; model_level_number: 70; grid_latitude: 121; grid_longitude: 56)>,
    # <iris 'Cube' of x_wind / (m s-1) (time: 25; model_level_number: 70; grid_latitude: 121; grid_longitude: 56)>,
    # <iris 'Cube' of y_wind / (m s-1) (time: 25; model_level_number: 70; grid_latitude: 121; grid_longitude: 56)>]

    # FORECAST_PERIOD = cube1.aux_coords[1][:]

    # -------------------------------------------------------------
    # Define unrotated coordinate grid
    # -------------------------------------------------------------
    #### the following uses iris to unrotate the coordinate grid.
    ####    this only works with square domains (i.e. paXXX files)
    ####    only needs to be performed once -- saved grid as .csv file
    # lon, lat = unrotateGrid(cube)

    #### read in saved unrotated coordinate grid
    position_data = readfile(position_filename)
    lon = position_data.values[:,2]     ### unrotated longitude
    lat = position_data.values[:,1]     ### unrotated latitude
    lon, lat = np.meshgrid(lon,lat)     ### mesh for use with model diags

    # -------------------------------------------------------------
    # Plot data (map)
    # -------------------------------------------------------------
    ### select hour to plot
    hour = 0
    map = plot_cartmap(ship_data, cube, hour, lon, lat)

    END_TIME = time.time()
    print '******'
    print ''
    print 'End: ' + time.strftime("%c")
    print ''


if __name__ == '__main__':

    main()
