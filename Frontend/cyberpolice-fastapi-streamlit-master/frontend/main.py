import requests
import streamlit as st

st.title('CyberPolice')
st.subheader("Sexual Harassment Detection System")

input_text = st.text_input('Text Input')

if st.button("Check"):
    if input_text is not None and len(input_text) > 0:
        res = requests.post(f"http://backend:8000/predict",
                            json={'input_text': input_text})
        result = res.json()
        print(res, result, type(res), type(result))
        # st.write(res, result, type(res), type(result))
        pred = result["confidence"]
        if pred>0.5:
            st.warning(result['CyberPolice'])
        else:
            st.success(result['CyberPolice'])
    else:
        st.error("Please provide text input for CyberPolice to check!")
