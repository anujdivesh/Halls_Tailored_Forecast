from download_waves import generate_waves
from download_gfs import generate_gfs, get_start_date, interpolate_gfs
from download_tides import generate_tides
from msl import msl_plots
from plotter import produce_report
import pandas as pd
from maileroffice import send_email
import os

#CONFIG
#now = '2023060200'
import datetime as dt
now = dt.datetime(2023,6,6,12)

def hallsTailoredForecast(now):
    #CONFIGURE HERE !!!!!!!!!!!!!!!!
    matfile = '../runs/'+now.strftime("%Y") + now.strftime("%m") + now.strftime("%d") +  now.strftime("%H") +'/output.mat'
    tideFolder = '../tmp/'
    gfsDataDir = '../Regional_tmp/out'
    location_pts_csv = '../extras/Hall_output_pts.csv' 
    
    #GET Locations
    df = pd.read_csv(location_pts_csv)

    #Remove files 
    try:
        print('removing files')
        os.remove('dataset.csv')
        os.remove('gfs_3hourly_interpolated.csv')
        os.remove('gfs_3hourly.csv')
        os.remove('tide_data.csv')
        for file in os.listdir('.'):
            if file.endswith('.pdf'):
                os.remove(file) 
    except:
        pass

    document_arr = []
    for index, row in df.iterrows():
    
        tide_name = row['atoll']
        document_arr.append(str(tide_name)+'.pdf')
        lon = row['lon']
        lat = row['lat']
        namesplit =tide_name.split('_')
        factor = ' Ocean' if namesplit[1] == 'Fun' else ''
        proper_name = namesplit[1]+" "+namesplit[2]+factor

        #DOWNLOAD WAVES
        rows_to_remove = 48
        generate_waves(lon, lat, rows_to_remove,matfile)

        #DOWNLOAD GFS
        generate_gfs(lon, lat,gfsDataDir)
        interpolate_gfs()
        start_date = get_start_date()

        ##DOWNLOAD TIDES
        generate_tides(tide_name, start_date,tideFolder)

        ##CREATE MAPS
        factor = 1 if start_date.hour == 12 else 0
        msl_plots(1,gfsDataDir)

        ####PLOTTER#####
        produce_report(tideFolder, str(tide_name)+'.pdf',proper_name,lat,lon,tide_name)

        print('Report Generated Successfully!')

    #SEND EMAIL
    #receipients=['moritzw@spc.int']
    receipients=['divesha@spc.int','moritzw@spc.int','antonioh@spc.int','herveda@spc.int','zulfikarb@spc.int','mativano94@gmail.com','tuvmet@gmail.com','tauala.k@gmail.com']
    send_email(document_arr, receipients)
    print('Email Send Successfully!')

#hallsTailoredForecast(now)