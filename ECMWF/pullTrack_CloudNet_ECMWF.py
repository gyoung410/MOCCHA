###
###
### SCRIPT TO READ IN UM MODEL DATA IN NETCDF FORMAT AS IRIS CUBE,
###         PULL SHIP TRACK, AND OUTPUT AS NETCDF FOR CLOUDNET
###


import time
import datetime
import numpy as np
from netCDF4 import Dataset
import numpy as np
# import diags_MOCCHA as diags
# import diags_varnames as varnames
# import cartopy.crs as ccrs
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

def pullLatLon(filename):

    from netCDF4 import Dataset

    print '*****'
    print 'Extracting lat/lon from ECMWF netCDF file'
    print ''

    nc = Dataset(filename,'r')

    lat = nc.variables['latitude'][:]
    lon = nc.variables['longitude'][:]
    time = nc.variables['time'][:]

    print 'ECMWF file at: (' + str(lon) + ', ' + str(lat) + ')'

    nc.close()

    return lat, lon, time

def designGrid(lats, lons, tim):

    # print '*****'
    # print 'Find mid-points between ECMWF grid points'
    # print ''
    #
    # edgelats = np.zeros([38])
    # edgelons = np.zeros([38])
    # latdiff = np.zeros([38])
    # londiff = np.zeros([38])
    # for j in range(0,37):
    #     if lats[j] < lats[j+1]:
    #         edgelats[j] = (lats[j+1] + lats[j])/2.0
    #         latdiff[j] = (lats[j+1] - lats[j])/2.0
    #     elif lats[j] == lats[j+1]:
    #         if j < 36:
    #             if lats[j] < lats[j+2]: edgelats[j] = (lats[j+2] + lats[j])/2.0
    #     if lons[j] < lons[j+1]:
    #         edgelons[j] = (lons[j+1] + lons[j])/2.0
    #         londiff[j] = (lons[j+1] - lons[j])/2.0
    #     # if lons[j] > lons[j+1]:
    #     #     edgelons[j] = (lons[j+1] + lons[j])/2.0
    #     #     londiff[j] = (lons[j+1] - lons[j])/2.0
    #     elif lons[j] == lons[j+1]: edgelons[j] = lons[j]
    # edgelats[edgelats==0] = lats[edgelats==0] + latdiff[0]
    # edgelons[-1] = lons[-1] + (lons[-1] - edgelons[-2])

    # plt.plot(lons,lats,'bs',markersize=8);
    # plt.plot(lons[edgelats>0],edgelats[edgelats>0],'r^');
    # plt.plot(edgelons[edgelons>0],lats[edgelons>0],'g>');
    # plt.show()


    print '*****'
    print 'Use trig to design grid:'
    print ''

    edgelats = np.zeros([38])
    edgelons = np.zeros([38])

    print 'Latitude: th = (arc_m / R_e) * 180/(pi)'
    print ''
    R_e = 6.4*10e6          # radius of the Earth
    lat_arc = 9.0*1e3       # distance in m
    th1 = lat_arc/R_e        # angle in radians
    th1 = (th1/np.pi)*180.0   # angle in degrees

    edgelats = lats + th1    # gives upper grid boundaries for latitude

    print 'Longitude: '
    print '(needs to account for latitude)'
    print ''

    lon_arc = 9.0*1e3
    th2 = lat_arc/R_e        # angle in radians
    th2 = (th1/np.pi)*180.0   # angle in degrees

    # plt.plot(lons,lats,'bs');
    # plt.plot(lons[edgelats>0],edgelats[edgelats>0],'r^');
    # plt.plot(edgelons[edgelons>0],lats[edgelons>0],'g>');
    # plt.show()

    return edgelats, edgelons

def checkLatLon(ship_data, lats, lons, date, tim):

    print ''
    print 'Finding lat/lon of ship track'
    print '...'

    #################################################################
    ## find date of interest
    #################################################################
    day_ind = np.where(np.logical_and(ship_data.values[:,2] == float(date[-2:]),ship_data.values[:,1] == float(date[-4:-2])))

    #################################################################
    ## print ship track coordinates
    #################################################################
    print 'Ship start (lon,lat): ' + str(ship_data.values[day_ind[0][0],7]) + ', ' + str(ship_data.values[day_ind[0][0],6])
    print 'Ship end (lon,lat): ' + str(ship_data.values[day_ind[0][-1],7]) + ', ' + str(ship_data.values[day_ind[0][-1],6])

    ship_lats = ship_data.values[day_ind,7]
    ship_lons = ship_data.values[day_ind,6]

    i = 0
    # for i in range(0,24):
    for j in range(0,37):
        ind1 = np.where(np.logical_and(ship_lats[0][i] > lats[j],ship_lats[0][i] <= lats[j+1]))
        print ind1

    map = plot_basemap(ship_data, lats, lons, tim)

    return day_ind

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
    Aug_inIce = np.where(np.logical_and(np.logical_and(data.values[:,2]>=12,data.values[:,1]==8),data.values[:,3]>=0))
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
    # print 'Mean lon/lat of ship track: (' + str(np.nanmedian(data.values[inIce_index,6])) + ', ' + str(np.nanmedian(data.values[inIce_index,7])) + ')'
    print 'Lon/lat of start point: (' + str(data.values[inIce_index[0],6]) + ', ' + str(data.values[inIce_index[0],7]) + ')'
    print 'Lon/lat of end point: (' + str(data.values[inIce_index[-1],6]) + ', ' + str(data.values[inIce_index[-1],7]) + ')'
    # print 'Min/max longitude: ' + str(np.nanmin(data.values[inIce_index,6])) + ', ' + str(np.nanmax(data.values[inIce_index,6]))
    # print 'Min/max latitude: ' + str(np.nanmin(data.values[inIce_index,7])) + ', ' + str(np.nanmax(data.values[inIce_index,7]))
    print ''

    return inIce_index

