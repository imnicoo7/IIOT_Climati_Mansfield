# App de Mansfield with Python Streamlit
# IIOT Climate control Mansfield
# May-2023
# ----------------------------------------------------------------------------------------------------------------------
# Libraries
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ----------------------------------------------------------------------------------------------------------------------
# Function definition
def plot_on_off(fig, df, column, legend, rgb, visibility="legendonly", second_y=True,  axis_y="y2", r=1, c=1):

    fig.add_trace(go.Scatter(x=df.index, y=df[column],
                             fill='tozeroy', mode="lines",
                             fillcolor=rgb,
                             line_color='rgba(0,0,0,0)',
                             legendgroup=legend,
                             showlegend=True,
                             name=legend,
                             yaxis=axis_y,
                             visible=visibility)
                  , secondary_y=second_y, row=r, col=c)

    return fig


@st.cache_data(persist=False, experimental_allow_widgets=True, show_spinner=True, ttl=24 * 3600)
# @st.cache(persist=False, allow_output_mutation=True, suppress_st_warning=True, show_spinner=True, ttl=24 * 3600)
def plot_html_temp_hr(df, title):
    """
    Función para dibujar la temperatura y humedad de las zonas 1 y 2 salon CBC 1-8
    df = pandas dataframe traído de la base de dato SQL
    title = Título de la gráfica
    OUTPUT:
    fig = objeto figura para dibujarlo externamente de la función
    """
    # ----------------------------------------------------------------------------------------------
    fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]], vertical_spacing=0.02)

    # ZONE 1: TEMPERATURE  SENSOR  1 ROOM CBC
    fig.add_trace(go.Scatter(x=df.index, y=df["Z1_T"],
                             line=dict(color='#3366cc', width=1.5),
                             mode='lines', name='Temp sensor 1', yaxis="y1"),
                  row=1, col=1)
    # ZONE 2: TEMPERATURE  SENSOR  2 ROOM CBC
    fig.add_trace(go.Scatter(x=df.index, y=df["Z2_T"],
                             line=dict(color='#B40018', width=1.5),
                             mode='lines', name='Temp sensor 2', yaxis="y1"),
                  row=1, col=1)
    # ZONE 1: HUMIDITY SENSOR 1 ROOM CBC
    fig.add_trace(go.Scatter(x=df.index, y=df["Z1_HR"],
                             line=dict(color='#3366cc', width=1, dash='dash'),
                             mode='lines', name='HR sensor 1', yaxis="y2"),
                  secondary_y=True, row=1, col=1)
    # ZONE 2: HUMIDITY SENSOR 2 ROOM CBC
    fig.add_trace(go.Scatter(x=df.index, y=df["Z2_HR"],
                             line=dict(color='#B40018', width=1, dash='dash'),
                             mode='lines', name='HR sensor 2', yaxis="y2"),
                  secondary_y=True, row=1, col=1)
    # ----------------------------------------------------------------------------------------------
    # Settings axes and chart layout
    fig.update_layout(height=500, title=title, showlegend=True)
    fig.layout.template = 'seaborn'  # ggplot2, plotly_dark, seaborn, plotly, plotly_white
    fig.update_layout(modebar_add=["v1hovermode", "toggleSpikeLines"])
    fig.update_layout(legend_title_text='Variables room CBC')

    fig.update_yaxes(showline=True, linewidth=1, linecolor='black')
    fig.update_xaxes(title_text='Date', showline=True, linewidth=1, linecolor='black', row=1, col=1)

    fig.update_layout(yaxis=dict(title='Temperature [°F]', range=[50, 100]),
                      yaxis2=dict(title='Relative Humidity [%]'))  # range=[20, 40]))
    return fig


