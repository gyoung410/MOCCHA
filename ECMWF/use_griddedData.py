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

def plot_cartmap(ship_data, cube, hour, date): #, lon, lat):

    import iris.plot as iplt
    import iris.quickplot as qplt
    import iris.analysis.cartography
    import cartopy.crs as ccrs
    import cartopy
    import matplotlib.path as mpath
        # from matplotlib.patches import Polygon

    ###---------------------------------
    ### DEFINE OFFSETS DEPENDENT ON NEST ROI
    ###---------------------------------
    print 'What grid are we looking at?'
    if len(cube[0].dim_coords[-1].points) == 25:
    # if cube[0,0].shape >= 25-1:    # ll = 240, 471
        xoffset = -239
        yoffset = -470
    elif len(cube[0].dim_coords[-1].points) == 56:
    # elif cube[0,0].shape >= 93-1:    # ll = 211, 386
        xoffset = -210
        yoffset = -385
    elif len(cube[0].dim_coords[-1].points) == 95:
    # elif cube[0,0].shape >= 93-1:    # ll = 211, 386
        xoffset = -210
        yoffset = -385
    else:
    # elif cube[0,0].shape >= 500-1:
        xoffset = 0
        yoffset = 0

    print 'Because cube shape = ', str(len(cube[0].dim_coords[-1].points))
    print 'xoffset = ', xoffset
    print 'yoffset = ', yoffset

    ###################################
    ## CHOOSE DIAGNOSTIC
    ###################################
    diag = 2
    print ''
    print 'Diag is: ', cube[diag].long_name
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
    plt.figure(figsize=(6,8))#, dpi=300)
    ax = plt.axes(projection=ccrs.Orthographic(30, 70))    # NP Stereo
    # ax = plt.axes(projection=ccrs.NorthPolarStereo(central_longitude=30))

    ### set size
    # ax.set_extent([30, 60, 89.1, 89.6], crs=ccrs.PlateCarree())       ### ZOOM
    # ax.set_extent([40, 50, 88.4, 88.6], crs=ccrs.PlateCarree())       ### ZOOM
    ax.set_extent([0, 60, 86.75, 90], crs=ccrs.PlateCarree())     ### SWATH
    # ax.set_extent([-180, 190, 80, 90], crs=ccrs.PlateCarree())    ### WHOLE
    # ax.set_extent([-180, 180, 70, 90], crs=ccrs.PlateCarree())    ### V LARGE
    # ax.set_extent([-180, 180, 60, 90], crs=ccrs.PlateCarree())    ### POSTER
    # ax.set_global()

    ### DON'T USE PLATECARREE, NORTHPOLARSTEREO (on it's own), LAMBERT

    #################################################################
    ## add geographic features/guides for reference
    #################################################################
    ax.add_feature(cartopy.feature.OCEAN, color='white', zorder=0)
    ax.add_feature(cartopy.feature.LAND, color='lightgrey', zorder=0, edgecolor='black')
    ax.add_feature(cartopy.feature.COASTLINE)
    # ax.set_global()
    ax.gridlines()

    # # Compute a circle in axes coordinates, which we can use as a boundary
    # # for the map. We can pan/zoom as much as we like - the boundary will be
    # # permanently circular.
    # theta = np.linspace(0, 2*np.pi, 100)
    # center, radius = [0.5, 0.5], 0.5
    # verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    # circle = mpath.Path(verts * radius + center)
    #
    # ax.set_boundary(circle, transform=ax.transAxes)

    #################################################################
    ## plot UM data
    ################################################################
    # if np.size(cube[diag].data.shape) == 4:
    #     iplt.pcolormesh(cube[diag][hour,0,:,:])
    # elif np.size(cube[diag].data.shape) == 3:
    #     iplt.pcolormesh(cube[diag][hour,:,:])
    #     # iplt.pcolormesh(cube[hour,471:495,240:264])
    # elif np.size(cube[diag].data.shape) == 2:
    iplt.pcolormesh(cube[diag][290:370,150:230])
    # # plt.title(cube[diag].standard_name + ', ' + str(cube[diag].units))
    # plt.colorbar()

    #################################################################
    ## plot UM nest
    #################################################################
    ### draw outline of grid
    # qplt.outline(cube[hour,380:500,230:285])          ### original swath
    # qplt.outline(cube[diag][hour,386:479,211:305])          ### redesigned swath (>13th)
    # qplt.outline(cube[hour,471:495,240:264])          ### 12-13th Aug swath
    # qplt.outline(cube[diag][hour,386:495,211:305])          ### misc
    # qplt.outline(cube[diag][290:370,150:230])



    # gridship = gridShipTrack(cube[diag], xoffset, yoffset)

            #### MID POINT: (433, 258)

    #################################################################
    ## plot ship track
    #################################################################
    ### DEFINE DRIFT + IN_ICE PERIODS
    drift_index = iceDrift(ship_data)
    inIce_index = inIce(ship_data)
    trackShip_index = trackShip(ship_data, date)

    ### Plot tracks as line plot
    plt.plot(ship_data.values[trackShip_index,6], ship_data.values[trackShip_index,7],
             color = 'darkorange', linewidth = 3,
             transform = ccrs.PlateCarree(), label = 'Ship track',
             )
    plt.plot(ship_data.values[trackShip_index[0],6], ship_data.values[trackShip_index[0],7],
             'k^', markerfacecolor = 'darkorange', linewidth = 3,
             transform = ccrs.PlateCarree(),
             )
    plt.plot(ship_data.values[trackShip_index[-1],6], ship_data.values[trackShip_index[-1],7],
             'kv', markerfacecolor = 'darkorange', linewidth = 3,
             transform = ccrs.PlateCarree(),
             )

    ### Plot full track as line plot
    # plt.plot(ship_data.values[:,6], ship_data.values[:,7], '--',
    #          color = 'pink', linewidth = 2,
    #          transform = ccrs.PlateCarree(), label = 'Whole',
    #          )
    # plt.plot(ship_data.values[inIce_index,6], ship_data.values[inIce_index,7],
    #          color = 'palevioletred', linewidth = 3,
    #          transform = ccrs.PlateCarree(), label = 'In Ice',
    #          )
    # plt.plot(ship_data.values[inIce_index[0],6], ship_data.values[inIce_index[0],7],
    #          'k^', markerfacecolor = 'palevioletred', linewidth = 3,
    #          transform = ccrs.PlateCarree(),
    #          )
    # plt.plot(ship_data.values[inIce_index[-1],6], ship_data.values[inIce_index[-1],7],
    #          'kv', markerfacecolor = 'palevioletred', linewidth = 3,
    #          transform = ccrs.PlateCarree(),
    #          )
    # plt.plot(ship_data.values[drift_index,6], ship_data.values[drift_index,7],
    #          color = 'red', linewidth = 4,
    #          transform = ccrs.PlateCarree(), label = 'Drift',
    #          )

    #### test plotting of unrotated grid
    # lon, lat = unrotateGrid(cube)

    # plt.plot(np.nanmin(lon),np.nanmin(lat),
    #         color='black',transform = ccrs.PlateCarree())
    # plt.plot(np.nanmin(lon),np.nanmax(lat),
    #         color='black',transform = ccrs.PlateCarree())
    # plt.plot(np.nanmax(lon),np.nanmin(lat),
    #         color='black',transform = ccrs.PlateCarree())
    # plt.plot(np.nanmax(lon),np.nanmax(lat),
    #         color='black',transform = ccrs.PlateCarree())

    plt.legend()

    print '******'
    print ''
    print 'Finished plotting cartopy map! :)'
    print ''

    # plt.savefig('FIGS/HighArctic_vPOSTER.svg', dpi=100)
    plt.show()

