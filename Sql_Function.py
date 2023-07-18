# App de Mansfield with Python Streamlit
# IIOT Climate control Mansfield
# May-2023
# ----------------------------------------------------------------------------------------------------------------------
# Libraries
import datetime
import os

from io import BytesIO
import numpy as np
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


# ----------------------------------------------------------------------------------------------------------------------
# Function definition
def find_load(tipo, day, ini, database, table, redownload):
    """
    Función que busca y carga el archivo de datos si este ya ha sido descargado. En caso contrario
    lo descarga a través de la función sql_connet
    INPUT:
        tipo: ["day_planta", "rango_planta"].
        day: día final o unico día a analizar como STR ("2023-03-30").
        ini: día inicial a analizar en el rango como STR ("2023-12-28").
        database: base de dato a la cual se debe conectar.
        table: tabla a la cual se debe conectar.
        redownload = TRUE or FALSE statement si es TRUE se omite la parte de buscar el archivo y se
        descarga nuevamente.
    OUTPUT:
        pd_sql: dataframe con los datos buscados o descargados
    """
    # Setting the carpet a search
    directory = './Data/Raw/' + day[:-3] + '/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    filenames = os.listdir(directory)

    # Empty dataframe
    pd_sql = pd.DataFrame()

    if tipo == "day":
        # Create the name of the file to search
        filename = table + '_' + day + '.csv'
        if filename in filenames and redownload is False:
            pd_sql = load_data(folder=directory, filename=filename)
        else:
            pd_sql = sql_connect(tipo, day, database, table)

    elif tipo == 'rango_planta':
        # Date init
        l_ini_n = [int(x) for x in ini.split("-")]
        ini_date = datetime.date(l_ini_n[0], l_ini_n[1], l_ini_n[2])
        # Date end
        l_day_n = [int(x) for x in day.split("-")]
        day_date = datetime.date(l_day_n[0], l_day_n[1], l_day_n[2])

        # Recorded the days of this period of time
        while ini_date <= day_date:
            # Setting the folder where to search
            directory = './Data/Raw/' + str(ini_date)[:-3] + '/'
            if not os.path.exists(directory):
                os.makedirs(directory)
            filenames = os.listdir(directory)

            # Create the name of the file to search
            filename = table + '_' + str(ini_date) + '.csv'
            if filename in filenames and redownload is False:
                aux = load_data(folder=directory, filename=filename)
            else:
                aux = sql_connect(tipo="day", day=str(ini_date), database=database, table=table)

            pd_sql = pd.concat([pd_sql, aux])
            # Avant a day
            ini_date = ini_date + datetime.timedelta(days=1)

    return pd_sql


@st.cache_data(experimental_allow_widgets=True, show_spinner=True)
# @st.experimental_memo(suppress_st_warning=True, show_spinner=True)
def get_data_day(sel_dia="2023-01-01", sql_table="Mansfield_climati_cbc", flag_download=False):
    """
    Programa que permite conectar con una base de dato del servidor y devuelve la base de dato
    como un pandas dataframe
    INPUT:
        sel_dia = Día inicial EN STR
        sql_table = Selección de la tabla SQL a la que se conectara
        redownload = Debe descargarse la data o buscar dentro de los archivos previamente descargados.
    OUTPUT:
        df = pandas dataframe traído de la base de dato SQL
        health_list = lista con el dato de salud por día
        health_data = Número | Salud total de los datos
        title = Título para la gráfica
    """

    # Connection BD
    if sql_table in ['CBC 1-8', 'CBC 10-12']:
        df = find_load(tipo='day', day=str(sel_dia), ini=None, database='Mansfield_climati_cbc',
                       table='Mansfield_climati_cbc', redownload=flag_download)

    # Organization df
    df = organize_df(df, sql_table)
    datos_dias = 24 * 60 * 2  # 24 hours a day x 60 minutes in every hour x 2 times I take a data in each minute

    # Defining the title and filename for saving the plots
    title = f"Graph Mansfield {sel_dia}"

    # Health the data
    health_data = (df.shape[0] / datos_dias) * 100
    health_list = [np.round(health_data, 2)]

    return df, health_list, health_data, title