@st.cache_data(persist=False, experimental_allow_widgets=True, show_spinner=True, ttl=24 * 3600)
# @st.cache(persist=False, allow_output_mutation=True, suppress_st_warning=True, show_spinner=True, ttl=24 * 3600)
def plot_html_handler1(df, title):
    """
    Función para dibujar las variables para el handler 1: BMC 1-8
    df = pandas dataframe traído de la base de dato SQL
    title = Título de la gráfica
    OUTPUT:
    fig = objeto figura para dibujarlo externamente de la función
    """
    # ----------------------------------------------------------------------------------------------

    fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]], vertical_spacing=0.02)

    # Dampers outside, recirculation, factory
    fig = plot_on_off(fig, df, "HA1_Dmp_Vout", "Out Damp", 'rgba(255,127,0,0.3)', axis_y="y2", r=1, c=1)
    fig = plot_on_off(fig, df, "HA1_Dmp_Vrec", "Rec Damp", 'rgba(77,175,74,0.3)', axis_y="y2", r=1, c=1)
    fig = plot_on_off(fig, df, "HA1_Dmp_Vfac", "Fac Damp", 'rgba(55,126,184,0.3)', axis_y="y2", r=1, c=1)

    # 1er graph
    # HANDLER 1:INJECTION AIR TEMPERATURE ROOM CBC
    fig.add_trace(go.Scatter(x=df.index, y=df["HA1_T_Iny"],
                             line=dict(color='#ff9900', width=1), mode='lines',
                             name='Iny Air BMC', yaxis="y1"),
                  row=1, col=1)
    # HANDLER 1:RECIRCULATION AIR TEMPERATURE
    fig.add_trace(go.Scatter(x=df.index, y=df["HA1_T_Rec"],
                             line=dict(color='#0B961F', width=1),
                             mode='lines', name='Rec Temp', yaxis="y1"),
                  row=1, col=1)
    # HANDLER 1: AIR TEMPERATURE INJECT TO HANDLER
    fig.add_trace(go.Scatter(x=df.index, y=df["HA1_T_AHA"],
                             line=dict(color='gray', width=1),
                             mode='lines', name='Air Inject to handler', yaxis="y1"),
                  row=1, col=1)
    # HANDLER 1: OUT AIR TEMPERATURE
    fig.add_trace(go.Scatter(x=df.index, y=df["HA1_T_OUT"],
                             line=dict(color='black', width=1),
                             mode='lines', name='Out Air Temp', yaxis="y1"),
                  row=1, col=1)
    # HANDLER 1: OUT AIR TEMPERATURE
    fig.add_trace(go.Scatter(x=df.index, y=df["HA1_T_Fac"],
                             line=dict(color='#152DA3', width=1),
                             mode='lines', name='Plant Air Temp', yaxis="y1"),
                  row=1, col=1)
    # HANDLER 1 Y 2:OUTSIDE HUMIDITY
    fig.add_trace(go.Scatter(x=df.index, y=df["HA1_2_OUT_HR"],
                             line=dict(color='red', width=1, dash='dash'),
                             mode='lines', name='Outside HR', yaxis="y2"),
                  secondary_y=True, row=1, col=1)
    # ----------------------------------------------------------------------------------------------
    # Settings axes and chart layout
    fig.update_layout(height=500, title=title, showlegend=True)
    fig.layout.template = 'seaborn'  # ggplot2, plotly_dark, seaborn, plotly, plotly_white
    fig.update_layout(modebar_add=["v1hovermode", "toggleSpikeLines"])
    fig.update_layout(legend_title_text='Variables room CBC 1-8')
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black')

    fig.update_xaxes(title_text='Date', showline=True, linewidth=1, linecolor='black', row=1, col=1)

    fig.update_layout(yaxis=dict(title='Handler 1: Air Temperature [°F]'),
                      yaxis2=dict(title='Outside HR and Dampers [%]', range=[0, 100]))

    return fig