def plot_contour_TS(cube, filename): #, lon, lat):

    import iris.plot as iplt
    import iris.quickplot as qplt
    import iris.analysis.cartography
    import cartopy.crs as ccrs
    import cartopy
        # from matplotlib.patches import Polygon

    ###################################
    ## CHOOSE DIAGNOSTIC
    ###################################
    diag = 2
    print ''
    print 'Diag is: '
    print cube[diag]
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

    ###################################
    ## DEFINE DIMENSIONS COORDS DEPENDING ON DIAG
    ###################################

    time = cube[diag].dim_coords[0].points
    height = cube[diag].dim_coords[1].points

    ###################################
    ## PLOT MAP
    ###################################

    print '******'
    print ''
    print 'Plotting contour timeseries:'
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
    plt.figure(figsize=(8,6))
    ax = plt.gca()

    # plt.plot(cube[diag].dim_coords[0].points,cube[diag][:,0].data)        # line plot
    # plt.contourf(cube[0].data)
    # plt.plot(cube[2][0,:].data,height);plt.show()
    #################################################################
    ## plot contour timeseries
    ################################################################
    plt.contourf(time,height,np.transpose(cube[diag].data))
    # plt.pcolormesh(time,height,np.transpose(cube[2].data))
    plt.title(cube[diag].standard_name + ', ' + str(cube[diag].units))
    plt.colorbar()
    ax.set_ylim([0, 3000])

    plt.legend()

    print '******'
    print ''
    print 'Finished plotting! :)'
    print ''

    # plt.savefig('FIGS/12-13Aug_Outline_wShipTrackMAPPED.svg')
    plt.show()

