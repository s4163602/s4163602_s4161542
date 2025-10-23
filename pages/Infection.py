import component.navbar
import component.footer
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
        <title> Mission Statement Dashboard</title>
        <link rel="stylesheet" href="static/main.css">
        <link rel="stylesheet" href="static/infection.css">
        </head>

        <body>
        <!-- Navbar -->
        {component.navbar.navbar}
        <main>
       <h1 class="main-heading">Infection</h1>

  <!-- Filter Section -->
  <form  method="GET">
  <div class="filter-section">
    <label for="economic_phase">Economic Phase:</label>
    <select id="economic_phase" name="economic-phase">
      <option value="">Select</option>
      """
    sql_query = "SELECT phase FROM Economy"
    results = pyhtml.get_results_from_query("database/immunisation.db", sql_query)
    for row in results:
      page_html += f"<option value=\"{row[0]}\">{row[0]}</option>"
    
    
    page_html += """</select>
    <label for="disease">Preventable Disease:</label>
    <select id="disease" name="disease">
      <option value="">Select</option>
      """
    sql_query = "SELECT description FROM Infection_Type"
    results = pyhtml.get_results_from_query("database/immunisation.db", sql_query)
    for row in results:
      page_html += f"<option value=\"{row[0]}\">{row[0]}</option>"

    page_html +="""</select>
    <label for="year">Year:</label>
    <select id="year" name="year">
      <option value="">Select</option>
    """
    sql_query = "SELECT * FROM Yeardate"
    results = pyhtml.get_results_from_query("database/immunisation.db", sql_query)
    for row in results:
      page_html += f"<option value=\"{row[0]}\">{row[0]}</option>"
   
   
    page_html +=  f"""</select>
          <!-- Submit + Reset -->
              <button type="submit">Filter</button>
              <a class="reset-link" href="/Infection">Reset</a>
    </div>
  </form>
  <!-- Infection Table -->
  <table class="data-table">
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

    sql_query = f"""SELECT Infection_Type.description, Country.name, Economy.phase,YearDate.YearID,InfectionData.cases
FROM Infection_Type JOIN InfectionData ON Infection_Type.id = InfectionData.inf_type
JOIN Country ON InfectionData.country = Country.CountryID
JOIN Economy ON Country.economy = Economy.economyID
JOIN YearDate ON YearDate.YearID = InfectionData.year
WHERE Economy.phase = '{economic_phase}' AND Infection_Type.description = '{disease}' AND YearDate.YearID = '{year}'"""
   
    results = pyhtml.get_results_from_query("database/immunisation.db", sql_query)
    page_html += f"""
        <tbody id="infection-data">
        """
    for row in results:
      page_html += f"""
        <tr>
          <td>{row[0]}</td>
          <td>{row[1]}</td>
          <td>{row[2]}</td>
          <td>{row[3]}</td>
          <td>{float(row[4])/100000}</td>
        </tr>
        """
    page_html += f"""
        </tbody>
    </table>

  <!-- Separator Line -->
  <hr class="line-separator">

  <!-- Data Summary Section -->
  <h2 class="sub-heading">Data Summary</h2>

  <table class="summary-table">
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
ORDER BY Economy.phase"""
    results = pyhtml.get_results_from_query("database/immunisation.db", sql_query)
    page_html += f"""
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
    page_html += f"""
    </tbody>
  </table>

  <!-- Integrated Footer -->
            {component.footer.footer}
     
        </main>
        </body>
        </html>
    """
    
    return page_html