def trackShip(data, date):

    ###################################
    ## DEFINE METUM PERIOD (CLOUDNET COMPARISON)
    ###################################
    trackShip_start = np.where(np.logical_and(np.logical_and(data.values[:,2]==int(date[-2:]),data.values[:,1]==int(date[-4:-2])),data.values[:,3]>=0))
    trackShip_end = np.where(np.logical_and(np.logical_and(data.values[:,2]==(int(date[-2:]) + 1),data.values[:,1]==int(date[-4:-2])),data.values[:,3]==1))
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

def plot_basemap(ship_data, lats, lons, tim):

    from mpl_toolkits.basemap import Basemap
    from matplotlib.patches import Polygon

    ###################################
    ## PLOT MAP
    ###################################

    print '******'
    print ''
    print 'Plot basemap:'
    print ''

    ##################################################
    ##################################################
    #### 	BASEMAP
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

    ## create figure and axes instances
    fig = plt.figure(figsize=(8,10))

    #########################################################################################################

    ax  = fig.add_axes([0.1,0.1,0.8,0.8])	# left, bottom, width, height

    ### MAP DIMENSIONS
    dim = 500000

    m = Basemap(width=0.75*dim,height=dim,
                resolution='l',projection='stere',\
                lat_ts=89,lat_0=89,lon_0=20)
    m.drawcoastlines()
    # m.bluemarble()

    # define parallels/meridians
    m.drawparallels(np.arange(-90.,-60.,2.),labels=[1,1,0,0],color='k',linewidth=1.,fontsize=10)
    m.drawmeridians(np.arange(-180.,181.,10.),labels=[0,0,0,1],color='k',linewidth=1.,fontsize=10)
    m.drawcoastlines(linewidth=1.)

    # m.drawmapboundary(fill_color='aqua')
    # m.fillcontinents(color='coral',lake_color='aqua')

    ### DEFINE DRIFT + IN_ICE PERIODS
    # drift_index = iceDrift(ship_data)
    # inIce_index = inIce(ship_data)
    trackShip_index = trackShip(ship_data)
    edgelats, edgelons = designGrid(lats, lons, tim)

    ### MAP ONTO PROJECTION
    x, y = m(ship_data.values[trackShip_index,6], ship_data.values[trackShip_index,7])

    # Plot tracks as line plot
    # plt.plot(x, y, color = 'darkorange', linewidth = 2, label = 'Ship track')

    x_ecmwf, y_ecmwf = m(lons, lats)
    # Plot grid box centres as scatter plot
    plt.scatter(x_ecmwf, y_ecmwf, 10,
            color = 'blue', marker = 's',
            edgecolor = 'blue', linewidth = 2,
            label = 'ECMWF')

    x_t, y_t = m(lons, edgelats)
    # Plot grid box centres as scatter plot
    plt.scatter(x_t, y_t, 10,
            color = 'red', marker = '^',
            edgecolor = 'blue', linewidth = 2,
            label = 'ECMWF top edges')

    x_r, y_r = m(edgelons[edgelons>0], lats[edgelons>0])
    # Plot grid box centres as scatter plot
    plt.scatter(x_r, y_r, 10,
            color = 'green', marker = '>',
            edgecolor = 'blue', linewidth = 2,
            label = 'ECMWF right edges')

    ###########################################
    ### PLOT NEST + SWATH FOR INCREASED FREQ DIAGS VIS
    ###########################################
        # I.B.:
        # Drift limits are:
        # latitude   88.4502 to 89.6388
        # longitude  4.6830 to 73.7629
        #
        # R.P.: original 1.5km nest -> (0, 86.625) @ 500x500

    ### ADD LEGEND
    plt.legend()

    plt.show()

