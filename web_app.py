import streamlit as st
import helper
from PIL import Image

def load_image(image_file):
    img = Image.open(image_file)
    format = img.format
    img.save(f"input.{format.lower()}")
    return img,f"input.{format.lower()}",format

st.title("Image Based Search Engine")
st.text('A web-app to get relevant links based on input Image')
img = st.file_uploader("Upload the Image here")
image = st.button(label="Search")

if image:
    driver = helper.get_driver()
    img,input_img_path,format = load_image(img)
    st.text('Original Image')
    st.image(img)
    status,img_path = helper.face_detection(input_img_path,format)
    if status:
        st.text('Cropped Image using Face Detection')
        st.image(img_path)
    glink = helper.google_search_link(input_img_path)
    links = helper.links_scrape(driver,glink)
    st.text('Links Related to the Image')
    for idx,i in enumerate(links): 
        # print(i)
        st.markdown(f"[{i}]({i})")