@st.cache_data(persist=False, experimental_allow_widgets=True, show_spinner=True, ttl=24 * 3600)
# @st.cache(persist=False, allow_output_mutation=True, suppress_st_warning=True, show_spinner=True, ttl=24 * 3600)
def plot_html_handler2(df, title):
    """
    Función para dibujar las variables para el handler 2: BMC 10-12
        df = pandas dataframe traído de la base de dato SQL
        title = Título de la gráfica
    OUTPUT:
        fig = objeto figura para dibujarlo externamente de la función
    """
    # ----------------------------------------------------------------------------------------------
    fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]], vertical_spacing=0.02)
    # Dampers outside, recirculation, factory
    fig = plot_on_off(fig, df, "HA2_Dmp_Vout", "Out Damp", 'rgba(255,127,0,0.3)', axis_y="y2", r=1, c=1)
    fig = plot_on_off(fig, df, "HA2_Dmp_Vrec", "Rec Damp", 'rgba(77,175,74,0.3)', axis_y="y2", r=1, c=1)
    fig = plot_on_off(fig, df, "HA2_Dmp_Vfac", "Fac Damp", 'rgba(55,126,184,0.3)', axis_y="y2", r=1, c=1)

    # 1 graph
    # HANDLER 2:INJECTION AIR TEMPERATURE ROOM CBC
    fig.add_trace(go.Scatter(x=df.index, y=df["HA2_T_Iny"],
                             line=dict(color='#ff9900', width=1), mode='lines',
                             name='Iny Air BMC', yaxis="y1"),
                  row=1, col=1)
    # HANDLER 2: RECIRCULATION AIR TEMPERATURE
    fig.add_trace(go.Scatter(x=df.index, y=df["HA2_T_Rec"],
                             line=dict(color='#0B961F', width=1),
                             mode='lines', name='Rec Temp', yaxis="y1"),
                  row=1, col=1)
    # HANDLER 2: AIR TEMPERATURE INJECT TO HANDLER
    fig.add_trace(go.Scatter(x=df.index, y=df["HA2_T_AHA"],
                             line=dict(color='gray', width=1),
                             mode='lines', name='Air Iny Handler', yaxis="y1"),
                  row=1, col=1)
    # HANDLER 2: OUT AIR TEMPERATURE
    fig.add_trace(go.Scatter(x=df.index, y=df["HA2_T_OUT"],
                             line=dict(color='black', width=1),
                             mode='lines', name='Out Air Temp', yaxis="y1"),
                  row=1, col=1)
    # HANDLER 2: OUT AIR TEMPERATURE
    fig.add_trace(go.Scatter(x=df.index, y=df["HA2_T_Fac"],
                             line=dict(color='#152DA3', width=1),
                             mode='lines', name='Plant Air Temp', yaxis="y1"),
                  row=1, col=1)
    # HANDLER 1 Y 2:OUTSIDE HUMIDITY
    fig.add_trace(go.Scatter(x=df.index, y=df["HA1_2_OUT_HR"],
                             line=dict(color='red', width=1, dash='dash'),
                             mode='lines', name='Outside HR', yaxis="y2"),
                  secondary_y=True, row=1, col=1)
    # ----------------------------------------------------------------------------------------------
    # Settings axes and chart layout
    fig.update_layout(height=500, title=title, showlegend=True)
    fig.layout.template = 'seaborn'  # ggplot2, plotly_dark, seaborn, plotly, plotly_white
    fig.update_layout(modebar_add=["v1hovermode", "toggleSpikeLines"])
    fig.update_layout(legend_title_text='Variables room CBC 10-12')

    fig.update_yaxes(showline=True, linewidth=1, linecolor='black')
    fig.update_xaxes(title_text='Date', showline=True, linewidth=1, linecolor='black', row=1, col=1)

    fig.update_layout(yaxis=dict(title='Handler 2: Air Temperature [°F]'),
                      yaxis2=dict(title='Outside HR and Dampers [%]', range=[0, 100]))

    return fig


@st.cache_data(persist=False, experimental_allow_widgets=True, show_spinner=True, ttl=24 * 3600)
# @st.cache(persist=False, allow_output_mutation=True, suppress_st_warning=True, show_spinner=True, ttl=24 * 3600)
def plot_html_temp_hr2(df, title):
    """
    Función para dibujar la temperatura y humedad de las 3 zona salon CBC 10-12
    df = pandas dataframe traído de la base de dato SQL
    title = Título de la gráfica
    OUTPUT:
    fig = objeto figura para dibujarlo externamente de la función
    """
    # ----------------------------------------------------------------------------------------------
    fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]], vertical_spacing=0.02)

    # Temperature sensor 3
    fig.add_trace(go.Scatter(x=df.index, y=df["Z3_T"],
                             line=dict(color='#3366cc', width=1.5),
                             mode='lines',  # 'lines+markers'
                             name='Temp sensor 3', yaxis="y1"),
                  row=1, col=1)
    # Humidity sensor 3
    fig.add_trace(go.Scatter(x=df.index, y=df["Z3_HR"],
                             line=dict(color='#ff9900', width=1, dash='dash'),
                             mode='lines',  # 'lines+markers'
                             name='HR sensor 3', yaxis="y2"),
                  secondary_y=True, row=1, col=1)
    # -----------------------------------------------------------------------------------------------
    # Settings axes and chart layout
    fig.update_layout(height=500, title=title, showlegend=True)
    fig.layout.template = 'seaborn'  # ggplot2, plotly_dark, seaborn, plotly, plotly_white
    fig.update_layout(modebar_add=["v1hovermode", "toggleSpikeLines"])
    fig.update_layout(legend_title_text='Variables room CBC')
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black')

    fig.update_xaxes(title_text='Date', showline=True, linewidth=1, linecolor='black', row=1, col=1)

    fig.update_layout(yaxis=dict(title='Temperature [°F]', range=[50, 100]),
                      yaxis2=dict(title='Relative Humidity [%]'))

    return fig
