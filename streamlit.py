import base64
from io import BytesIO
from matplotlib.figure import Figure
import numpy as np
import streamlit as st
from diffusion import TwoDimensionalRDEquations
import tempfile

# Constants
WIDTH, HEIGHT, DX, DT = 200, 200, 1, 0.001

# Initialize session state
st.session_state.setdefault("display_output", False)

# Title
st.title("🌀 Nature is Data 🌀 Generate your own patterns")


# Function to create sidebar sliders
def create_slider(label, min_value, max_value, value, key):
    return st.sidebar.slider(
        label, min_value=min_value, max_value=max_value, value=value, key=key
    )


# Sidebar Widgets
da = create_slider("Diffusion coefficient for A", 0.0, 10.0, 1.0, "da")
db = create_slider("Diffusion coefficient for B", 0.0, 200.0, 100.0, "db")
alpha = create_slider("Alpha parameter", -1.0, 1.0, -0.005, "alpha")
beta = create_slider("Beta parameter", 0.0, 20.0, 10.0, "beta")
steps = st.sidebar.number_input("Number of steps", 1, 1000, 150)
output = st.sidebar.text_input("Output file name", value="image")
spatial = st.sidebar.checkbox("spatial")
gif = st.sidebar.checkbox("gif")


# Function to generate spatial dynamics
def generate_spatial():
    x, y = np.mgrid[0:WIDTH, 0:WIDTH]
    return 0.1 + 5 * (1 + np.sin(2 * np.pi * y / 50)) * (1 + np.sin(2 * np.pi * x / 50))


@st.cache_data(hash_funcs={Figure: hash}, ttl=3600)
def _generate_plot(da, db, alpha, beta, steps, spatial):
    beta_val = generate_spatial() if spatial else beta

    def Ra(a, b):
        return a - a**3 - b + alpha

    def Rb(a, b):
        return (a - b) * beta_val

    eq = TwoDimensionalRDEquations(
        da, db, Ra, Rb, width=WIDTH, height=HEIGHT, dx=DX, dt=DT, steps=100
    )

    return eq.plot_evolution_outcome_fig(n_steps=steps)


@st.cache_data(ttl=3600)
def _generate_gif(da, db, alpha, beta, steps, spatial):
    beta_val = generate_spatial() if spatial else beta

    def Ra(a, b):
        return a - a**3 - b + alpha

    def Rb(a, b):
        return (a - b) * beta_val

    eq = TwoDimensionalRDEquations(
        da, db, Ra, Rb, width=WIDTH, height=HEIGHT, dx=DX, dt=DT, steps=100
    )

    ani = eq.plot_time_evolution_fig(n_steps=steps)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".gif") as tmpfile:
        ani.save(tmpfile.name, dpi=60, fps=10, writer="pillow")
        return tmpfile.name


# Buttons in the same row
if st.button("Generate Pattern"):
    st.session_state["display_output"] = True
if st.button("Clear Output"):
    st.session_state["display_output"] = False

# Check if display_output is True
if st.session_state["display_output"]:
    st.subheader("Generated Turing Pattern Plot")
    plot_fig = _generate_plot(da, db, alpha, beta, steps, spatial)
    st.pyplot(plot_fig)
    # Save the plot to a BytesIO object
    buf = BytesIO()
    plot_fig.savefig(buf, format="png")
    buf.seek(0)

    # Create a button for downloading the plot
    st.download_button(
        label="Download Plot",
        data=buf,
        file_name=f"{output}_{da}_{db}_{alpha}_{beta}_{steps}_{'spatial' if spatial else ''}.png",
        mime="image/png",
    )
    if gif:
        st.subheader("Generated Turing Pattern GIF")
        gif_file_name = _generate_gif(da, db, alpha, beta, steps, spatial)
        # Read the contents of the saved temporary file
        with open(gif_file_name, "rb") as file:
            # Convert the file contents to a base64-encoded string
            data = base64.b64encode(file.read()).decode()

            # Embed the base64-encoded GIF using an HTML img tag
            st.markdown(
                f'<img src="data:image/gif;base64,{data}" alt="animation gif">',
                unsafe_allow_html=True,
            )

            # Read the saved file into a BytesIO object
        with open(gif_file_name, "rb") as file:
            buf_2 = BytesIO()
            buf_2.write(file.read())
            buf_2.seek(0)

            # Create a button for downloading the animation
            st.download_button(
                label="Download Animation",
                data=buf_2,
                file_name=f"{output}_{da}_{db}_{alpha}_{beta}_{steps}_{'spatial' if spatial else ''}.gif",
                mime="image/gif",
            )
else:
    st.write("Hello there! Start tweaking the values of each parameter to generate a pattern that is unique to you! Tick ”spatial” if you’d like to generate a symmetrical pattern Tick “gif” if you’d like to generate an animation for your unique pattern development Have fun :) Key features: Reaction-diffusion simulation Image generation Interactive parameters Batch image generation This website aims to reflect on the natural world and the mathematical laws that govern it. My design practice aims to create narratives that threads together the beauty of numerical patterns with the tactile richness of textiles. @lydiak0k")
