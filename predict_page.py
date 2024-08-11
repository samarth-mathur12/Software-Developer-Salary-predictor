import streamlit
import pickle
import numpy


def load_model():
    with open("saved_steps.pkl", "rb") as file:
        data = pickle.load(file)
    return data 

data = load_model()


regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]


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
    
    
    country = streamlit.selectbox("Country: ", countries)
    education = streamlit.selectbox("Education: ", education)
    
    expericence = streamlit.slider("Year od Experince", 0, 50, 3)
    
    ok = streamlit.button("Calaucate Salary")
    
    if ok:
        X = numpy.array([[country, education, expericence]])
        X[:, 0] = le_country.transform(X[:,0])
        X[:, 1] = le_education.transform(X[:,1])
        X = X.astype(float)
        
        salary = regressor.predict(X)
        streamlit.subheader(f"The estimated salary is ${salary[0]:.2f}") 