def plot_cartmap(ship_data, data, date): #, lon, lat):

    import iris.plot as iplt
    import iris.quickplot as qplt
    import iris.analysis.cartography
    import cartopy.crs as ccrs
    import cartopy
        # from matplotlib.patches import Polygon

    ###################################
    ## CHOOSE DIAGNOSTIC
    ###################################
    # diag = 1
    print ''
    print 'Available diags are: ', data.keys()

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
    plt.figure(figsize=(12,10))
    # ax = plt.axes(projection=ccrs.Orthographic(0, 90))    # NP Stereo
    ax = plt.axes(projection=ccrs.NorthPolarStereo(central_longitude=30))

    ### set size
    # ax.set_extent([30, 60, 89.1, 89.6], crs=ccrs.PlateCarree())       ### ZOOM
    # ax.set_extent([40, 50, 88.4, 88.6], crs=ccrs.PlateCarree())       ### ZOOM
    ax.set_extent([0, 60, 87.75, 90], crs=ccrs.PlateCarree())     ### SWATH
    # ax.set_extent([-180, 190, 80, 90], crs=ccrs.PlateCarree())    ### WHOLE

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
    ################################################################
    # if np.size(cube[diag].data.shape) == 4:
    #     iplt.pcolormesh(cube[diag][hour,0,:,:])
    # elif np.size(cube[diag].data.shape) == 3:
    #     iplt.pcolormesh(cube[diag][hour,:,:])
    #     # iplt.pcolormesh(cube[hour,471:495,240:264])
    # elif np.size(cube[diag].data.shape) == 2:
    #     iplt.pcolormesh(cube[diag][:,:])
    # plt.title(cube[diag].standard_name + ', ' + str(cube[diag].units))
    # plt.colorbar()
    # plt.pcolormesh(data['lats'][:],data['lons'][:],data['pressure'][:,0,0])

    #################################################################
    ## plot UM nest
    #################################################################
    ### draw outline of grid
    # qplt.outline(cube[hour,380:500,230:285])          ### original swath
    # qplt.outline(cube[diag][hour,386:479,211:305])          ### redesigned swath (>13th)
    # qplt.outline(cube[hour,471:495,240:264])          ### 12-13th Aug swath
    # qplt.outline(cube[diag][hour,386:495,211:305])          ### misc
    # qplt.outline(cube[diag][hour,:,:])


    ### make grid of unique latitude and longitude points
    lats, lons = np.meshgrid(data['ulat'][:], data['ulon'][:])
    ### plot grid midpoints from file
    plt.scatter(data['lons'][:], data['lats'][:], c = 'black',#data['pressure'][:,0,0],
            label = 'Grid mid points',
            transform = ccrs.PlateCarree())

    ### find northern boundaries of gridpoints
    nblats = ((data['ulat'][1:] - data['ulat'][0:-1]) / 2.0) + data['ulat'][0:-1]       ## northern bounds for latitude
    data['nb_lats'] = np.zeros([np.size(data['lats'][:])])
    print 'Northern boundary array has shape: ' + str(np.size(nblats))
    for j in range(0,len(nblats)):
        # print 'j = ' + str(j)
        for i in range(0,len(data['lats'][:])):
            # print 'i = ' + str(i)
            if data['ulat'][j] == data['lats'][i]:
                data['nb_lats'][i] = nblats[j]

    plt.scatter(data['lons'][:], data['nb_lats'][:], c = 'red',
            label = 'northern bounds',
            transform = ccrs.PlateCarree())

    ### find eastern boundaries of gridpoints
    rblons = ((data['lons'][1:] - data['lons'][0:-1]) / 2.0) + data['lons'][0:-1]       ## RH bounds for longitude
    data['rb_lons'] = np.zeros([np.size(data['lons'][:-1])])
    data['rb_lons'][0:9] = rblons[0:9]
    data['rb_lons'][9] = rblons[8]
    data['rb_lons'][10:12] = rblons[10:12]
    data['rb_lons'][12] = rblons[11]
    data['rb_lons'][13] = rblons[13]
    data['rb_lons'][14] = rblons[13]
    data['rb_lons'][15:18] = rblons[15:18]
    data['rb_lons'][18] = data['lons'][17] + ((data['lons'][18] - data['lons'][17]) / 2.0)
    data['rb_lons'][19:21] = rblons[19]
    data['rb_lons'][21:27] = rblons[21:27]
    data['rb_lons'][27] = data['lons'][27] + (rblons[27] - data['lons'][27])/2.0
    data['rb_lons'][28:] = rblons[28:]
    data['rb_lons'][35] = rblons[34]
    plt.scatter(data['rb_lons'][:], data['lats'][0:-1], c = 'blue',
            label = 'eastern bounds',
            transform = ccrs.PlateCarree())

            # rblons[17:21]
    #################################################################
    ## plot ship track
    #################################################################
    ### DEFINE DRIFT + IN_ICE PERIODS
    drift_index = iceDrift(ship_data)
    inIce_index = inIce(ship_data)
    trackShip_index = trackShip(ship_data, date)

    ## Plot tracks as line plot
    # plt.plot(ship_data.values[:,6], ship_data.values[:,7],
    #          color = 'yellow', linewidth = 2,
    #          transform = ccrs.PlateCarree(), label = 'Whole',
    #          )
    # plt.plot(ship_data.values[inIce_index,6], ship_data.values[inIce_index,7],
    #          color = 'darkorange', linewidth = 3,
    #          transform = ccrs.PlateCarree(), label = 'In Ice',
    #          )
    # plt.plot(ship_data.values[inIce_index[0],6], ship_data.values[inIce_index[0],7],
    #          'k^', markerfacecolor = 'darkorange', linewidth = 3,
    #          transform = ccrs.PlateCarree(),
    #          )
    # plt.plot(ship_data.values[inIce_index[-1],6], ship_data.values[inIce_index[-1],7],
    #          'kv', markerfacecolor = 'darkorange', linewidth = 3,
    #          transform = ccrs.PlateCarree(),
    #          )
    plt.plot(ship_data.values[drift_index,6], ship_data.values[drift_index,7],
             color = 'yellow', linewidth = 2,
             transform = ccrs.PlateCarree(), label = 'Drift',
             )

    ### Plot tracks as line plot
    plt.plot(ship_data.values[trackShip_index,6], ship_data.values[trackShip_index,7],
             color = 'green', linewidth = 3,
             transform = ccrs.PlateCarree(), label = 'Ship track',
             )
    plt.plot(ship_data.values[trackShip_index[0],6], ship_data.values[trackShip_index[0],7],
             'k^', markerfacecolor = 'green', linewidth = 3,
             transform = ccrs.PlateCarree(),
             )
    plt.plot(ship_data.values[trackShip_index[-1],6], ship_data.values[trackShip_index[-1],7],
             'kv', markerfacecolor = 'green', linewidth = 3,
             transform = ccrs.PlateCarree(),
             )

    plt.legend()

    print '******'
    print ''
    print 'Finished plotting cartopy map! :)'
    print ''

    # plt.savefig('FIGS/12-13Aug_Outline_wShipTrackMAPPED.svg')
    plt.show()

