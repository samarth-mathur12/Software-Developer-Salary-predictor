import streamlit
import pandas
import matplotlib.pyplot as plt


def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_experience(x):
    if x == "More than 50 years":
        return 50
    if x == "Less than 1 year":
        return 0.5
    
    return float(x)

def clean_education(x):
    if "Bachelor’s degree" in x:
        return "Bachelor’s degree"
    
    if "Master’s degree" in x:
        return "Master’s degree"
    
    if "Professional degree" in x:
        return "Professional degree"
    
    return "Less than a Bachelors"


def load_data():
    df = pandas.read_csv('D:\ML-Projects\Salary Prediction of Software developers\dataset\survey_results_public.csv')
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
    df = df.rename({"ConvertedComp": "Salary"}, axis=1)
    return df

df = load_data()

def show_explore_page():
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

    streamlit.write("""#### Number of Data from different countries""")

    streamlit.pyplot(fig1)
    
    streamlit.write(
        """
    #### Mean Salary Based On Country
    """
    )

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    streamlit.bar_chart(data)
    
    streamlit.write(
        """
    #### Mean Salary Based On Experience
    """
    )
    
    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    streamlit.line_chart(data)