import streamlit
import numpy
import pickle

def show_predict_page():
    streamlit.title("Software Developer Salary Prediction")
    streamlit.write(""" ### We need some information to predict the salary""")
    
    countries = (
        "United States",
        "India",
        "United Kingdom",
        "Germany",
        "Canada",
        "Brazil",
        "France",
        "Spain",
        "Australia",
        "Netherlands",
        "Poland",
        "Italy",
        "Russian Federation",
        "Sweden",
    )

    education = (
        "Less than a Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad",
    )
    
    country = streamlit.selectbox("Country: ", countries, key='country_selectbox')
    education = streamlit.selectbox("Education: ", education, key='education_selectbox')
    
    experience = streamlit.slider("Years of Experience", 0, 50, 3, key='experience_slider')
    
    ok = streamlit.button("Calculate Salary", key='calculate_button')
    
    if ok:
        X = numpy.array([[country, education, experience]])
        X[:, 0] = le_country.transform(X[:,0])
        X[:, 1] = le_education.transform(X[:,1])
        X = X.astype(float)
        
        salary = regressor.predict(X)
        streamlit.subheader(f"The estimated salary is ${salary[0]:.2f}")