@st.cache_data(experimental_allow_widgets=True, show_spinner=True)
# @st.experimental_memo(suppress_st_warning=True, show_spinner=True)
def get_data_range(sel_dia_ini="2023-05-29", sel_dia_fin="2023-05-30", sql_table="Mansfield_climati_cbc",
                   flag_download=False):
    """
    Programa que permite conectar con una base de dato del servidor y devuelve la base de dato como un pandas dataframe
    del periodo de fecha ingresado
    INPUT:
        sel_dia_ini = Día inicial en STR ("2022-01-01")
        sel_dia_fin = Día final en STR ("2022-01-02")
        sql_table = Selección de la tabla SQL de climatización a la que se conectara
        redownload = Debe descargarse la data o buscar dentro de los archivos previamente descargados
    OUTPUT:
        df = pandas dataframe traído de la base de dato SQL
        health_list = lista con el dato de salud por día
        health_data = Número | Salud total de los datos.
        title = Título para la gráfica
        """

    datos_dias = 24 * 60 * 2  # 24 hours a day x 60 minutes in every hour x 2 times I take a data in each minute

    # Connection BD SQL
    if sql_table in ['CBC 1-8', 'CBC 10-12']:
        df = find_load(tipo="rango_planta", ini=str(sel_dia_ini), day=str(sel_dia_fin),
                       database="Mansfield_climati_cbc", table="Mansfield_climati_cbc", redownload=flag_download)
    # Organizing the raw DF
    df = organize_df(df, sql_table)

    # Defining the title and filename for saving the plots
    title = "Graph climate between " + str(sel_dia_ini) + " and " + str(sel_dia_fin)
    # Health of each day in period
    health_list = []
    while sel_dia_ini <= sel_dia_fin:
        df_filter = df.loc[(df.index >= str(sel_dia_ini) + ' 00:00:00') &
                           (df.index <= str(sel_dia_ini) + ' 23:59:59')]
        salud_dia = np.round((df_filter.shape[0] / datos_dias) * 100, 2)
        health_list.append(salud_dia)

        # Avant a day
        sel_dia_ini = sel_dia_ini + datetime.timedelta(days=1)

    health_data = sum(health_list) / len(health_list)

    return df, health_list, health_data, title


def load_data(folder="./data/", filename="Mansfield_climati_cbc-03-30.csv"):
    """
    Función que carga el archivo csv guardado al conectar con la base de datos y devuelve un
    dataframe
    """
    df = pd.read_csv(folder + filename)

    return df


def organize_df(df, sql_table):
    """
    Función que organiza el data frame, generando nuevas columnas de informaciónd e fechas, reorganizando las columnas
    y redodeando los valores a 2 cifras decimales.
    INPUT:
        df = data frame original
        sql_table = Selección de la tabla SQL de climatización a la que se conectara
    OUTPUT:
        df = data frame  reorganizado
    """
    # Organizer date
    df["fecha"] = pd.to_datetime(df['fecha'], format='%Y/%m/%d', exact=False)
    df['fecha'] += pd.to_timedelta(df["hora"], unit='h')
    df['fecha'] += pd.to_timedelta(df["minuto"], unit='m')
    df['fecha'] += pd.to_timedelta(df["segundo"], unit='s')

    # Separate the years, months y days
    df["año"] = df["fecha"].dt.year
    df["n_dia"] = df["fecha"].dt.day_name()
    df["mes"] = df["fecha"].dt.month
    df["dia"] = df["fecha"].dt.day

    if sql_table in ['CBC 1-8', 'CBC 10-12']:
        # Organize columns
        re_columns = ['fecha', 'hora', 'minuto', 'segundo', 'Z1_T', 'Z2_T', 'Z3_T', 'Z1_HR', 'Z2_HR', 'Z3_HR',
                      'HA1_T_Iny', 'HA1_T_Rec', 'HA1_T_Fac', 'HA1_T_AHA', 'HA1_T_OUT', 'HA2_T_Iny', 'HA2_T_Rec',
                      'HA2_T_Fac', 'HA2_T_AHA', 'HA2_T_OUT', 'HA1_2_OUT_HR', 'HA1_Dmp_Vout', 'HA1_Dmp_Vrec',
                      'HA1_Dmp_Vfac', 'HA2_Dmp_Vout', 'HA2_Dmp_Vrec', 'HA2_Dmp_Vfac', 'año', 'n_dia', 'mes', 'dia']
        df = df[re_columns]
        # Renaming the columns
        df.columns = ['Date', 'hora', 'minuto', 'segundo', 'Z1_T', 'Z2_T', 'Z3_T', 'Z1_HR', 'Z2_HR', 'Z3_HR',
                      'HA1_T_Iny', 'HA1_T_Rec', 'HA1_T_Fac', 'HA1_T_AHA', 'HA1_T_OUT', 'HA2_T_Iny', 'HA2_T_Rec',
                      'HA2_T_Fac', 'HA2_T_AHA', 'HA2_T_OUT', 'HA1_2_OUT_HR', 'HA1_Dmp_Vout', 'HA1_Dmp_Vrec',
                      'HA1_Dmp_Vfac', 'HA2_Dmp_Vout', 'HA2_Dmp_Vrec', 'HA2_Dmp_Vfac', 'año', 'n_dia', 'mes', 'dia']

        # Round the complete dataframe
        df = df.round(2)

    # Ordeno la data por la fecha
    df = df.sort_values(by='Date', ascending=True)
    # Fecha pasa a ser el index
    df.set_index("Date", inplace=True, drop=False)

    return df


