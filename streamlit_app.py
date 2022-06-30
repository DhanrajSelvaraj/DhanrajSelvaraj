
import matplotlib.pyplot as plt
import time

from datetime import date
# from datetime import time
import pandas as pd
from clustering_function import clustering
from anomaly_removal import anomalyremoval
from dataset_preparation import dataset
from curve_fitting import curve_fitting
from plot_watercut import plot_watercut
from plot_forecast import plot_forecast
from water_cut import water_forecast
from water_cut import find_watercut
from plot_rates import plot_rates
import sys
from forecaste_values_func import forecast_values_function
import xlsxwriter
import os
import matplotlib
import logging
import re
import shutil
import os
from openpyxl import load_workbook
import random


from datetime import datetime

# datetime object containing current date and time
now = datetime.now()


dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

start_time = time.time()
today = date.today()


# create folder to save outputs

# D:\Work Done_Abhijith\DCA\PycharmProjects\DCA



if os.path.exists("D:/Work Done_Abhijith/DCA/PycharmProjects/DCA/output"):
    path = 'D:/Work Done_Abhijith/DCA/PycharmProjects/DCA/output'
    shutil.rmtree(path)

if not os.path.exists("D:/Work Done_Abhijith/DCA/PycharmProjects/DCA/output"):

    directory = "output"

    # Parent Directory path
    parent_dir = "D:/Work Done_Abhijith/DCA/PycharmProjects/DCA/"

    # Path
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)


logging.basicConfig(filename="D:/Work Done_Abhijith/DCA/PycharmProjects/DCA/output/"+"logfile.log", level=logging.INFO)
with open('logfile.log', 'w'):
    pass

logging.info("Auto DCA process ran on "+ str(dt_string))

Project = 'Volve' # Input for user, default Project_ name comment
# Project = input()

fluid_type = 'Oil'# User input options Gas or Oil as shown in widget


logging.info("Project: "+ str(Project))

## Input file upload file option

# file = 'E:/inputdata/Boggess_Well_Production.xlsx'
# file = 'E:/inputdata/Boggess_Well_Production_csv.csv'
# file = 'E:/inputdata/pdo_new.xlsx'
# file = 'E:/inputdata/5wellsdata_together.xlsx'
# file = 'E:/inputdata/5wellsdata.xlsx'
# file = 'E:/inputdata/pdo_new_csv.csv'
file = 'D:/Work Done_Abhijith/DCA/PycharmProjects/DCA/inputdata/5wellsdata_together.xlsx'


## Check file format
try:
    xls = pd.ExcelFile(file) # reading as xlsx file
    Input_file_format = 'excel'
except:
    try:
        # reading as CSV file
        dfn = pd.read_csv(file)
        Input_file_format = 'csv'
    except:
        print ("Please upload in *.xlsx/*.xls or *.csv formats")

dfn = pd.DataFrame()