def pullTrack(cube, grid_filename, con):

    from iris.coords import DimCoord
    from iris.cube import Cube
    import iris.plot as iplt

    print '******'
    print ''

    #################################################################
    ## load gridded ship track
    #################################################################
    # print '******'
    print ''
    print 'Pulling gridded track from netCDF:'
    print ''

    # tim, ilat, ilon = readGriddedTrack(grid_filename)

    #################################################################
    ## fix time index
    #################################################################

    if np.size(cube)>1:
        print ''
        print 'More than one variable constraint. Proceeding...'
        print ''

        cubetime = np.round(cube[0].coord('forecast_period').points - 12.0)      ### forecast period (ignore first 12h)
        print ''
        print 'Cube times relative to forecast start:', cubetime[:-1]
        print ''

        #################################################################
        ## CREATE EMPTY CUBE
        #################################################################
        ncube = Cube(np.zeros([np.size(cube),70,len(cubetime)-1]))

        #################################################################
        ## POPULATE NP ARRAY WITH DATA
        #################################################################
        ### populate 0th dimension with time field
        # data[:,0] = cubetime[:,:-1]

        for k in range(0,np.size(cube)):            ### loop over number of variables
            print ''
            print 'k = ', k, ###', so processing', con[k]   # doesn't work with global_con
            print ''
            #################################################################
            ## PROBE VARIABLE
            #################################################################
            ### do we want to average exluding zeros?
            stash_flag, stash = excludeZeros(cube[k])

            ### do we need to re-grid?  -- DOESN'T WORK LIKE WRF, GRID NOT SPACED SAME WAY
            # cube[k], wind_stash = checkWind(cube[k])

            #################################################################
            ## CHECK DIMENSIONS
            #################################################################
            if np.logical_and(np.size(cube[k].data,1) >= 69, np.size(cube[k].data,1) < 71):
                print 'Variable is 4D:'
                print ''
                #### create empty arrays to be filled
                data = np.zeros([len(cube[k].coord('model_level_number').points),len(cubetime)-1])
                ### make empty cube
                dim_flag = 1        ### for next loops
                print 'data.shape = ', str(data.shape)
                print ''
            else:
                print 'Variable is 3D:'
                print ''
                #### create empty arrays to be filled
                data = np.zeros([len(cubetime)-1])
                dim_flag = 0       ### for next loops
                print 'data.shape = ', str(data.shape)
                print ''

            #################################################################
            ## LOOP OVER TIME INDEX, DECOMPOSE ONTO 24H TIMESERIES
            #################################################################
            for j in range(0,len(cubetime)-1):              ### loop over time
                if j < len(cubetime[:-1]):
                    itime = np.where(np.logical_and(tim >= cubetime[j], tim < cubetime[j+1]))
                else:
                    ### end point (23h)
                    itime = np.where(tim >= cubetime[-1])
                print ''
                print 'For ', str(j), 'h, itime = ', itime
                if dim_flag == 1: dat = np.zeros([len(cube[k].coord('model_level_number').points),len(itime[0])])
                if dim_flag == 0: dat = np.zeros([len(itime[0])])
                for i in range(0, len(itime[0])):                   ### loop over time gridded by ship track
                    if np.size(itime) > 1:
                        # print 'Processing i = ', str(itime[0][i])
                        # print '...'
                        if dim_flag == 1: temp = cube[k][j,:,int(ilat[itime[0][i]] + yoffset),int(ilon[itime[0][i]] + xoffset)]
                        if dim_flag == 0: temp = cube[k][j,int(ilat[itime[0][i]] + yoffset),int(ilon[itime[0][i]] + xoffset)]
                    else:
                        # print 'Processing i = ', str(itime[i])
                        # print '...'
                        if dim_flag == 1: temp = cube[k][j,:,int(ilat[itime[i]] + yoffset),int(ilon[itime[i]] + xoffset)]
                        if dim_flag == 0: temp = cube[k][j,int(ilat[itime[i]] + yoffset),int(ilon[itime[i]] + xoffset)]
                    if dim_flag == 1: dat[:,i] = np.squeeze(temp.data)
                    if dim_flag == 0: dat[i] = np.squeeze(temp.data)
                    if np.size(itime) > 1:
                        if stash_flag == 1: dat[dat==0] = np.nan              # set zeros to nans
                        if dim_flag == 1: data[:,j] = np.nanmean(dat,1)     # mean over time indices
                        if dim_flag == 0: data[j] = np.nanmean(dat)     # mean over time indices
                        # print 'averaging over itime ...'
                        # print ''
                    else:
                        if dim_flag == 1: data[:,j] = np.squeeze(dat)                   # if only one index per hour
                        if dim_flag == 0: data[j] = np.squeeze(dat)                   # if only one index per hour
                        # print 'no averaging, itime = 1 ...'
                        print ''
                # print data
        # print 'data.shape = ', data.shape

        #################################################################
        ## FIGURES TO TEST OUTPUT
        #################################################################
        ### timeseries of lowest model level
        # plt.figure(figsize=(7,5))
        # plt.plot(cubetime[:-1],data[0:10,:])
        # plt.show()

        ### vertical profile of 1st timestep
        # plt.figure(figsize=(7,5))
        # plt.plot(data[:,0],cube.coord('model_level_number').points)
        # plt.show()

        ### pcolormesh of timeseries
        # plt.figure(figsize=(7,5))
        # plt.pcolormesh(cubetime[:-1], cube.coord('model_level_number').points, data)
        # plt.colorbar()
        # plt.show()

        #################################################################
        ## CREATE CUBE
        #################################################################
        ### ECMWF FIELD NAMES
        # field_names = {'forecast_time','pressure','height','temperature','q','rh','ql','qi','uwind','vwind','cloud_fraction',
        #             'wwind','gas_atten','specific_gas_atten','specific_dry_gas_atten','specific_saturated_gas_atten','K2',
        #             'specific_liquid_atten','sfc_pressure','sfc_height_amsl'};
            varname = varnames.findfieldName(stash)
            print 'standard_name = ', cube[k].standard_name
            print 'long name = ', cube[k].long_name
            print 'varname = ', varname
            print ''

            ntime = DimCoord(cubetime[:-1], var_name = 'forecast_time', standard_name = 'time', units = 'h')
            if dim_flag == 1:         ### 4D VARIABLE
                model_height = DimCoord(cube[k].aux_coords[2].points, var_name = 'height', standard_name = 'height', units='m')
                ncube = Cube(np.transpose(data),
                        dim_coords_and_dims=[(ntime, 0),(model_height, 1)],
                        standard_name = cube[k].standard_name,
                        long_name = cube[k].long_name,
                        units = cube[k].units,
                        var_name = varname,
                        attributes = cube[k].attributes,
                        aux_coords_and_dims = None,
                        )
            elif dim_flag == 0:         ### 3D VARIABLE
                ncube = Cube(np.transpose(data),
                        dim_coords_and_dims=[(ntime, 0)],
                        standard_name = cube[k].standard_name,
                        long_name = cube[k].long_name,
                        units = cube[k].units,
                        var_name = varname,
                        attributes = cube[k].attributes,
                        aux_coords_and_dims = None,
                        )
            # ncube.attributes = cube[k].attributes
            # iris.save(ncube, pp_outfile, append=True)
            if k == 0:
                print 'Assigning fcube'
                print ''
                fcube = [ncube]
            else:
                print 'Appending to fcube'
                print ''
                fcube.append(ncube)

        # print fcube

    else:
        print ''
        print 'Only one variable constraint. Proceeding...'
        print ''

        cubetime = np.round(cube.coord('forecast_period').points - 12.0)      ### forecast period (ignore first 12h)
        print ''
        print 'Cube times relative to forecast start:', cubetime[:-1]
        print ''

        #################################################################
        ## CREATE EMPTY CUBE
        #################################################################
        ncube = Cube(np.zeros([len(cube.coord('model_level_number').points),len(cubetime)-1]))

        #################################################################
        ## PROBE VARIABLE
        #################################################################
        ### do we want to average exluding zeros?
        stash_flag, stash = excludeZeros(cube)

        #################################################################
        ## FIND ARRAY SIZE AND CREATE EMPTY NP ARRAY
        #################################################################
        if np.logical_and(np.size(cube.data,1) >= 69, np.size(cube.data,1) < 71):
            print 'Variable is 4D:'
            print ''
            #### create empty arrays to be filled
            data = np.zeros([len(cube.coord('model_level_number').points),len(cubetime)-1])
            dim_flag = 1        ### for next loops
            print 'data.shape = ', str(data.shape)
            print ''
        else:
            print 'Variable is 3D:'
            print ''
            #### create empty arrays to be filled
            data = np.zeros([len(cubetime)-1])
            dim_flag = 0       ### for next loops
            print 'data.shape = ', str(data.shape)
            print ''

        #################################################################
        ## POPULATE NP ARRAY WITH DATA
        #################################################################
        ### populate 0th dimension with time field
        # data[:,0] = cubetime[:,:-1]

        for j in range(0,len(cubetime)-1):
            if j < len(cubetime[:-1]):
                itime = np.where(np.logical_and(tim >= cubetime[j], tim < cubetime[j+1]))
            else:
                ### end point (23h)
                itime = np.where(tim >= cubetime[-1])
            print 'For ', str(j), 'h, itime = ', itime
            if dim_flag == 1: dat = np.zeros([len(cube.coord('model_level_number').points),len(itime[0])])
            if dim_flag == 0: dat = np.zeros([len(itime[0])])
            for i in range(0, len(itime[0])):
                if np.size(itime) > 1:
                    # print 'Processing i = ', str(itime[0][i])
                    if dim_flag == 1: temp = cube[j,:,int(ilat[itime[0][i]] + yoffset),int(ilon[itime[0][i]] + xoffset)]
                    if dim_flag == 0: temp = cube[j,int(ilat[itime[0][i]] + yoffset),int(ilon[itime[0][i]] + xoffset)]
                else:
                    # print 'Processing i = ', str(itime[i])
                    if dim_flag == 1: temp = cube[j,:,int(ilat[itime[i]] + yoffset),int(ilon[itime[i]] + xoffset)]
                    if dim_flag == 0: temp = cube[j,int(ilat[itime[i]] + yoffset),int(ilon[itime[i]] + xoffset)]
                if dim_flag == 1: dat[:,i] = temp.data
                if dim_flag == 0: dat[i] = temp.data
                if np.size(itime) > 1:
                    if stash_flag == 1: dat[dat==0] = np.nan              # set zeros to nans
                    if dim_flag == 1: data[:,j] = np.nanmean(dat,1)     # mean over time indices
                    if dim_flag == 0: data[j] = np.nanmean(dat)     # mean over time indices
                    # print 'averaging over itime...'
                else:
                    if dim_flag == 1: data[:,j] = np.squeeze(dat)                   # if only one index per hour
                    if dim_flag == 0: data[j] = np.squeeze(dat)                   # if only one index per hour
                    # print 'no averaging, itime = 1...'
        # print data
        # print 'data.shape = ', data.shape

        #################################################################
        ## FIGURES TO TEST OUTPUT
        #################################################################
        ### timeseries of lowest model level
        # plt.figure(figsize=(7,5))
        # plt.plot(cubetime[:-1],data[0:10,:])
        # plt.show()

        ### vertical profile of 1st timestep
        # plt.figure(figsize=(7,5))
        # plt.plot(data[:,0],cube.coord('model_level_number').points)
        # plt.show()

        ### pcolormesh of timeseries
        # plt.figure(figsize=(7,5))
        # plt.pcolormesh(cubetime[:-1], cube.coord('model_level_number').points, data)
        # plt.colorbar()
        # plt.show()

        #################################################################
        ## CREATE CUBE
        #################################################################
        ### ECMWF FIELD NAMES
        # field_names = {'forecast_time','pressure','height','temperature','q','rh','ql','qi','uwind','vwind','cloud_fraction',
        #             'wwind','gas_atten','specific_gas_atten','specific_dry_gas_atten','specific_saturated_gas_atten','K2',
        #             'specific_liquid_atten','sfc_pressure','sfc_height_amsl'};

        varname = varnames.findfieldName(stash)
        print 'standard_name = ', cube.standard_name
        print 'long name = ', cube.long_name
        print 'varname = ', varname
        print ''

        ntime = DimCoord(cubetime[:-1], var_name = 'forecast_time', standard_name = 'time', units = 'h')
        if dim_flag == 1:             ### 4D VARIABLE
            model_height = DimCoord(cube.aux_coords[2].points, var_name = 'height', standard_name = 'height', units='m')
            ncube = Cube(np.transpose(data),
                    dim_coords_and_dims=[(ntime, 0),(model_height, 1)],
                    standard_name = cube.standard_name,
                    long_name = cube.long_name,
                    units = cube.units,
                    var_name = varname,
                    )
        elif dim_flag == 0:             ### 3D VARIABLE
            ncube = Cube(np.transpose(data),
                    dim_coords_and_dims=[(ntime, 0)],
                    standard_name = cube.standard_name,
                    long_name = cube.long_name,
                    units = cube.units,
                    var_name = varname,
                    )
        ncube.attributes = cube.attributes
        ### for consistency with multi-diag option
        fcube = ncube

    #################################################################
    ## CREATE NETCDF
    #################################################################

    #################################################################
    ## define output filename
    #################################################################
    print '******'
    print 'Define outfile:'
    # pp_outfile = out_dir + grid_filename[9:17] + '_oden_metum.pp'
    # nc_outfile = out_dir + grid_filename[9:17] + '_oden_metum.nc'
    # pp_outfile = grid_filename[9:17] + '_oden_metum.pp'
    nc_outfile = grid_filename[9:17] + '_oden_metum.nc'
    print 'Outfile = ', nc_outfile

    ### save cube to netcdf file
    print ''
    print 'Writing fcube to NetCDF file:'
    print ''
    # iris.save(fcube, nc_outfile)
    print fcube

    return fcube, nc_outfile