def plot_multicontour_TS(cube, filename, out_dir): #, lon, lat):

    import iris.plot as iplt
    import iris.quickplot as qplt
    import iris.analysis.cartography
    import cartopy.crs as ccrs
    import cartopy
    import matplotlib.cm as mpl_cm
        # from matplotlib.patches import Polygon

    ###################################
    ## PLOT MAP
    ###################################

    print '******'
    print ''
    print 'Plotting contour timeseries:'
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
    plt.figure(figsize=(12,10))
    # plt.rc('figure',titlesize=LARGE_SIZE)
    plt.subplots_adjust(top = 0.95, bottom = 0.05, right = 0.96, left = 0.1,
            hspace = 0.4, wspace = 0.1)

    l = -1
    for i in range(0,len(cube)):
        ## ONLY WANT COLUMN VARIABLES - IGNORE TIMESERIES FOR NOW
        if np.sum(cube[i].data.shape) > 30:     # ignores microwave frequency diagnostics

                ###################################
                ## CHOOSE DIAGNOSTIC
                ###################################
                diag = i
                print ''
                print 'Diag is: '
                print cube[diag]

                ### define empty array for cube data
                data = []

                ###################################
                ## DEFINE DIMENSIONS COORDS DEPENDING ON DIAG
                ###################################

                time = cube[diag].dim_coords[0].points
                height = cube[37].data   #cube[diag].dim_coords[1].points #cube[37].data

                #################################################################
                ## data corrections
                #################################################################
                ### set height limit to consider
                ind = np.where(height[0,:]<5000)

                # cube[diag].data
                # for k in range(0,len(height)):
                #     for t in range(0,len(time)):
                #         if cube[diag].data.mask[t,k] == True: cube[diag].data[t,k] = np.nan

                if cube[diag].var_name == 'temperature':
                    data = np.transpose(np.squeeze(cube[diag].data[:,ind]))
                    title = cube[diag].var_name + ' [' + str(cube[diag].units) + ']'
                elif cube[diag].var_name == 'qi':
                    data = np.transpose(np.squeeze(cube[diag].data[:,ind]*1e3))
                    title = cube[diag].var_name + ' [g/kg]'
                elif cube[diag].var_name == 'ql':
                    data = np.transpose(np.squeeze(cube[diag].data[:,ind]*1e3))
                    title = cube[diag].var_name + ' [g/kg]'
                elif cube[diag].var_name == 'q':
                    data = np.transpose(np.squeeze(cube[diag].data[:,ind]*1e3))
                    title = cube[diag].var_name + ' [g/kg]'
                elif cube[diag].var_name == 'pressure':
                    data = np.transpose(np.squeeze(cube[diag].data[:,ind]/1e2))
                    title = cube[diag].var_name + ' [hPa]'
                elif cube[diag].var_name == 'uwind':
                    data = np.transpose(np.squeeze(cube[diag].data[:,ind]))
                    title = cube[diag].var_name + ' [' + str(cube[diag].units) + ']'
                elif cube[diag].var_name == 'wwind':
                    data = np.transpose(np.squeeze(cube[diag].data[:,ind]))
                    title = cube[diag].var_name + ' [' + str(cube[diag].units) + ']'
                elif cube[diag].var_name == 'rh':
                    data = np.transpose(np.squeeze(cube[diag].data[:,ind]*1e2))
                    title = cube[diag].var_name + ' [%]'
                elif cube[diag].var_name == 'cloud_fraction':
                    data = np.transpose(np.squeeze(cube[diag].data[:,ind]))
                    title = cube[diag].var_name + ' [' + str(cube[diag].units) + ']'
                elif cube[diag].var_name == 'vwind':
                    data = np.transpose(np.squeeze(cube[diag].data[:,ind]))
                    title = cube[diag].var_name + ' [' + str(cube[diag].units) + ']'

                #################################################################
                ## create figure and axes instances
                #################################################################
                if len(data) > 0:
                    l = l + 1 ## increment index for positive data association

                    print 'l = ' + str(l)
                    print title



                    plt.subplot(5,2,l+1)
                    ax = plt.gca()

                    #################################################################
                    ## plot timeseries
                    #################################################################
                    # plt.contourf(time,height,np.transpose(cube[diag].data))
                    if cube[diag].var_name == 'temperature':
                        plt.contourf(time, np.squeeze(height[0,ind]), data, vmin = 250, vmax = np.nanmax(data))
                    elif cube[diag].var_name == 'uwind':
                        plt.contourf(time, np.squeeze(height[0,ind]), data, vmin = -20, vmax = 20)
                    elif cube[diag].var_name == 'vwind':
                        plt.contourf(time, np.squeeze(height[0,ind]), data, vmin = -20, vmax = 20)
                    elif cube[diag].var_name == 'wwind':
                        plt.contourf(time, np.squeeze(height[0,ind]), data, vmin = -0.1, vmax = 0.1)
                    elif cube[diag].var_name == 'pressure':
                        plt.contourf(time, np.squeeze(height[0,ind]), data, vmin = 500, vmax = 1000)
                    elif cube[diag].var_name == 'rh':
                        plt.contourf(time, np.squeeze(height[0,ind]), data, vmin = 50, vmax = 100)
                    else:
                        plt.contourf(time, np.squeeze(height[0,ind]), data, vmin = np.nanmin(data), vmax = np.nanmax(data))

                    #################################################################
                    ## set plot properties
                    #################################################################
                    ### colormaps:
                    if cube[diag].var_name == 'wwind':
                        plt.set_cmap(mpl_cm.RdBu_r)
                    elif cube[diag].var_name == 'uwind':
                        plt.set_cmap(mpl_cm.RdBu_r)
                    elif cube[diag].var_name == 'vwind':
                        plt.set_cmap(mpl_cm.RdBu_r)
                    elif cube[diag].var_name[0] == 'q':
                        plt.set_cmap(mpl_cm.Blues)
                    else:
                        plt.set_cmap(mpl_cm.viridis)

                    ### title and axes properties
                    plt.title(title)
                    plt.colorbar()
                    ax.set_ylim([0, 5000])
                    # plt.gca().invert_yaxis()


                    ### global plot properties
                    plt.subplot(5,2,9)
                    plt.xlabel('Time [UTC]')
                    plt.ylabel('Z [m]')
                    plt.subplot(5,2,10)
                    plt.xlabel('Time [UTC]')
                    plt.subplot(5,2,1)
                    plt.ylabel('Z [m]')
                    plt.subplot(5,2,3)
                    plt.ylabel('Z [m]')
                    plt.subplot(5,2,5)
                    plt.ylabel('Z [m]')
                    plt.subplot(5,2,7)
                    plt.ylabel('Z [m]')

    print '******'
    print ''
    print 'Finished plotting! :)'
    print ''

    fileout = '../FIGS/ECMWF/' + filename[-22:-3] + '.png'
    plt.savefig(fileout, dpi=300)
    plt.show()

