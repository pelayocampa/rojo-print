import random
from datetime import datetime

import folium
import kagglehub
import pandas as pd
import streamlit as st
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static

# Set page config
st.set_page_config(page_title="Rojo-Foot-Print", page_icon="🌍", layout="wide")

# Initialize session state variables if they don't exist
if "entries" not in st.session_state:
    st.session_state.entries = []
if "total_co2" not in st.session_state:
    st.session_state.total_co2 = 0


# Header
st.title("🌍 Rojo-Foot-Print Mockup")
st.markdown("Track and visualize your carbon footprint from travel")

# Create two columns for the main layout
operations_col, map_col = st.columns([1, 2])

# cars_dataset_path = kagglehub.dataset_download(
#     "midhundasl/co2-emission-of-cars-dataset"
# )
# dataset_dataframe = pd.read_csv(cars_dataset_path)
# Display the dataset in the sidebar

with operations_col:
    # Form for adding new entries
    with st.form(key="entry_form"):
        st.subheader("Add New Journey")
        origin = st.text_input("Origin", placeholder="e.g., Madrid")
        destination = st.text_input("Destination", placeholder="e.g., Barcelona")

        vehicle_type = st.selectbox(
            "Transport Type", ["Car", "Bus", "Train", "Plane", "Bicycle", "Walk"]
        )

        # Show additional options if Car is selected
        # if vehicle_type == "Car":
        #     brands = dataset_dataframe["Car"].unique().tolist()
        #     car_brand = st.selectbox(
        #         "Car Brand",
        #         brands,
        #     )
        #     if car_brand:
        #         car_type = dataset_dataframe[dataset_dataframe["Car"] == car_brand][
        #             "Model"
        #         ].values[0]

            # You could adjust emission rates based on car_type
            # This would be used later in your emission calculation

        # CO2 emission rates in g/km (simplified)
        emission_rates = {
            "Car": 120,
            "Bus": 70,
            "Train": 40,
            "Plane": 250,
            "Bicycle": 0,
            "Walk": 0,
        }

        submit_button = st.form_submit_button(label="Add Entry")

        if submit_button:
            # In a real app, you would calculate the distance between origin and destination
            # For now, we'll use a random distance
            # Check if we have valid origin and destination
            if not origin or not destination:
                st.error("Please provide both origin and destination.")
                st.stop()

            # Use geopy to calculate the distance

            try:
                geolocator = Nominatim(user_agent="rojo-foot-print")
                origin_location = geolocator.geocode(origin)
                destination_location = geolocator.geocode(destination)

                if origin_location and destination_location:
                    origin_coords = (
                        origin_location.latitude,
                        origin_location.longitude,
                    )
                    destination_coords = (
                        destination_location.latitude,
                        destination_location.longitude,
                    )
                    distance = round(
                        geodesic(origin_coords, destination_coords).kilometers
                    )

                    co2_emitted = (
                        distance * emission_rates[vehicle_type] / 1000
                    )  # convert to kg

                    entry = {
                        "origin": origin,
                        "destination": destination,
                        "vehicle": vehicle_type,
                        "distance_km": distance,
                        "co2_kg": co2_emitted,
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    }

                    st.session_state.entries.append(entry)
                    st.session_state.total_co2 += co2_emitted
                    st.success(f"Added journey from {origin} to {destination}")

                    st.balloons()  # Celebrate the addition
                else:
                    st.warning("Couldn't find one or both locations.")
            except Exception as e:
                st.warning(f"Error calculating distance: {e}.")

    # Display CO2 Indicator
    st.subheader("Carbon Footprint")
    total_co2_tons = st.session_state.total_co2 / 1000  # Convert kg to tons
    st.metric("Total CO2 Generated", f"{total_co2_tons:.2f} tons", delta=None)

    # Progress bar with custom animation
    st.subheader("Carbon Reduction Progress")
    progress_value = min(1.0, total_co2_tons / 10)  # Assuming 10 tons is the max

    st.progress(progress_value)

    # Display a GIF as indicator (you would need to replace this URL with your own GIF)
    if progress_value > 0:
        st.image(
            "https://media.giphy.com/media/3o7TKSjRrfIPjeUGic/giphy.gif", width=200
        )

with map_col:
    # Map display
    st.subheader("Journey Map")

    # Create map centered at a default location
    m = folium.Map(location=[40.416775, -3.703790], zoom_start=6)

    # Add markers for each entry
    if st.session_state.entries:
        # In a real app, you would geocode the addresses or use coordinates
        # For this example we'll use random coordinates in Spain
        for entry in st.session_state.entries:
            # Random coordinates in Spain's bounding box (simplified)
            lat = random.uniform(36.0, 43.8)
            lon = random.uniform(-9.4, 3.4)

            color = {
                "Car": "red",
                "Bus": "orange",
                "Train": "blue",
                "Plane": "purple",
                "Bicycle": "green",
                "Walk": "green",
            }.get(entry["vehicle"], "gray")

    # Display the map
    folium_static(m)

    # Layer control for the map would be added here in a more complex implementation
    st.info(
        "You can add journeys using the form on the left. The map will update with each new entry."
    )

# Display all entries in a table
st.subheader("All Journeys")
if st.session_state.entries:
    entries_df = pd.DataFrame(st.session_state.entries)
    st.dataframe(entries_df)
else:
    st.info("No journeys added yet. Use the form to add your first journey.")

# Add options to clear data
if st.button("Clear All Data"):
    st.session_state.entries = []
    st.session_state.total_co2 = 0
    st.success("All data has been cleared.")