def readCube(name):

    ### LOOP OVER FILENAMES TO EXTRACT DIAGNOSTIC OVER ALL GRIDBOXES

    print 'Filename to load is: ' + name

    diag = 24

    data = {}
    dat = np.zeros([25,137])
    cube = iris.load(name)
    print 'Diag will be ' + cube[diag].var_name
    tims = cube[diag].dim_coords[0].points
    hgts = cube[35].data
    lats = cube[40].data
    lons = cube[41].data
    if np.sum(cube[diag].shape) > 24:        # if 2D diagnostic
        mlevs = cube[diag].dim_coords[1].points
    for t in range(len(tims)):
        dat[t,:] = tims[t]
        for k in range(np.size(hgts,1)):
            dat[:,k] = cube[diag].data[t,k]
    data[cube[diag].var_name] = dat
    data['lats'] = lats
    data['lons'] = lons
    data['tims'] = tims
    data['hgts'] = hgts
    data['mlevs'] = mlevs

    # print data.keys()

    return data, cube, diag

def ReadWriteDaily(filenames, date):

    from iris.coords import DimCoord
    from iris.cube import Cube

    '''
     function to read in each lat/lon ECMWF IFS (netCDF) file with Iris then
     output required diagnostics for Cloudnet into a new netCDF
    '''

    i = -1
    data = {}
    data['pressure'] = np.zeros([38,25,137])
    data['hgts'] = np.zeros([38,25,137])
    data['tims'] = np.zeros([25])
    data['lats'] = np.zeros([38])
    data['lons'] = np.zeros([38])
    data['mlevs'] = np.zeros([137])
    for name in filenames:
        i = i + 1
        print 'i = ' + str(i)
        dat, cube, diag = readCube(name)
        # print dat
        data['pressure'][i, :, :] = dat['pressure'][:, :]
        data['hgts'][i, :, :] = dat['hgts'][:, :]
        data['lats'][i] = dat['lats']
        data['lons'][i] = dat['lons']
    data['tims'][:] = dat['tims'][:]
    data['mlevs'][:] = dat['mlevs'][:]

    #################################################################
    ## CREATE EMPTY CUBE
    #################################################################
    ncube = Cube(np.zeros([38,25,137]))

    data['ulat'] = np.zeros([np.size(np.unique(data['lats'][:]))])
    data['ulat'][:] = np.unique(data['lats'][:])
    data['ulon'] = np.zeros([np.size(np.unique(data['lons'][:]))])
    data['ulon'][:] = np.unique(data['lons'][:])
    mlats, mlons = np.meshgrid(data['ulat'][:], data['ulon'][:])

    ntime = DimCoord(data['tims'][:], var_name = 'time', standard_name = 'time', units='hours since ' + date[0:4] + '-' + date[4:6] + '-' + date[6:8] + ' 00:00:00 +00:00')
    level = DimCoord(data['mlevs'][:], var_name = 'level', standard_name = 'model_level_number', units='m')
    lats = DimCoord(data['ulat'][:], var_name = 'latitude', standard_name = 'latitude', units='degrees_N')
    lons = DimCoord(data['ulon'][:], var_name = 'longitude', standard_name = 'longitude', units='degrees_E')
    # ncube = Cube(data['pressure'][:,:,:],
    #         dim_coords_and_dims=[(lats, 0), (ntime, 1), (level, 2)],
            # standard_name = cube.standard_name,
            # long_name = cube.long_name,
            # units = cube.units,
            # var_name = varname,
            # attributes = cube.attributes,
            # aux_coords_and_dims = None,
            # )

    nc_outfile = date + '_oden_ecmwf_n38.nc'
    # iris.save(ncube, nc_outfile)

    ### write to combined netCDF file
    # data = writeNetCDF(nc_outfile, data, date, cube)

    ### append metadata to combined netCDF file
    # data = appendMetaNetCDF(nc_outfile, date)

    return data, nc_outfile

