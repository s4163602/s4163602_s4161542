import component.navbar
import pyhtml

def get_page_html(form_data):
    print("About to return infection page...")
    economic_phase = form_data.get("economic-phase", [""])[0]
    disease = form_data.get("disease", [""])[0]
    year = form_data.get("year", [""])[0]
    
    page_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Infection Data</title>
        <!-- Match first page styles -->
        <link rel="stylesheet" href="/static/style.css">
        <link rel="stylesheet" href="/static/main.css">
        <!-- Keep your page-specific file if needed -->
        </head>

        <body class="page-body">
        {component.navbar.navbar}

        <div class="page-container">
          <!-- Filter Section -->
          <h2 class="table-heading">Infection Rates</h2>
          <form method="GET" class="filter-bar">
            <div class="left-group">
              <select id="economic_phase" name="economic-phase">
                <option value="">Economic Phase</option>
      """
    
    sql_query = "SELECT phase FROM Economy"
    results = pyhtml.get_results_from_query("database/immunisation.db", sql_query)
    for row in results:
        page_html += f"<option value=\"{row[0]}\">{row[0]}</option>"

    page_html += """
              </select>

              <select id="disease" name="disease">
                <option value="">Preventable Disease</option>
      """
    
    sql_query = "SELECT description FROM Infection_Type"
    results = pyhtml.get_results_from_query("database/immunisation.db", sql_query)
    for row in results:
        page_html += f"<option value=\"{row[0]}\">{row[0]}</option>"

    page_html += """
              </select>

              <select id="year" name="year">
                <option value="">Year</option>
      """
    
    sql_query = "SELECT * FROM Yeardate"
    results = pyhtml.get_results_from_query("database/immunisation.db", sql_query)
    for row in results:
        page_html += f"<option value=\"{row[0]}\">{row[0]}</option>"

    page_html += f"""
              </select>
            </div>

            <div class="right-group">
              <input type="submit" value="Show" class="btn">
            </div>
          </form>

          <!-- Infection Table -->
          <div class="table-container">
            <table id="infection-table-1" class="vaccination-table">
              <thead>
                <tr>
                  <th>Preventable Disease</th>
                  <th>Country</th>
                  <th>Economic Phase</th>
                  <th>Year</th>
                  <th>Cases per 100,000 people</th>
                </tr>
              </thead>
    """

    sql_query = f"""SELECT Infection_Type.description, Country.name, Economy.phase,YearDate.YearID,ROUND((InfectionData.cases/CountryPopulation.population)*100000,2) AS cases_per_100k
FROM Infection_Type JOIN InfectionData ON Infection_Type.id = InfectionData.inf_type
JOIN Country ON InfectionData.country = Country.CountryID
JOIN Economy ON Country.economy = Economy.economyID
JOIN CountryPopulation ON CountryPopulation.country = Country.CountryID AND CountryPopulation.year = InfectionData.year
JOIN YearDate ON YearDate.YearID = InfectionData.year
WHERE Economy.phase = '{economic_phase}' AND Infection_Type.description = '{disease}' AND YearDate.YearID = '{year}';"""
    
    results = pyhtml.get_results_from_query("database/immunisation.db", sql_query)
    page_html += """
              <tbody id="infection-data">
    """
    for row in results:
        page_html += f"""
                <tr>
                  <td>{row[0]}</td>
                  <td>{row[1]}</td>
                  <td>{row[2]}</td>
                  <td>{row[3]}</td>
                  <td>{row[4]}</td>
                </tr>
        """
    if not results:
        page_html += """
                <tr><td colspan="5" style="text-align:center;">No data matches filters.</td></tr>
        """
    page_html += """
              </tbody>
            </table>
          </div>

          <hr style="margin:2rem 0; border:none; border-top:1px solid #e5e7eb;">

          <!-- Data Summary Section -->
          <h2 class="table-heading">Data Summary</h2>
          <div class="table-container">
            <table id="infection-table-2" class="vaccination-table">
              <thead>
                <tr>
                  <th>Preventable Disease</th>
                  <th>Economic Phase</th>
                  <th>Year</th>
                  <th>Cases</th>
                </tr>
              </thead>
    """
    sql_query = f"""SELECT
Infection_Type.description,
Economy.phase,
YearDate.YearID,
SUM(InfectionData.cases)
FROM  Infection_Type JOIN InfectionData ON Infection_Type.id = InfectionData.inf_type
JOIN Country ON InfectionData.country = Country.CountryID
JOIN Economy ON Country.economy = Economy.economyID
JOIN YearDate ON YearDate.YearID = InfectionData.year
WHERE description = '{disease}' AND YearID = '{year}'
GROUP BY Infection_Type.description,Economy.phase,YearDate.YearID
ORDER BY Economy.economyID;"""
    results = pyhtml.get_results_from_query("database/immunisation.db", sql_query)
    page_html += """
              <tbody id="summary-data">
    """
    for row in results:
        page_html += f"""
                <tr>
                  <td>{row[0]}</td>
                  <td>{row[1]}</td>
                  <td>{row[2]}</td>
                  <td>{row[3]}</td>
                </tr>
        """
    if not results:
        page_html += """
                <tr><td colspan="4" style="text-align:center;">No data available for this selection.</td></tr>
        """
    page_html += f"""
              </tbody>
            </table>
          </div>
        </div> <!-- /.page-container -->
        </body>
        </html>
    """
    
    return page_html