if Input_file_format == 'excel':

    xls = pd.ExcelFile(file)
    # print(xls.sheet_names) ## Display all sheets sheet/sheets selection dropdown


    Num_skip_raws = 0
    skip_raws = 'No' # give option to user using slider in UI
    if skip_raws == 'Yes':
        Num_skip_raws = 1  ## give option to user using input option
        # skip_raws = input()


    first_sheet = xls.sheet_names[0]


    # print(first_sheet)
    df0 = pd.read_excel(file, sheet_name=first_sheet, header=Num_skip_raws)


    print(df0.columns)
    print(df0.head())
    try:
        well = 'Well'  # default value well name
        df0['Well'] = df0[well]
    except KeyError:
        try:
            well = 'Well Name'  # user will cho0se from list of columns in dropdown menu from  df0.columns
            df0['Well'] = df0[well]
        except KeyError:
            print('sheet name will be considered as well name')



    # print(df0.columns)
    Rate = 'Oil_rate(stb/d)'  # user will cho0se from list of columns in dropdown menu from  df0.columns



    # print(df0.columns)
    Filter = 'Avg_Choke_size(%)'  # user will select from list of columns in dropdown menu from  df0.columns



    try:
        Date = 'Date'  # default value well name
        df0['Date'] = df0[Date]
    except KeyError:
        Date = 'Date'  # user will cho0se from list of columns shown in dropdown menu from df0.columns
        df0['Date'] = df0[Date]


    water_rate_available = 'Yes'  # Forecast water input yes or no user will chose from slider

    if water_rate_available == 'Yes':
        # print(df0.columns)
        Water_Rate = 'Water_rate(stb/d)'  # user will choose from list of columns printed
        # Water_Rate = 'Water (BBL)'

    for sheet in xls.sheet_names:

        df0 = pd.read_excel(file, sheet_name= sheet, header=Num_skip_raws)


        try:

            df0['Well'] = df0[well]
        except KeyError:

            well = sheet
            df0['Well'] = well

        try:
            df0['Rate'] = df0[Rate]
        except KeyError:
            print("Cant forecast without Rate")
            sys.exit("Error")

        try:

            df0['Filter'] = df0[Filter]
        except KeyError:
            print("Cant forecast without Filter")
            sys.exit("Error")

        try:

            df0['Date'] = df0[Date]

        except KeyError:
            print("Cant forecast without Date")
            sys.exit("Error")

        if water_rate_available == 'Yes':

            if not Water_Rate:
                print("Cant forecast Water_cut ")
                break
            # elif not Oil_Rate:
            #     print("Cant forecast Water_cut ")

            else:
                df0['Water Rate'] = df0[Water_Rate]
                # df0['Oil Rate'] = df0[Oil_Rate]

        dfn = dfn.append(df0)


elif Input_file_format == 'csv':

    df0 = pd.read_csv(file)

    print(df0.head()) # print inside the square lower right in UI dashboard

    skip_raws = 'No'  #  give option to user Yes or No (slider in  UI)

    if skip_raws == 'yes':
        skip_no = input("Number of Raws to skip :")
        skip_no = int(skip_no)
        df0 = pd.read_csv(file, skiprows = skip_no)

    print((df0.columns))

    try:
        well = 'Well'  # user will cho0se from list of column printed above
        df0['Well'] = df0[well]
    except KeyError:

        # well = input("Couldn't find well name, please enter the well name for sheet " + str(selected_sheet) + ":")
        well = 'Well'

        df0['Well'] = well

    print(df0.columns)
    try:
        Rate = 'Gas(scf/d)'  # user will cho0se from list of column printed above

        df0['Rate'] = df0[Rate]
    except KeyError:
        print("Cant forecast without Rate")
        sys.exit("Error")

    try:
        Filter = 'FTHP(Bar)'  # user will select from list of column printed above
        df0['Filter'] = df0[Filter]


    except KeyError:
        print("Cant forecast without Filter")
        sys.exit("Error")
    try:
        Date = 'Date'  # user will select from list of column printed above

        df0['Date'] = df0[Date]

    except KeyError:
        print("Cant forecast without Date")
        sys.exit("Error")



    water_rate_available = 'NO'  # Forecast water input yes or no
    if water_rate_available == 'Yes':

        print(df0.columns)

        Water_Rate = 'Water_rate(stb/d)'  # user will choose from list of columns printed


        if not Water_Rate:
            print("Cant forecast Water_cut ")


        else:
            df0['Water Rate'] = df0[Water_Rate]
            # df0['Oil Rate'] = df0[Oil_Rate]

    dfn = dfn.append(df0)
    dfn['Date'] = pd.to_datetime(dfn['Date'])




syl_all = []
eps_all = []

print(dfn.head())

A = dfn['Well'].unique()



input_file_name = re.split('\\binputdata/\\b',file)[-1]

logging.info("Input File Name: " + str(input_file_name))


new = pd.DataFrame()
dfn = dataset(dfn)

A = dfn['Well'].unique()

Anew = []

print(A)
selected_wells = ['F14','F12'] # option to user to select the wells  from  available wells using dropdown in UI based on print(A)