# def writeNetCDF(outfile, data, date, cube):

    # from iris.coords import DimCoord
    # from iris.cube import Cube
    # import iris.plot as iplt
    #
    # #################################################################
    # ## CREATE EMPTY CUBE
    # #################################################################
    # ncube = Cube(np.zeros([38,25,137]))
    #
    # ntime = DimCoord(data['tims'][:], var_name = 'time', standard_name = 'forecast_time', units='hours since ' + date[0:4] + '-' + date[4:6] + '-' + date[6:8] + ' 00:00:00 +00:00')
    # level = DimCoord(data['mlevs'][:], var_name = 'level', standard_name = 'model_level_number', units='m')
    # ncube = Cube(data['pressure'],
    #         dim_coords_and_dims=[(lats, 0), (level, 1), (ntime, 2)],
    #         standard_name = cube.standard_name,
    #         long_name = cube.long_name,
    #         units = cube.units,
    #         var_name = varname,
    #         attributes = cube.attributes,
    #         aux_coords_and_dims = None,
    #         )


    ###################################
    ## Open new netCDF file
    ###################################

    # dataset = Dataset(outfile, 'w')

    ###################################
    ## Data dimensions
    ###################################
    # tim = dataset.createDimension('time', np.size(data['tims'][:]))
    # Z = dataset.createDimension('level', np.size(data['mlevs']))
    # lat = dataset.createDimension('latitude', np.size(data['lats'][:]))
    # lon = dataset.createDimension('longitude', np.size(data['lons'][:]))
    #
    # ###################################
    # ## Dimensions variables
    # ###################################
    # #### Time
    # print 'Writing time:'
    # print '---'
    # tim = dataset.createVariable('time', np.float32, ('time',),fill_value='-9999')
    # tim.units = 'hours since ' + date[0:4] + '-' + date[4:6] + '-' + date[6:8] + ' 00:00:00 +00:00'
    # tim.long_name = 'Hours UTC'
    # tim.standard_name = 'time'
    # tim[:] = data['tims'][:]
    #
    # #### Z
    # print 'Writing model levels:'
    # print '---'
    # mlevs = dataset.createVariable('level', np.int16, ('level',),fill_value='-9999')
    # mlevs.units = '1'
    # mlevs.long_name = 'Model level'
    # mlevs.positive = 'down'
    # mlevs.standard_name = 'model_level_number'
    # mlevs[:] = data['mlevs'][:]
    #
    # #### Latitude
    # print 'Writing latitudes:'
    # print '---'
    # lats = dataset.createVariable('latitude', np.float32, ('latitude',),fill_value='-9999')
    # lats.units = 'degrees_N'
    # lats.long_name = 'Latitude of model grid point'
    # lats.standard_name = 'latitude'
    # lats[:] = data['lats'][:]
    #
    # #### Longitude
    # print 'Writing longitudes:'
    # print '---'
    # lons = dataset.createVariable('longitude', np.float32, ('longitude',),fill_value='-9999')
    # lons.units = 'degrees_E'
    # lons.long_name = 'Longitude of model grid point'
    # lons.standard_name = 'longitude'
    # lons[:] = data['lons'][:]

    ###################################
    ## Writing out Cloudnet diagnostics
    ###################################
    # print 'Writing pressure:'
    # print '---'
    # pres = dataset.createVariable('pressure', np.float64, ('latitude','time','level'), fill_value='-9999')
    # pres.scale_factor = float(1)
    # pres.add_offset = float(0)
    # pres.units = 'Pa'
    # pres.long_name = 'air_pressure'
    # pres[:,:] = data['pressure'][:,:]

    # print 'Appending LWP:'
    # print '---'
    # lwp = dataset.createVariable('LWP', np.float64, ('forecast_time',), fill_value='-9999')
    # lwp.scale_factor = float(1)
    # lwp.add_offset = float(0)
    # lwp.units = 'kg m-2'
    # lwp.long_name = 'large_scale_liquid_water_path'
    # lwp[:] = nc.variables['LWP'][:]
    #
    # print 'Appending rainfall_flux:'
    # print '---'
    # rain = dataset.createVariable('rainfall_flux', np.float64, ('forecast_time',), fill_value='-9999')
    # rain.scale_factor = float(1)
    # rain.add_offset = float(0)
    # rain.units = 'kg m-2 s-1'
    # rain.long_name = 'stratiform_rainfall_flux'
    # rain[:] = nc.variables['rainfall_flux'][:]
    #
    # print 'Appending snowfall_flux:'
    # print '---'
    # snow = dataset.createVariable('snowfall_flux', np.float64, ('forecast_time',), fill_value='-9999')
    # snow.scale_factor = float(1)
    # snow.add_offset = float(0)
    # snow.units = 'kg m-2 s-1'
    # snow.long_name = 'stratiform_snowfall_flux'
    # snow[:] = nc.variables['snowfall_flux'][:]
    #
    # print 'Appending surface_pressure:'
    # print '---'
    # sfc_pressure = dataset.createVariable('sfc_pressure', np.float64, ('forecast_time',), fill_value='-9999')
    # sfc_pressure.scale_factor = float(1)
    # sfc_pressure.add_offset = float(0)
    # sfc_pressure.units = 'Pa'
    # sfc_pressure.long_name = 'surface_pressure'
    # sfc_pressure[:] = nc.variables['sfc_pressure'][:]
    #
    # print 'Appending surface_temperature:'
    # print '---'
    # sfc_temperature = dataset.createVariable('sfc_temperature', np.float64, ('forecast_time',), fill_value='-9999')
    # sfc_temperature.scale_factor = float(1)
    # sfc_temperature.add_offset = float(0)
    # sfc_temperature.units = 'K'
    # sfc_temperature.long_name = 'surface_temperature'
    # sfc_temperature[:] = nc.variables['sfc_temperature'][:]

    ###################################
    ## Write out file
    ###################################
    # dataset.close()
    #
    # return dataset