def plot_multicontour_multidate_TS(timem, data, cube, month_flag, missing_files, out_dir): #, lon, lat):

    import iris.plot as iplt
    import iris.quickplot as qplt
    import iris.analysis.cartography
    import cartopy.crs as ccrs
    import cartopy
    import matplotlib.cm as mpl_cm
        # from matplotlib.patches import Polygon

    ###################################
    ## PLOT MAP
    ###################################

    print '******'
    print ''
    print 'Plotting combined contour timeseries:'
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
    plt.figure(figsize=(15,10))
    # plt.rc('figure',titlesize=LARGE_SIZE)
    plt.subplots_adjust(top = 0.95, bottom = 0.05, right = 0.96, left = 0.1,
            hspace = 0.4, wspace = 0.1)

    print data.keys()

    l = -1

    # for i in range(0,len(data.keys())):
    for diag in range(0,len(data.keys())):
        ###################################
        ## CHOOSE DIAGNOSTIC
        ###################################
        # diag = i
        print ''
        print 'Diag is: '
        print data.keys()[diag]

        ### pcXXX - CUBE
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

        ###################################
        ## DEFINE DIMENSIONS COORDS DEPENDING ON DIAG
        ###################################

        ### the following works for now, but could do with finding an easier
        ###         way to index cube by string
        for j in range(0,len(cube)):
            if cube[j].var_name == 'ql': height = cube[37].data[0,:]#cube[j].dim_coords[1].points

        dat = []
        print 'dat = ' + str(len(dat))

        ### set diag-specific titles
        if str(data.keys()[diag]) == "radr_refl":
            title = str(data.keys()[diag]) + ' [dBz]'
            dat = np.transpose(np.squeeze(data[data.keys()[diag]].data))
        elif str(data.keys()[diag]) == "pressure":
            title = str(data.keys()[diag]) + ' [hPa]'
            dat = np.transpose(np.squeeze(data[data.keys()[diag]].data/1e2))
        elif str(data.keys()[diag]) == "temperature":
            title = str(data.keys()[diag]) + ' [K]'
            dat = np.transpose(np.squeeze(data[data.keys()[diag]].data))
        elif str(data.keys()[diag]) == "uwind":
            title = str(data.keys()[diag]) + ' [m/s]'
            dat = np.transpose(np.squeeze(data[data.keys()[diag]].data))
        elif str(data.keys()[diag]) == "wwind":
            title = str(data.keys()[diag]) + ' [m/s]'
            dat = np.transpose(np.squeeze(data[data.keys()[diag]].data))
        elif str(data.keys()[diag]) == "vwind":
            title = str(data.keys()[diag]) + ' [m/s]'
            dat = np.transpose(np.squeeze(data[data.keys()[diag]].data))
        elif str(data.keys()[diag]) == "cloud_fraction":
            title = str(data.keys()[diag]) + ' []'
            dat = np.transpose(np.squeeze(data[data.keys()[diag]].data))
        elif str(data.keys()[diag]) == "qi":
            title = str(data.keys()[diag]) + ' [g/kg]'
            dat = np.transpose(np.squeeze(data[data.keys()[diag]].data*1e3))
        elif str(data.keys()[diag]) == "ql":
            title = str(data.keys()[diag]) + ' [g/kg]'
            dat = np.transpose(np.squeeze(data[data.keys()[diag]].data*1e3))
        elif str(data.keys()[diag]) == "q":
            title = str(data.keys()[diag]) + ' [g/kg]'
            dat = np.transpose(np.squeeze(data[data.keys()[diag]].data*1e3))
        elif str(data.keys()[diag]) == "rh":
            title = str(data.keys()[diag]) + ' [%]'
            dat = np.transpose(np.squeeze(data[data.keys()[diag]].data*1e2))

        print 'dat = ' + str(len(dat))
        print ''

        if len(dat) > 0:
            print 'Plotting since len(dat)>0'
            print ''
            print title

            l = l + 1 ## increment index for positive data association
            print 'l = ' +  str(l)
            #################################################################
            ## create figure and axes instances
            #################################################################
            plt.subplot(5,2,l+1)
            ax = plt.gca()

            #################################################################
            ## plot timeseries
            #################################################################
            # plt.contourf(time,height,np.transpose(cube[diag].data))
            if str(data.keys()[diag]) == 'temperature':
                plt.pcolormesh(timem, height, dat, vmin = 250, vmax = np.nanmax(dat))
            elif str(data.keys()[diag]) == 'pressure':
                plt.pcolormesh(timem, height, dat, vmin = 500, vmax = np.nanmax(dat))
            elif str(data.keys()[diag]) == 'uwind':
                plt.pcolormesh(timem, height, dat, vmin = -20, vmax = 20)
            elif str(data.keys()[diag]) == 'vwind':
                plt.pcolormesh(timem, height, dat, vmin = -20, vmax = 20)
            elif str(data.keys()[diag]) == 'wwind':
                plt.pcolormesh(timem, height, dat, vmin = -0.1, vmax = 0.1)
            elif str(data.keys()[diag]) == 'qice':
                plt.pcolormesh(timem, height, dat, vmin = 0, vmax = 0.05)
            elif str(data.keys()[diag]) == 'rh':
                plt.pcolormesh(timem, height, dat, vmin = 50, vmax = 100)
            else:
                plt.pcolormesh(timem, height, dat, vmin = np.nanmin(dat), vmax = np.nanmax(dat))
            #################################################################
            ## set plot properties
            #################################################################
            ### colormaps:
            if str(data.keys()[diag]) == 'wwind':
                plt.set_cmap(mpl_cm.RdBu_r)
            elif str(data.keys()[diag]) == 'uwind':
                plt.set_cmap(mpl_cm.RdBu_r)
            elif str(data.keys()[diag]) == 'vwind':
                plt.set_cmap(mpl_cm.RdBu_r)
            elif str(data.keys()[diag][0]) == 'q':
                plt.set_cmap(mpl_cm.Blues)
            else:
                plt.set_cmap(mpl_cm.viridis)

            plt.title(title)
            plt.colorbar()
            ax.set_ylim([0, 5000])
            if month_flag == 8: ax.set_xlim([13.0, 32.0])
            if month_flag == 9: ax.set_xlim([1.0, 15.0])
            if month_flag == -1: ax.set_xlim([225.0, 257.0])

            print ''
            print 'Zero out any data from missing files:'
            print ''
            for mfile in missing_files:
                # mtime = float(mfile[6:8]) + ((cube[0].dim_coords[0].points)/24.0)
                # nans = np.zeros([len(height),len(mtime)])
                # # nans[nans == 0] = np.nan
                # plt.pcolormesh(mtime, height, nans)
                mtime = np.arange(247,249,0.1)    ### change all 20180904 points (doy = 247) to nans
                nans = ax.get_ylim()
                ax.fill_between(mtime, nans[0], nans[-1], facecolor = 'lightgrey', zorder = 3)

    ### global plot properties
    plt.subplot(5,2,9)
    if month_flag == 8: plt.xlabel('Day of month [Aug]')
    if month_flag == 9: plt.xlabel('Day of month [Sep]')
    if month_flag == -1: plt.xlabel('Day of year')
    plt.ylabel('Z [m]')
    plt.subplot(5,2,10)
    if month_flag == 8: plt.xlabel('Day of month [Aug]')
    if month_flag == 9: plt.xlabel('Day of month [Sep]')
    if month_flag == -1: plt.xlabel('Day of year')
    plt.subplot(5,2,1)
    plt.ylabel('Z [m]')
    plt.subplot(5,2,3)
    plt.ylabel('Z [m]')
    plt.subplot(5,2,5)
    plt.ylabel('Z [m]')
    plt.subplot(5,2,7)
    plt.ylabel('Z [m]')

    print '******'
    print ''
    print 'Finished plotting! :)'
    print ''

    if month_flag == 8:
        fileout = '../FIGS/ECMWF/201808_oden_ecmwf.png'
    if month_flag == 9:
        fileout = '../FIGS/ECMWF/201809_oden_ecmwf.png'
    if month_flag == -1:
        fileout = '../FIGS/ECMWF/moccha_oden_ecmwf.png'
    plt.savefig(fileout, dpi=300)
    plt.show()

