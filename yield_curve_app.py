import streamlit as st
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go

# Define bond maturities
bonds = ["1M", "3M", "6M", "1Y", "2Y", "3Y", "5Y", "7Y", "10Y", "20Y", "30Y"]

def get_bond_yields():
    bondsy = []
    for bond in bonds:
        result = requests.get(f"https://www.cnbc.com/quotes/US{bond}")
        src = result.content
        soup = BeautifulSoup(src, 'lxml')
        data = soup.find_all(lambda tag: tag.name == 'span' and tag.get('class') == ['QuoteStrip-lastPrice'])
        for element in data:
            bondsy.append(float(element.text[0:4]))
    return bondsy

def plot_yield_curve(bondsy):
    status = "Yield Curve"
    if bondsy[8] < bondsy[4]:
        status = "Inverted Yield Curve"

    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=bonds, y=bondsy, mode='lines+markers', name='US Treasury Yields'))
    fig.update_layout(
        title=status,
        xaxis_title="Bond Maturity",
        yaxis_title="Interest Rate (%)",
        template="plotly_dark"
    )
    return fig, status

# Streamlit UI
st.title("Yield Curve Visualizer")
st.write("Click the button below to generate the latest yield curve.")

if st.button("Generate Yield Curve"):
    st.write("Fetching data...")
    try:
        bondsy = get_bond_yields()
        fig, status = plot_yield_curve(bondsy)
        st.write(f"**Status:** {status}")
        st.plotly_chart(fig)
    except Exception as e:
        st.error("Failed to fetch yield data. Please try again later.")
        st.error(f"Error: {e}")