for well in selected_wells:

    Anew.append(well)
A = Anew

new = pd.DataFrame()
est = 10
new = pd.DataFrame()

cmap = matplotlib.pyplot.cm.jet
cmaplist = [cmap(i) for i in range(cmap.N)]
cmaplist[0] = (.5, .5, .5, 1.0)


input_data_all = pd.DataFrame()
anomaly_removed_all = pd.DataFrame()
clustered_data_all = pd.DataFrame()
All_data_all = pd.DataFrame()

forecast_values_all = pd.DataFrame()
forecast_values_water = pd.DataFrame()

wells=A

wells_completed = []
eps_all  = []
dfn1 = pd.DataFrame()

cont_all = []

for well in A:

    print(well) # print this name in the box shown in the UI in well box

    remaining_wells = list(set(A).difference(wells_completed))

    df = dfn[dfn['Well'] == well]

    # y1 = max(df['Rate'])
    # y2 = min(df['Rate'])

    y1 = max(df['Rate'])
    y = min(df['Rate'])
    y2 = y - ((y1-y)/20)

    start_date_prod = df['Date'].min()
    end_date_prod = df['Date'].max()

    try:
        while True:

            cont = 0.1 # Contamination option to user to select from range 0 - 0.5 in data using the slider


            df_input = df[["Rate", "Filter", "Well", "Date", "Days"]]

            if water_rate_available == 'Yes':
                df_input["Water Rate"] = df["Water Rate"]

            df_input = df_input.fillna(0)

            start1 = time.time()


            df1, iso_df = anomalyremoval(df_input, est, cont)

            end1 = time.time()
            time1 = end1 - start1
            plot_rates(df, df1, y2, y1, fluid_type, Project, well)

            freeze = 'Yes'  # " Yes or No,  Freeze if answer is Yes using freeze buton in UI"

            if freeze.upper() == "No":  # go back to the top again
                continue


            break  # exit
        print("Model Building ... ") # to be shown in UI

        # need to discuss regarding Asynchronous process impementation with API developer


        df_no_anamolies, db_df, eps, syl_all, eps_all = clustering(df1,syl_all, eps_all)
        dfn1 = dfn1.append(df_no_anamolies)
        input_data_all = input_data_all.append(df_input)
        cont_all.append(cont)
        # anomaly_removed_all = anomaly_removed_all.append(df1)
    except KeyError:

        print('Key error')

    wells_completed.append(well)




A = dfn1['Well'].unique()

A= list(A)


wells_completed = []

