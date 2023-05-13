# ---- HIDE Manage App ----
def load_css(file_name: str):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Call the function to load the CSS file
load_css("static/style.css")


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)  

def load_image(logo_path, width, height):
    """Read, resize, and return logo as a data URL"""
    if not os.path.isfile(logo_path):
        st.error(f"File {logo_path} not found")
        return None
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))

    # Convert the image to a data URL
    byte_arr = io.BytesIO()
    modified_logo.save(byte_arr, format='JPEG')
    encoded_image = base64.b64encode(byte_arr.getvalue()).decode()

    return f'data:image/jpeg;base64,{encoded_image}'

# Call the function to add the logo
my_logo = load_image(logo_path="qvision.jpg", width=160, height=90)

# Apply the custom CSS
if my_logo:
    custom_css = f'''
    <style>
    /* Hide the default Streamlit footer */
    .footer {{
        visibility: hidden;
    }}
    /* Add your logo to the page */
    header::after {{
        content: url("{my_logo}");
        display: block;
        position: absolute;
        right: 0px;  # move it closer to the right edge
        bottom: 0px;  # move it closer to the bottom edge
        width: 160px;
        height: 90px;
        z-index: 100;
    }}
    </style>
    '''
    st.markdown(custom_css, unsafe_allow_html=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)  