def appendMetaNetCDF(outfile, date):

    from netCDF4 import num2date, date2num
    import time
    from datetime import datetime, timedelta

    print '******'
    print ''
    print 'Appending metadata to ' + outfile
    print ''

    ###################################
    ## Open File
    ###################################
    dataset = Dataset(outfile, 'a', format ='NETCDF4_CLASSIC')
    # infile = net.Dataset("2015%s%s-160000_0.nc" % (month,day), "a")
    print ''
    print dataset.file_format
    print ''

    ###################################
    ## Global Attributes
    ###################################
    dataset.conventions = 'CF-1.0'
    dataset.title = 'ECMWF Model single-site output during MOCCHA'
    dataset.location = 'MOCCHA'
    # dataset.description = 'Hourly data taken from grid box closest to ship location. Where the ship covers more than one grid box within an hour period, data are averaged from all grid boxes crossed.'
    dataset.description = 'Hourly data combined from n=38 files into 1 daily file.'
    dataset.history = 'ke 5.6.2019 14.09.20 +0300 - NetCDF generated from original data by Ewan O''Connor <ewan.oconnor@fmi.fi> using cnmodel2nc on cloudnet.fmi.fi. Combined from n=38 lat/lon files at ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' by Gillian Young <G.Young1@leeds.ac.uk> using Python (Iris).'
    dataset.source = 'ECMWF Integrated Forecast System (IFS)'
    dataset.references = ''
    dataset.project = 'MOCCHA: Microbiology-Ocean-Cloud Coupling in the High Arctic.'
    dataset.comment = ''
    dataset.institution = 'European Centre for Medium-Range Weather Forecasting.'
    # dataset.initialization_time = outfile[0:4] + '-' + outfile[4:6] + '-' + outfile[6:8]) + ' 00:00:00 UTC.'
    dataset.initialization_time = date[0:4] + '-' + date[4:6] + '-' + date[6:8] + ' 00:00:00 +00:00'

    dataset.close()

    return dataset

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
    ### DESKTOP

    if platform == 'JASMIN':
        root_dir = '/gws/nopw/j04/ncas_weather/gyoung/MOCCHA/ECMWF/'
        ship_filename = '~/GWS/MOCCHA/ODEN/2018_shipposition_1hour.txt'
    if platform == 'LAPTOP':
        root_dir = '/home/gillian/MOCCHA/ECMWF/DATA/'
        ship_filename = '/home/gillian/MOCCHA/ODEN/DATA/2018_shipposition_1hour.txt'
    if platform == 'DESKTOP':
        root_dir = '/nfs/a96/MOCCHA/working/data/ecmwf_ewan/moccha/ecmwf-all/2018/'
        ship_filename = '/nfs/a96/MOCCHA/working/gillian/ship/2018_shipposition_1hour.txt'

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

    # # -------------------------------------------------------------
    # # Load data
    # # -------------------------------------------------------------
    print '******'
    print ''
    print 'Begin data read in at ' + time.strftime("%c")
    print ' '

    ### -------------------------------------------------------------------------
    ### define input filenames
    ### -------------------------------------------------------------------------
    date = '20180901'
    base_name = date + '_moccha_ecmwf_'
    names = [None] * 38         ## 'empty' list of 38 elements. can assign index without list.append
    filenames = [None] * 38
    for i in range(0,38):
        id = i+1
        str_i = "%03d" % id
        names[i] = base_name + str_i + '.nc'
        filenames[i] = root_dir + names[i]

    print filenames[0] + ' ... ' + filenames[-1]
    print ''

    # -------------------------------------------------------------
    # Find ECMWF grid
    # -------------------------------------------------------------
    lats = np.zeros([38])
    lons = np.zeros([38])
    tim = np.zeros([24])
    for i in range(0,38):
        lats[i], lons[i], tim = pullLatLon(filenames[i])

    print 'Lats = ' + str(lats)
    print 'Lons = ' + str(lons)

    # -------------------------------------------------------------
    # Extract each position file with Iris and write to combined netCDF
    # -------------------------------------------------------------
    data, outfile = ReadWriteDaily(filenames, date)

    # -------------------------------------------------------------
    # Plot data (map)
    # -------------------------------------------------------------
    # map = plot_basemap(ship_data, lats, lons, tim)

    # -------------------------------------------------------------
    # Plot data (cartopy map)
    # -------------------------------------------------------------
    map = plot_cartmap(ship_data, data, date)

    # -------------------------------------------------------------
    # Pull daily gridded ship track from netCDFs
    # -------------------------------------------------------------
    # edgelats, edgelons = designGrid(lats, lons, tim)
    # ship_ind = checkLatLon(ship_data, lats, lons, date, tim)

    #### LOAD CUBE
    # if con_flag == 0: fcube, outfile = pullTrack(cube, grid_filename, var_con)
    # if con_flag == 1: fcube, outfile = pullTrack(cube, grid_filename, global_con)
    # ## Update netCDF comments
    # out = appendNetCDF(outfile)
    # # final_outfile = out_dir + grid_filename[9:17] + '_oden_metum.nc'
    # # os.rename(outfile, final_outfile)

    # print outfile

    END_TIME = time.time()
    print '******'
    print ''
    print 'End: ' + time.strftime("%c")
    print ''

    #### DIAGNOSTICS TO CHOOSE FROM:

