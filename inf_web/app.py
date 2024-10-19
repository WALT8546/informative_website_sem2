from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route("/")
def mainpage():
    return render_template("main.html")

@app.route("/about")
def aboutpage():
    return render_template("about.html")

# this part focuses on connecting the data with the dropdown select button to have the same options to choose as in the data set
# it uses pandas to further clean the data variables and to sort the list of available countries
# it also uses GET and POST methods that were taken from the FLASK Documentation and examples used in class 
@app.route("/choose", methods=['GET', 'POST'])
def country_selector():
    if request.method == 'POST':
        country_id = request.form['country']
        return redirect(url_for('country_detail', country_id=country_id))
    
    country_df = pd.read_csv('static/csv/country_table_export.csv')
    country_df.columns = country_df.columns.str.strip()
    countries = country_df[['Country_ID', 'Country_Name']].sort_values(by='Country_Name').to_dict(orient='records')
        
    return render_template("choose.html", countries=countries)
    

# this part focuses on the page where the data will be shown
# it uses elements from the os and matplotlib packages to avoid doing a graph manually for every country which documentation and further -
#understanding/documentation was retrieved from OS: https://docs.python.org/3/library/os.html and PLT: https://matplotlib.org/stable/users/explain/figure/backends.html, 
@app.route("/country/<int:country_id>")
def country_detail(country_id):
    country_df = pd.read_csv('static/csv/country_table_export.csv')
    ratings_df = pd.read_csv('static/csv/ratings_table_export.csv')
    country_df.columns = country_df.columns.str.strip()
    ratings_df.columns = ratings_df.columns.str.strip()
        
    country_name = country_df[country_df['Country_ID'] == country_id]['Country_Name'].values[0]
    country_data = ratings_df[ratings_df['Country_ID'] == country_id].sort_values(by='Year')
        
    plt.figure()
    plt.plot(country_data['Year'], country_data['Total_Score'], marker='o')
    plt.title(f'Freedom Rankings for {country_name}')
    plt.xlabel('Years')
    plt.ylabel('Freedom Score')
    plt.grid(True)
        
    # because of the os package, the graph is sent to the static folder into the graphs folder
    # it then saves the graph image and ends
    graph_path = f'static/graphs/{country_id}.png'
    plt.savefig(graph_path)
    plt.close()
        
    return render_template("country_detail.html", country_name=country_name, graph_url=url_for('static', filename=f'graphs/{country_id}.png'))

if __name__ == "__main__":
    app.run(debug=True)