# for well in A:
for i in range(len(A)):
    well = A[i]
    print(well)

    remaining_wells = list(set(A).difference(wells_completed))

    dfn2 = dfn1[dfn1['Well'] == well]
    start2 = time.time()
    forecast_values = pd.DataFrame()
    start_date_forecast = dfn2['Date'].max()

    start_date_prod = dfn2['Date'].min()
    end_date_prod = dfn2['Date'].max()

    y1 = max(dfn2['Rate'])
    y = min(dfn2['Rate'])
    y2 = y - ((y1-y)/20)


    end2 = time.time()
    time2 = end2 - start2

    while True:


        CurveFitting_method = 'Exponential'  #  User to  select from options Exponential, Harmonic and Hyperbolic as shown in UI

        if CurveFitting_method == 'Exponential':
            method = 0
        elif CurveFitting_method == 'Harmonic':
            method = 2
        elif CurveFitting_method == 'Hyperbolic':
            method = 1


        startDate = start_date_forecast
        number_of_years = 5 # years option for user to select from range 0-5 using slider in UI
        forecast_date = startDate.replace(startDate.year + number_of_years)

        Rate_cut_off = 0  # option to user till what rate the production will happen, default =0,
        change_rate_cut_off = 'Yes'
        if change_rate_cut_off == 'Yes':
            Rate_cut_off = 0
            #

        start3 = time.time()

        v_fit, curve_data, dataset, final1 = curve_fitting(dfn2, method)


        forecast_values = forecast_values_function(curve_data, dataset, start_date_forecast, final1,
                                                   forecast_values, method,
                                                   forecast_date, Rate_cut_off, well)

        end3 = time.time()
        time3 = end3 - start3



        All_data = plot_forecast(curve_data, dataset, start_date_forecast, final1, forecast_values, method, y2,
                      y1, cmap,
                      forecast_date, Rate_cut_off, well, fluid_type, dfn2, Project)


        All_data['Well'] = well

        freeze = 'Yes'#" Yes or No,  Freeze if answer is No using freeze buton in UI"



        if freeze.upper() == "No":  # go back to the top again
            continue
        # print("Curve fitting saved")
        clustered_data_all = clustered_data_all.append(dfn2)
        All_data_all = All_data_all.append(All_data)
        break  # exit




    if water_rate_available == 'Yes':

        dfn2 = find_watercut(dfn2)
        water_forecaste_values = pd.DataFrame()

        diff = forecast_date - start_date_forecast
        days = diff.days
        water_curve_data, Forecast_water = water_forecast(dfn2, start_date_forecast, days, well)


        Forecast_water1 = Forecast_water[Forecast_water['Date'] >= end_date_prod]
        forecast_values_water = forecast_values_water.append(Forecast_water1)
        plot_watercut(dfn2, forecast_date, water_curve_data, Forecast_water, Project, well)

    wells_completed.append(well)
    logging.info("Well Name: " + str(well))
    logging.info("Input Parameters")
    logging.info("Contamination: "+ str(cont_all[i]))
    logging.info("CurveFitting method: " + str(CurveFitting_method))
    logging.info("Rate cut off : " + str(Rate_cut_off))
    logging.info("Input Date ranges : " + str(start_date_prod) + ' to ' + str(end_date_prod ))
    logging.info("Forecast Date ranges : " + str(start_date_forecast) + ' to ' + str(forecast_date))



    forecast_values1 = forecast_values[forecast_values['Date'] >= end_date_prod]
    forecast_values_all = forecast_values_all.append(forecast_values1)


#
# print(syl_all)
# print(eps_all)



A = dfn1['Well'].unique()

anomaly_removed_all = dfn1

# newdf = pd.dataframe
for well in A:

    input_data_all1 = input_data_all[input_data_all['Well'] == well]
    anomaly_removed_all1 = anomaly_removed_all[anomaly_removed_all['Well'] == well]
    clustered_data_all1 = clustered_data_all[clustered_data_all['Well'] == well]
    forecast_values_all1 = forecast_values_all[forecast_values_all['Well'] == well]
    All_data_all1 = All_data_all[All_data_all['Well'] == well]

    # newdf["Date"] = clustered_data_all1[Date]
    #
    # All_New1 = pd.merge(clustered_data_all1, forecast_values_all1, on='Date', how='outer')



    out_path = "D:/Work Done_Abhijith/DCA/PycharmProjects/DCA/output/" + Project + '_' + well + "_data.xlsx"
    writer = pd.ExcelWriter(out_path, engine='xlsxwriter')
    input_data_all1.to_excel(writer, sheet_name='Input_data')
    anomaly_removed_all1.to_excel(writer, sheet_name='Anomaly_removed')
    clustered_data_all1.to_excel(writer, sheet_name='Clustered')
    All_data_all1.to_excel(writer, sheet_name='Curve-fit')
    # All_New1.to_excel(writer, sheet_name='Forecast-fit')

    writer.save()

    forecast_values_all1.to_excel("D:/Work Done_Abhijith/DCA/PycharmProjects/DCA/output/" + Project + '_' + well + "_Rate_forecast.xlsx")

    if water_rate_available == 'Yes':
        forecast_values_water1 = forecast_values_water[forecast_values_water['Well'] == well]

        forecast_values_water1.to_excel("D:/Work Done_Abhijith/DCA/PycharmProjects/DCA/output/" + Project + '_' + well + "_water_forecast.xlsx")

logging.info("Total Process Time: " + str(time.time()-start_time)+" seconds")