def sql_connect(tipo="day", day="023-03-30", database='Mansfield_climati_cbc', table="Mansfield_climati_cbc"):
    """
    Programa que permite conectar con una base de dato del servidor y devuelve la base
    de dato como un pandas dataframe
    INPUT:
        tipo = ["day_planta", "day"]
        day = Día a descargar en  STR ("2021-04-28")
        database: base de dato a la cual se debe conectar
        table: tabla a la cual se debe conectar
    OUTPUT:
        pd_sql = pandas dataframe traído de la base de dato SQL
    """
    # Connection keys
    load_dotenv('./.env')

    server = os.environ.get("SERVER")
    username = os.environ.get("USER_SQL")
    password = os.environ.get("PASSWORD")

    # Connecting to the sql database
    connection_str = f'DRIVER={{SQL SERVER}};SERVER={server};DATABASE={database}; UID={username};PWD={password}'
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_str})

    conn = create_engine(connection_url)
    # -----------------------------------------------------------------------------------------------
    # Tipos de conexiones establecidas para traer distintas cantidades de datos
    # -----------------------------------------------------------------------------------------------
    if tipo == "day":
        pd_sql = pd.read_sql_query("SELECT * FROM " + database + ".dbo." + table + " WHERE fecha like '"
                                   + day + "'", conn)
        # Guardando los datos en archivos estaticos
        if day == str(datetime.date.today()):
            pass  # No guardar datos si el día seleccionado es el día actual del sistema
        else:
            # Checking and creating the folder
            folder = day[:-3]
            if not os.path.exists('./Data/Raw/' + folder):
                os.makedirs('./Data/Raw/' + folder)
            # Saving the raw data
            pd_sql.to_csv('./Data/Raw/' + folder + '/' + table + '_' + day + '.csv', index=False)

    return pd_sql


def add_day(day, add=1):
    """
    Función agrega o quita dias, teniendo en cuenta inicio de mes e inicio de año
    INPUT
        day = "2023-03-01"  EN STRING
    OUTPUT
        ini_date = día entregado en STR
        fin_date = día con los días sumados o restados en STR al día ingresado
    """
    l_day_n = [int(x) for x in day.split("-")]
    ini_date = datetime.date(l_day_n[0], l_day_n[1], l_day_n[2])
    fin_date = ini_date + datetime.timedelta(days=add)

    return str(ini_date), str(fin_date)


def to_excel(df):
    """
    Función para agregar los datos a un excel y poder descargarlo
    INPUT
        df: data frame
    OUTPUT
        file: archivo a descargar
    """
    # Create object BytesIO empty
    output = BytesIO()

    # Create object ExcelWriter and write DataFrame en la hoja 'Mansfield_climati_cbc'
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Mansfield_climati_cbc')

    # Save file in Excel
    writer.book.close()
    # writer.save()

    # Get the Excel file and return it
    archivo = output.getvalue()

    return archivo
