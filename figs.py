import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

def plot1(df, ticker_name):
    # Create the Candlestick trace
    Candlestick = go.Candlestick(x=df['Date'],
                                 open=df['Open'],
                                 high=df['High'],
                                 low=df['Low'],
                                 close=df['Close'],
                                 name='Candlestick')

    # Create the figure with both traces
    fig = go.Figure(data=[Candlestick])

    # Update the layout properties
    fig.update_layout(
        title=f'Price: {ticker_name}',
        xaxis_title='Date',
        xaxis=dict(
            type='date',
            tickfont=dict(size=10),
            nticks=10),
        yaxis=dict(
            title='Price',
            tickfont=dict(size=10)
        ),
        title_x=0.5,
        showlegend=False
    )
    return fig

def plot2(df, ticker_name):
    # Create the volume trace (bar chart)
    volume = go.Bar(x=df['Date'],
                    y=df['Volume'],
                    yaxis='y2',  # Use the secondary y-axis for volume
                    name='Volume',
                    marker=dict(color='rgba(0, 0, 255, 1)'))  # Set the color and opacity

    # Create the figure with both traces
    fig = go.Figure(data=[volume])

    # Update the layout properties
    fig.update_layout(
        title=f'Volume: {ticker_name}',
        xaxis_title='Date',
        xaxis=dict(
            type='date',
            tickfont=dict(size=10),
            nticks=10),
        yaxis=dict(
            title='Volume',
            tickfont=dict(size=10)
        ),
        title_x=0.5,

        showlegend=False
    )
    return fig

def plot3(df, commodities, start_date, end_date):
# Create the correlation matrix
    close_prices = pd.DataFrame()
    for name, ticker in commodities.items():
        data = df[ticker]
        close_prices[name] = data['Close']

    correlation_matrix = close_prices.corr()
    heatmap = go.Heatmap(z=correlation_matrix,
                         x=correlation_matrix.columns,
                         y=correlation_matrix.index,
                         colorscale='Plasma',  # Choose a colorscale
                         zmin=-1, zmax=1)  # Set the color range to [-1, 1]

    fig = go.Figure(data=heatmap)

    # Update the layout properties
    fig.update_layout(
        title=f'Correlation Heatmap of Commodities using data from <br>{start_date} to {end_date}',
        xaxis_title='Commodity',
        yaxis_title='Commodity',
        title_x=0.5,
        xaxis=dict(tickfont=dict(size=10)),
        yaxis=dict(tickfont=dict(size=10)),
        showlegend=False
    )

    return fig