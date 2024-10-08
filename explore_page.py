import streamlit
import pandas as pd
import matplotlib.pyplot as plt
import os

def shorten_categories(categories, cutoff):
    return {cat: cat if count >= cutoff else 'Other' for cat, count in categories.items()}

def clean_experience(x):
    if x == "More than 50 years":
        return 50
    if x == "Less than 1 year":
        return 0.5
    return float(x)

def clean_education(x):
    if "Bachelor's degree" in x:
        return "Bachelor's degree"
    if "Master's degree" in x:
        return "Master's degree"
    if "Professional degree" in x:
        return "Professional degree"
    return "Less than a Bachelors"

def load_data():
    try:
        file_path = os.path.join('dataset', 'survey_results_public.csv')
        df = pd.read_csv(file_path)
        df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
        df = df[df["ConvertedComp"].notnull()]
        df = df.dropna()
        df = df[df["Employment"] == "Employed full-time"]
        df = df.drop("Employment", axis=1)

        country_map = shorten_categories(df.Country.value_counts(), 400)
        df["Country"] = df["Country"].map(country_map)
        df = df[df["ConvertedComp"] <= 250000]
        df = df[df["ConvertedComp"] >= 10000]
        df = df[df["Country"] != "Other"]

        df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
        df["EdLevel"] = df["EdLevel"].apply(clean_education)
        df = df.rename(columns={"ConvertedComp": "Salary"})
        return df
    except FileNotFoundError:
        streamlit.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        streamlit.error(f"An error occurred: {e}")
        return None

df = load_data()

def show_explore_page():
    if df is None:
        return

    streamlit.title("Explore Software Engineer Salaries")
    
    streamlit.write(
        """
        ### Stack Overflow Developer Survey 2020
        """
    )
    
    data = df["Country"].value_counts()
    
    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    streamlit.write("#### Number of Data from different countries")
    streamlit.pyplot(fig1)
    
    streamlit.write("#### Mean Salary Based On Country")
    data = df.groupby("Country")["Salary"].mean().sort_values(ascending=True)
    streamlit.bar_chart(data)
    
    streamlit.write("#### Mean Salary Based On Experience")
    data = df.groupby("YearsCodePro")["Salary"].mean().sort_values(ascending=True)
    streamlit.line_chart(data)
