import copy

import fiona
import geopandas as gpd
import numpy as np
import pandas as pd
import plotly_express as px
import streamlit as st


def validate_geopackage(filename) -> bool | None:
    try:
        with fiona.open(filename) as src:
            profile = src.profile
            if profile["driver"] in ["GPKG"]:
                return True
            else:
                return False
    except Exception as e:
        print(f"Invalid File format. {e}")


@st.cache_data
def get_geodataframe(filename, layer) -> gpd.GeoDataFrame:
    return gpd.read_file(filename, layer=layer)


st.title("Spatial Autocorrelation Data App")

st.markdown(
    """
    This is a data app thats help you in perform an exploratory analysis of spatial data
    like Spatial Autocorrelation in deep analysis.
    """
)


with st.sidebar:
    file_uploaded = st.file_uploader(
        "Choose a GeoPackage", type="gpkg", help="Only use geopackage file"
    )
# Copy file for future use if valid
file_uploaded_for_layers = copy.deepcopy(file_uploaded)
file_uploaded_for_gdf = copy.deepcopy(file_uploaded)


if file_uploaded is None:
    st.info(
        """
        Please upload a Geopackge to start the analysis
        """,
        icon="ℹ️",
    )
    st.stop()

if not validate_geopackage(file_uploaded):
    st.error(
        """
        Not a valid GeoPackage, please upload a valid gpkg file
        """,
        icon="🚨",
    )
    file_uploaded.close()
    st.stop()

# Close original file
file_uploaded.close()
# file_uploaded.closed

# List layers inside gpkg
list_layers = fiona.listlayers(file_uploaded_for_layers)
list_layers.sort()

with st.sidebar:
    with st.form("layer_selection"):
        selected_layer = st.selectbox(
            label="Select layer", options=list_layers, index=None
        )
        submit = st.form_submit_button("Confirm layer selection")


if not submit:
    st.info(
        """
        Please confirm the layer selection of the Geopackge
        """,
        icon="ℹ️",
    )
    st.stop()


# If valid read the file to a geodataframe
gdf: gpd.GeoDataFrame = get_geodataframe(file_uploaded_for_gdf, layer=selected_layer)
wkt_gdf: pd.DataFrame = gdf.to_wkt()
st.dataframe(wkt_gdf)


# Close gdf file copy
file_uploaded_for_layers.close()  # type: ignore
file_uploaded_for_gdf.close()  # type: ignore
