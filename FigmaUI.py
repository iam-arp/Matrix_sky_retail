import streamlit as st
import streamlit.components.v1 as components

class FigmaUI:
    def __init__(self):
        pass

    def display_figma_ui(self):
        st.title("Figma Prototype Viewer")

        figma_link = "https://www.figma.com/file/lMYyNOptCmZb5JlYXmKkif/CourseEvaluation?type=design&node-id=160-1249&mode=design"

        components.iframe(figma_link, width=800, height=500, scrolling=True)

    def run_web_app(self):
        self.display_figma_ui()
