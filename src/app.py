import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import random
from datetime import datetime

# Set page config
st.set_page_config(page_title="Rojo-Foot-Print", page_icon="🌍", layout="wide")

# Initialize session state variables if they don't exist
if "entries" not in st.session_state:
    st.session_state.entries = []
if "total_co2" not in st.session_state:
    st.session_state.total_co2 = 0

# Header
st.title("🌍 Rojo-Foot-Print")
st.markdown("Track and visualize your carbon footprint from travel")

# Create two columns for the main layout
col1, col2 = st.columns([1, 2])

with col1:
    # Form for adding new entries
    with st.form(key="entry_form"):
        st.subheader("Add New Journey")
        origin = st.text_input("Origin", placeholder="e.g., Madrid")
        destination = st.text_input("Destination", placeholder="e.g., Barcelona")

        vehicle_type = st.selectbox(
            "Transport Type", ["Car", "Bus", "Train", "Plane", "Bicycle", "Walk"]
        )

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
            distance = random.randint(10, 500)
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

with col2:
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

            folium.Marker(
                [lat, lon],
                popup=f"{entry['origin']} to {entry['destination']}<br>"
                f"{entry['vehicle']} | {entry['distance_km']} km<br>"
                f"CO2: {entry['co2_kg']:.2f} kg",
                icon=folium.Icon(color=color),
            ).add_to(m)

    # Display the map
    folium_static(m)

    # Layer control for the map would be added here in a more complex implementation
    st.info(
        "In a full implementation, the map would include layer controls and actual routes."
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