def plot_IFS_ContourTS(timem, data, month_flag, missing_files, out_dir, doy): #, lon, lat):

    import iris.plot as iplt
    import iris.quickplot as qplt
    import iris.analysis.cartography
    import cartopy.crs as ccrs
    import cartopy
    import matplotlib.cm as mpl_cm
        # from matplotlib.patches import Polygon

    ###################################
    ## PLOT MAP
    ###################################

    print '******'
    print ''
    print 'Plotting IFS contour timeseries for entire drift:'
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
    plt.figure(figsize=(15,10))
    # plt.rc('figure',titlesize=LARGE_SIZE)
    plt.subplots_adjust(top = 0.95, bottom = 0.05, right = 0.96, left = 0.1,
            hspace = 0.4, wspace = 0.1)

    print data.keys()

    ### pcXXX - CUBE
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

    ###################################
    ## DEFINE DIMENSIONS COORDS DEPENDING ON DIAG
    ###################################

    ### the following works for now, but could do with finding an easier
    ###         way to index cube by string
    # for j in range(0,len(cube)):
    #     if cube[j].var_name == 'ql': height = cube[j].dim_coords[1].points

    ###################################
    ### set diag-specific titles
    ###################################
    height = np.transpose(np.nanmean(np.squeeze(data['height'].data),0))    ## use average height coordinate
    temperature = np.transpose(np.squeeze(data['temperature'].data))
    uwind = np.transpose(np.squeeze(data['uwind'].data))
    wwind = np.transpose(np.squeeze(data['wwind'].data))
    vwind = np.transpose(np.squeeze(data['vwind'].data))
    qice = np.transpose(np.squeeze(data['qi'].data*1e3))
    qliq = np.transpose(np.squeeze(data['ql'].data*1e3))
    q = np.transpose(np.squeeze(data['q'].data*1e3))

    #################################################################
    ## create figure and axes instances
    #################################################################
    plt.subplot(4,2,1)
    plt.pcolormesh(timem, height, temperature, vmin = 250, vmax = 275)
    plt.set_cmap(mpl_cm.viridis)
    plt.title('Temperature [K]')
    plt.colorbar()
    ax = plt.gca()
    ax.set_ylim([0, 5000])
    ax.set_xlim([doy[0], doy[-1]])
    plt.ylabel('Z [m]')

    plt.subplot(4,2,2)
    plt.pcolormesh(timem, height, q, vmin = 0.0, vmax = 4.0)
    plt.set_cmap(mpl_cm.Blues)
    plt.title('q [g/kg]')
    plt.colorbar()
    ax = plt.gca()
    ax.set_ylim([0, 5000])
    ax.set_xlim([doy[0], doy[-1]])

    plt.subplot(4,2,3)
    plt.pcolormesh(timem, height, qliq, vmin = 0.0, vmax = 0.35)
    plt.set_cmap(mpl_cm.Blues)
    plt.title('qliq [g/kg]')
    plt.colorbar()
    ax = plt.gca()
    ax.set_ylim([0, 5000])
    ax.set_xlim([doy[0], doy[-1]])
    plt.ylabel('Z [m]')

    plt.subplot(4,2,4)
    plt.pcolormesh(timem, height, qice, vmin = 0, vmax = 0.05)
    plt.set_cmap(mpl_cm.Blues)
    plt.title('qice [g/kg]')
    plt.colorbar()
    ax = plt.gca()
    ax.set_ylim([0, 5000])
    ax.set_xlim([doy[0], doy[-1]])

    plt.subplot(4,2,5)
    plt.pcolormesh(timem, height, uwind, vmin = -20, vmax = 20)
    plt.set_cmap(mpl_cm.RdBu_r)
    plt.title('uwind [m/s]')
    plt.colorbar()
    ax = plt.gca()
    ax.set_ylim([0, 5000])
    ax.set_xlim([doy[0], doy[-1]])
    plt.ylabel('Z [m]')

    plt.subplot(4,2,6)
    plt.pcolormesh(timem, height, vwind, vmin = -20, vmax = 20)
    plt.set_cmap(mpl_cm.RdBu_r)
    plt.title('vwind [m/s]')
    plt.colorbar()
    ax = plt.gca()
    ax.set_ylim([0, 5000])
    ax.set_xlim([doy[0], doy[-1]])
    plt.xlabel('Day of year')

    plt.subplot(4,2,7)
    plt.pcolormesh(timem, height, wwind, vmin = -0.1, vmax = 0.1)
    plt.set_cmap(mpl_cm.RdBu_r)
    plt.title('wwind [m/s]')
    plt.colorbar()
    ax = plt.gca()
    ax.set_ylim([0, 5000])
    ax.set_xlim([doy[0], doy[-1]])
    plt.xlabel('Day of year')
    plt.ylabel('Z [m]')

    print '******'
    print ''
    print 'Finished plotting! :)'
    print ''

    fileout = 'FIGS/AO2018_oden_ecmwf_vPaper'
    plt.savefig(fileout + '.png', dpi=300)
    plt.show()

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
        root_dir = '/home/gillian/MOCCHA/ECMWF/'
        ship_filename = '/home/gillian/MOCCHA/ODEN/DATA/2018_shipposition_1hour.txt'

    ### CHOSEN RUN
    out_dir = 'OUT_25H/'

    ### TESTING/domain_tests/umnsaa_pa000
    ### 4_u-bg610_RA2M_CON/OUT_R1/papbpc_combined/
    ### 5_u-bl616_RA2M_CASIM/OUT_R0/

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
    # tempnames = ['umnsaa_pa012_r0.nc','umnsaa_pb012_r0.nc','umnsaa_pc011_r0.nc','umnsaa_pd011_r0.nc','20180812_oden_ecmwf.nc']
    Aug_names = ['20180813_oden_ecmwf.nc','20180814_oden_ecmwf.nc','20180815_oden_ecmwf.nc','20180816_oden_ecmwf.nc','20180817_oden_ecmwf.nc',
            '20180818_oden_ecmwf.nc','20180819_oden_ecmwf.nc','20180820_oden_ecmwf.nc','20180821_oden_ecmwf.nc',
            '20180822_oden_ecmwf.nc','20180823_oden_ecmwf.nc','20180824_oden_ecmwf.nc','20180825_oden_ecmwf.nc',
            '20180826_oden_ecmwf.nc','20180827_oden_ecmwf.nc','20180828_oden_ecmwf.nc','20180829_oden_ecmwf.nc',
            '20180830_oden_ecmwf.nc','20180831_oden_ecmwf.nc']

    Sep_names = ['20180901_oden_ecmwf.nc','20180902_oden_ecmwf.nc','20180903_oden_ecmwf.nc','20180904_oden_ecmwf.nc',
            '20180905_oden_ecmwf.nc','20180906_oden_ecmwf.nc','20180907_oden_ecmwf.nc','20180908_oden_ecmwf.nc',
            '20180909_oden_ecmwf.nc','20180910_oden_ecmwf.nc','20180911_oden_ecmwf.nc','20180912_oden_ecmwf.nc',
            '20180913_oden_ecmwf.nc','20180914_oden_ecmwf.nc']

    moccha_names = ['20180813_oden_ecmwf.nc','20180814_oden_ecmwf.nc','20180815_oden_ecmwf.nc','20180816_oden_ecmwf.nc','20180817_oden_ecmwf.nc',
            '20180818_oden_ecmwf.nc','20180819_oden_ecmwf.nc','20180820_oden_ecmwf.nc','20180821_oden_ecmwf.nc',
            '20180822_oden_ecmwf.nc','20180823_oden_ecmwf.nc','20180824_oden_ecmwf.nc','20180825_oden_ecmwf.nc',
            '20180826_oden_ecmwf.nc','20180827_oden_ecmwf.nc','20180828_oden_ecmwf.nc','20180829_oden_ecmwf.nc',
            '20180830_oden_ecmwf.nc','20180831_oden_ecmwf.nc','20180901_oden_ecmwf.nc','20180902_oden_ecmwf.nc',
            '20180903_oden_ecmwf.nc','20180905_oden_ecmwf.nc','20180906_oden_ecmwf.nc',
            '20180907_oden_ecmwf.nc','20180908_oden_ecmwf.nc','20180909_oden_ecmwf.nc','20180910_oden_ecmwf.nc',
            '20180911_oden_ecmwf.nc','20180912_oden_ecmwf.nc','20180913_oden_ecmwf.nc','20180914_oden_ecmwf.nc']

    Aug_missing_files = ['20180812_oden_ecmwf.nc']

    Sep_missing_files = ['20180904_oden_ecmwf.nc']

    moccha_missing_files = ['20180812_oden_ecmwf.nc','20180904_oden_ecmwf.nc']

    doy = np.arange(225,258)        ## set DOY for full moccha figures

    # names = ['umnsaa_pa000','umnsaa_pc000.nc']       ### DEFAULT OUTPUT NAMES FOR TESTING

    ## Flag for individual file or monthly:
    combine = 1
    ## Choose month:
    names = moccha_names
    missing_files = moccha_missing_files
    month_flag = -1         ### -1 to plot as DOY

    if combine == 0:
        name = '20180813_oden_ecmwf.nc'
        filename = root_dir + out_dir + name#s[1]
        print filename
        print ''

        # -------------------------------------------------------------
        #### LOAD CUBE
        # -------------------------------------------------------------
        print 'Loading multiple diagnostics:'
        cube = iris.load(filename)

        print cube
        print ''

        # -------------------------------------------------------------
        # Plot data (5x2 timeseries)
        # -------------------------------------------------------------
        # figure = plot_multicontour_TS(cube, filename, out_dir)

        # -------------------------------------------------------------
        # Plot data (map)
        # -------------------------------------------------------------
        ### select hour to plot
        # date = '20180814'
        # hour = 0
        # figure = plot_cartmap(ship_data, cube, hour, date)#, lon, lat)

    else:
        for i in range(0,len(names)):
            filename = root_dir + out_dir + names[i]
            print filename
            print ''

            print 'Loading multiple diagnostics:'
            # cube = iris.load(filename)
            nc2 = Dataset(filename,'r')

            # print 'i = ' + str(i)
            print ''

            #### only load specific variables
            var_list = ['temperature','q','ql','qi','uwind','vwind','wwind','height']   ### time always read in separately

            ###     LOAD IN IFS DATA
            if i == 0:
                ifs_data = {}
                ifs_data1d = {}
                if month_flag == -1:
                    time_ifs = doy[i] + ((nc2.variables['time'][:])/24.0)
                else:
                    time_ifs = float(names[i][6:8]) + ((nc2.variables['time'][:])/24.0)
                for j in range(0,len(var_list)):
                    if np.sum(nc2.variables[var_list[j]].shape) <= 25:  # 1d timeseries only
                        ifs_data1d[var_list[j]] = nc2.variables[var_list[j]][:]
                    else:                                   # 2d column um_data
                        ifs_data[var_list[j]] = nc2.variables[var_list[j]][:]
                        ## set filled values to nans
                        ifs_data[var_list[j]][ifs_data[var_list[j]] == -9999.0] = np.nan
            else:
                if month_flag == -1:
                    time_ifs = np.append(time_ifs, doy[i] + ((nc2.variables['time'][:])/24.0))
                else:
                    time_ifs = np.append(time_ifs,float(filename_ifs[-16:-14]) + ((nc2.variables['time'][:])/24.0))
                print ifs_data
                for j in range(0,len(var_list)):
                    ## ONLY WANT COLUMN VARIABLES - IGNORE TIMESERIES FOR NOW
                    # print 'j = ' + str(j)
                    if np.sum(nc2.variables[var_list[j]].shape) <= 25:
                        ifs_data1d[var_list[j]] = np.append(ifs_data1d[var_list[j]].data,nc2.variables[var_list[j]][:])
                    else:
                        ifs_data[var_list[j]] = np.append(ifs_data[var_list[j]].data,nc2.variables[var_list[j]][:],0)
                        ## set filled values to nans
                        ifs_data[var_list[j]][ifs_data[var_list[j]] == -9999.0] = np.nan
            nc2.close()

            # if i == 0:
            #     data = {}
            #     data1d = {}
            #     # data['time'] = []
            #     # data['time'] = float(filename[-16:-14]) + ((cube[0].dim_coords[0].points)/24.0)
            #     # timem = float(filename[-16:-14]) + ((cube[0].dim_coords[0].points)/24.0)
            #     if month_flag == -1:
            #         timem = doy[i] + ((cube[0].dim_coords[0].points)/24.0)
            #     else:
            #         timem = float(filename[-16:-14]) + ((cube[0].dim_coords[0].points)/24.0)
            #     for j in range(0,len(cube)):
            #         ## ONLY WANT COLUMN VARIABLES - IGNORE TIMESERIES FOR NOW
            #         if np.size(np.shape(cube[j])) == 0:     # ignore horizontal_resolution
            #             continue
            #         elif np.size(np.shape(cube[j])) == 1:  # 1d timeseries only
            #             data1d[cube[j].var_name] = cube[j].data
            #         else:                                   # 2d column data
            #             data[cube[j].var_name] = cube[j].data
            #     # print data1d[cube[j].var_name]
            # else:
            #     # data['time'] = np.append(data['time'],float(filename[-16:-14]) + ((cube[0].dim_coords[0].points)/24.0))
            #     if month_flag == -1:
            #         if doy[i] == 247:       ### don't load data from 20180904
            #             continue
            #         else:
            #             timem = np.append(timem, doy[i] + ((cube[0].dim_coords[0].points)/24.0))
            #     else:
            #         timem = np.append(timem,float(filename[-16:-14]) + ((cube[0].dim_coords[0].points)/24.0))
            #     # print data
            #     for j in range(0,len(cube)):
            #         ## ONLY WANT COLUMN VARIABLES - IGNORE TIMESERIES FOR NOW
            #         # print 'j = ' + str(j)
            #         if np.size(np.shape(cube[j])) == 0:     # ignore horizontal_resolution
            #             continue
            #         elif np.size(np.shape(cube[j])) == 1:
            #             data1d[cube[j].var_name] = np.append(data1d[cube[j].var_name].data,cube[j].data)
            #         else:
            #             data[cube[j].var_name] = np.append(data[cube[j].var_name].data,cube[j].data,0)
            #     # print data

            # print 'Data dict = ' + str(data['radr_refl'].shape)

        # -------------------------------------------------------------
        # Plot combined column data (5x2 timeseries)
        # -------------------------------------------------------------
        np.save('working_data', ifs_data)
        # figure = plot_multicontour_multidate_TS(time_ifs, ifs_data, cube, month_flag, missing_files, out_dir)
                    ### doesn't matter which cube, just needed for dim_coords
        figure = plot_IFS_ContourTS(time_ifs, ifs_data, month_flag, missing_files, out_dir, doy)

    # -------------------------------------------------------------
    # FIN.
    # -------------------------------------------------------------
    END_TIME = time.time()
    print '******'
    print ''
    print 'End: ' + time.strftime("%c")
    print ''

    #### DIAGNOSTICS TO CHOOSE FROM:

    #### test

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
