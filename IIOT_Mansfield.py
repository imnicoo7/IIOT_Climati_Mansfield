# App Climate control Mansfield with Python Streamlit
# IIOT Climate control Mansfield
# May-2023
# ----------------------------------------------------------------------------------------------------------------------
# Libraries
import datetime
import streamlit as st

from Plotly_Function import plot_html_handler1, plot_html_handler2, plot_html_temp_hr, plot_html_temp_hr2
from Sql_Function import get_data_day, get_data_range, to_excel
# ----------------------------------------------------------------------------------------------------------------------
# Settings page
st.set_page_config(page_title='IIOT - Mansfield',
                   initial_sidebar_state='collapsed',
                   page_icon='./assets/logo_corona.png',
                   layout='wide')
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Initial config
st.title('📈 IIOT|Corona: Climate control Mansfield')
st.markdown("""---""")
# st.divider()
st.header('1) Select the room to see')
select_room = st.radio('What room do you want to see?', ['CBC 1-8', 'CBC 10-12'], 0)
st.markdown("""---""")
# st.divider()
# ----------------------------------------------------------------------------------------------------------------------
# Configuration date
st.header('2) Select date')
date_actual = datetime.date.today()
col1, col2 = st.columns(2)
with col1:
    select_date = st.radio('What do you want to analyze?', ('By day', 'By range of days'), key='fecha')
    FLAG_DOWNLOAD = False
with col2:
    # options to day
    if select_date == 'By day':
        sel_day = st.date_input('What day do you want to analyze?', date_actual, key='day')

        if sel_day > datetime.date.today():
            st.error(
                f"Remember that the selected day can't be higher than the actual day {date_actual}")
            st.stop()

        st.info(f'You will analyze the day {str(sel_day)}')

    # Opciones por rangos de días
    if select_date == 'By range of days':
        sel_day_init = st.date_input('Select the starting day', date_actual - datetime.timedelta(days=1),
                                     key='day_ini')
        sel_day_end = st.date_input('Select the end day', date_actual, key='day_fin')

        if sel_day_end <= sel_day_init:
            st.error("Remember to select a start date that is previous to the end date!!!")
            st.stop()

        elif sel_day_end > date_actual:
            st.error("Remember that the end date can't exceed the current date.")
            st.stop()

        else:
            st.info(f"You will analyze a period of {str((sel_day_end - sel_day_init).days + 1)} days.")
# st.divider()
st.markdown("""---""")
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Visualization the information
st.header('3) Graph information')
graph = st.checkbox('Graph', key='graph')

if graph is True:
    with st.spinner('Downloading information'):
        # Search dataFrame by the day or range chosen
        if select_date == 'By day':
            df, health_list, health_data, title = get_data_day(sel_day, select_room, FLAG_DOWNLOAD)
            # Date name to use in downloading an Excel file
            AUX_ARCHIVO = sel_day

        elif select_date == 'By range of days':
            df, health_list, health_data, title = get_data_range(sel_day_init, sel_day_end, select_room,
                                                                 FLAG_DOWNLOAD)
            # Date name to use in downloading an Excel file
            AUX_ARCHIVO = "from_" + str(sel_day_init) + "_until_" + str(sel_day_end)

        c1, c2, c3 = st.columns(3)
        c1.success('Success')
        c2.metric(label='Global health data', value=f"{health_data:.2f}%")
        # -------------------------------------------------------------------------------------------------
        # Plot room CDI
        if select_room == 'CBC 1-8':
            st.header('Room CBC 1-8')
            # Button to refresh the data
            if st.button('Refresh graphic', key='refresh'):
                FLAG_DOWNLOAD = True
                get_data_day.clear()
                get_data_range.clear()
                st.experimental_rerun()

            # Draw graph
            with st.spinner('Drawing the graphic...'):
                fig = plot_html_handler1(df, title)
                st.plotly_chart(fig, use_container_width=True)
                fig = plot_html_temp_hr(df, title)
                st.plotly_chart(fig, use_container_width=True)
            with st.expander("Download file"):
                # Converting to Excel file
                excel = to_excel(df[['Z1_T', 'Z2_T', 'Z1_HR', 'Z2_HR', 'HA1_T_Iny', 'HA1_T_Rec', 'HA1_T_AHA',
                                     'HA1_T_OUT', 'HA1_T_Fac', 'HA1_2_OUT_HR', 'HA1_Dmp_Vout', 'HA1_Dmp_Vrec',
                                     'HA1_Dmp_Vfac']])
                # Button to export the data
                st.download_button(label='📥 Download data as a *.xlsx file ', data=excel,
                                   file_name=f'Data_room_CBC_1-8_{AUX_ARCHIVO}.xlsx')
# ----------------------------------------------------------------------------------------------------------------------
        # Plot room CDI
        elif select_room == 'CBC 10-12':
            st.header('Room CBC 10-12')
            # Button to refresh the data
            if st.button('Refresh graphic', key='refresh'):
                FLAG_DOWNLOAD = True
                get_data_day.clear()
                get_data_range.clear()
                st.experimental_rerun()

            # Draw graph
            with st.spinner('Drawing the graphic...'):
                fig = plot_html_handler2(df, title)
                st.plotly_chart(fig, use_container_width=True)
                fig = plot_html_temp_hr2(df, title)
                st.plotly_chart(fig, use_container_width=True)

            with st.expander("Download file"):
                # Converting to Excel file
                excel = to_excel(df[['Z3_T', 'Z3_HR', 'HA2_T_Iny', 'HA2_T_Rec', 'HA2_T_AHA', 'HA2_T_OUT',
                                     'HA1_T_Fac', 'HA1_2_OUT_HR', 'HA2_Dmp_Vout', 'HA2_Dmp_Vrec', 'HA2_Dmp_Vfac']])
                # Button to export the data
                st.download_button(label='📥 Download data as a *.xlsx file ', data=excel,
                                   file_name=f'Data_room_CBC_10-12_{AUX_ARCHIVO}.xlsx')
# ----------------------------------------------------------------------------------------------------------------------