#     dimensions(sizes): time(25), level(137), flux_level(138), frequency(2)
#     variables(dimensions): float32 latitude(), float32 longitude(),
#           float32 horizontal_resolution(), float32 time(time), float32 forecast_time(time),
#           int16 level(level), int16 flux_level(flux_level), float32 pressure(time,level),
#           float32 uwind(time,level), float32 vwind(time,level), float32 omega(time,level),
#           float32 temperature(time,level), float32 q(time,level), float32 rh(time,level),
#           float32 ql(time,level), float32 qi(time,level), float32 cloud_fraction(time,level),
#           float32 flx_net_sw(time,flux_level), float32 flx_net_lw(time,flux_level),
#           float32 flx_down_sens_heat(time,flux_level), float32 flx_turb_moist(time,flux_level),
#           float32 flx_ls_rain(time,flux_level), float32 flx_ls_snow(time,flux_level),
#           float32 flx_conv_rain(time,flux_level), float32 flx_conv_snow(time,flux_level),
#           float32 flx_turb_mom_u(time,flux_level), float32 flx_turb_mom_v(time,flux_level),
#           float32 sfc_pressure(time), float32 sfc_net_sw(time), float32 sfc_net_lw(time),
#           float32 sfc_down_sw(time), float32 sfc_down_lw(time), float32 sfc_cs_down_sw(time),
#           float32 sfc_cs_down_lw(time), float32 sfc_down_lat_heat_flx(time),
#           float32 sfc_down_sens_heat_flx(time), float32 sfc_ls_rain(time),
#           float32 sfc_conv_rain(time), float32 sfc_ls_snow(time), float32 sfc_conv_snow(time),
#           float32 sfc_ls_precip_fraction(time), float32 sfc_cloud_fraction(time),
#           float32 sfc_bl_height(time), float32 sfc_albedo(time), float32 sfc_temp_2m(time),
#           float32 sfc_q_2m(time), float32 sfc_rough_mom(time), float32 sfc_rough_heat(time),
#           float32 sfc_skin_temp(time), float32 sfc_wind_u_10m(time), float32 sfc_wind_v_10m(time),
#           float32 sfc_geopotential(time), float32 height(time,level), float32 sfc_height_amsl(time),
#           float32 flx_height(time,flux_level), float32 wwind(time,level), float32 frequency(frequency),
#           float32 gas_atten(frequency,time,level), float32 specific_gas_atten(frequency,time,level),
#           float32 specific_saturated_gas_atten(frequency,time,level),
#           float32 specific_dry_gas_atten(frequency,time,level), float32 K2(frequency,time,level),
#           float32 specific_liquid_atten(frequency,time,level)



if __name__ == '__main__':

    main()
