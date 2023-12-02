import fiona
import geopandas as gpd
import numpy as np
import pandas as pd
import plotly_express as px
import streamlit as st
from fiona.io import MemoryFile

# def validate_geopackage(filename):
#     try:
#         src = fiona.open(filename)
#         profile = src.profile
#         # print(src.driver)
#         # print(src.profile)
#         # print(type(src))
#         if profile["driver"] in ["GPKG"]:
#             src.close()
#             return True
#         else:
#             return False
#     except Exception as e:
#         print(f"Invalid File format. {e}")


def geopackage(filename):
    try:
        src = fiona.open(filename)
        profile = src.profile
        if profile["driver"] in ["GPKG"]:
            return src
        else:
            return False
    except Exception as e:
        print(f"Invalid File format. {e}")


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

if file_uploaded is None:
    st.info(
        """
        Please upload a Geopackge to start the analysis
        """,
        icon="ℹ️",
    )
    st.stop()

# if not validate_geopackage(file_uploaded):
#     st.error(
#         """
#         Not a valid GeoPackage, please upload a valid gpkg file
#         """,
#         icon="🚨",
#     )
#     st.stop()

src = geopackage(file_uploaded)
print(src.profile)
