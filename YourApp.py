import streamlit as st
from gmplot import gmplot

class YourApp:
    def display_google_maps(self, latitude, longitude, zoom=10):
        gmap = gmplot.GoogleMapPlotter(latitude, longitude, zoom)
        gmap.marker(latitude, longitude)

        map_filename = "google_map.html"
        gmap.draw(map_filename)

        with open(map_filename, "r", encoding="utf-8") as f:
            map_html = f.read()

        st.markdown(map_html, unsafe_allow_html=True)

    def run_web_app(self):
        # st.set_page_config(page_title="Your App", page_icon=":earth_americas:")

        # Your existing app code goes here...

        # Add Google Maps to your app
        location = (77.2190, 28.6278)  # Replace with actual coordinates
        self.display_google_maps(*location)

if __name__ == "__main__":
    your_app = YourApp()
    your_app.run_web_app()
