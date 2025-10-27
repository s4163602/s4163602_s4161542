import component.navbar
import component.footer
import pyhtml

def get_page_html(form_data):
    print("About to return infection Insight page...")
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
        <link rel="stylesheet" href="static/Infection_Insight.css">
        </head>

        <body>
        <!-- Navbar -->
        {component.navbar.navbar}
        <main>
         <h1 class="main-heading">Infection Insight</h1>"""
         
    sql_query = f"""SELECT 
  'Global' AS Country,
  Infection_Type.description AS "Infection Type",
  ROUND((SUM(InfectionData.cases) * 100000.0) / SUM(CountryPopulation.population), 2) 
    AS "Infection per 100,000 people",
  YearDate.YearID AS Year
FROM Country 
JOIN InfectionData 
  ON Country.CountryID = InfectionData.country
JOIN Infection_Type 
  ON Infection_Type.id = InfectionData.inf_type
JOIN CountryPopulation 
  ON CountryPopulation.country = Country.CountryID 
  AND CountryPopulation.year = InfectionData.year
JOIN YearDate 
  ON YearDate.YearID = InfectionData.year
WHERE Infection_Type.description = '{disease}' 
  AND YearDate.YearID = '{year}'             
GROUP BY Infection_Type.description, YearDate.YearID;
"""
    results = pyhtml.get_results_from_query("database/immunisation.db", sql_query)
    global_rate = results[0][2] if results else "--"
    page_html += f"""
         <h2 class="sub-heading"> Global Infection Rate:{global_rate}</h2>
         
         <!-- Filter Section -->
         <form  method="GET">
         <div class="filter-section">
          <label for="disease">Infection Type</label>
          <select id="disease" name="disease">
          <option value="">Select</option>
          """
    sql_query = "SELECT description FROM Infection_Type"
    results = pyhtml.get_results_from_query("database/immunisation.db", sql_query)
    for row in results:
        page_html += f"<option value=\"{row[0]}\">{row[0]}</option>"

    page_html += f"""</select>
    <label for="year">Year:</label>
    <select id="year" name="year">
      <option value="">Select</option>
    """
    sql_query = "SELECT * FROM YearDate"
    results = pyhtml.get_results_from_query("database/immunisation.db", sql_query)
    for row in results:
        page_html += f"<option value=\"{row[0]}\">{row[0]}</option>"
   
    page_html += f"""</select>
          <!-- Submit + Reset -->
              <button type="submit">Filter</button>
              <a class="reset-link" href="/Infection_Insight">Reset</a>
    </div>
  </form>

   <!-- Infection Table -->
  <table class="data-table">
    <thead>
      <tr>
        <th>Country</th>
        <th>Infection Type</th>
        <th>Infection per 100,000 people</th>
        <th>Year</th>
      </tr>
    </thead>
    """

    
    if disease and year:
        sql_query = f"""SELECT 
  'Global' AS Country,
  Infection_Type.description AS "Infection Type",
  ROUND((SUM(InfectionData.cases) * 100000.0) / SUM(CountryPopulation.population), 2) 
    AS "Infection per 100,000 people",
  YearDate.YearID AS Year
FROM Country 
JOIN InfectionData 
  ON Country.CountryID = InfectionData.country
JOIN Infection_Type 
  ON Infection_Type.id = InfectionData.inf_type
JOIN CountryPopulation 
  ON CountryPopulation.country = Country.CountryID 
  AND CountryPopulation.year = InfectionData.year
JOIN YearDate 
  ON YearDate.YearID = InfectionData.year
WHERE Infection_Type.description = '{disease}'
  AND YearDate.YearID = '{year}'
GROUP BY Infection_Type.description, YearDate.YearID

UNION ALL

SELECT 
  Country.name AS Country,
  Infection_Type.description AS "Infection Type",
  ROUND((SUM(InfectionData.cases) * 100000.0) / SUM(CountryPopulation.population), 2) 
    AS "Infection per 100,000 people",
  YearDate.YearID AS Year
FROM Country 
JOIN InfectionData 
  ON Country.CountryID = InfectionData.country
JOIN Infection_Type 
  ON Infection_Type.id = InfectionData.inf_type
JOIN CountryPopulation 
  ON CountryPopulation.country = Country.CountryID 
  AND CountryPopulation.year = InfectionData.year
JOIN YearDate 
  ON YearDate.YearID = InfectionData.year
WHERE Infection_Type.description = '{disease}' 
  AND YearDate.YearID = '{year}'
GROUP BY Country.name, Infection_Type.description, YearDate.YearID
HAVING 
  (SUM(InfectionData.cases) * 100000.0) / SUM(CountryPopulation.population) >
  (
    SELECT (SUM(i2.cases) * 100000.0) / SUM(cp2.population)
    FROM InfectionData i2
    JOIN Infection_Type it2 ON it2.id = i2.inf_type
    JOIN CountryPopulation cp2 ON cp2.country = i2.country AND cp2.year = i2.year
    JOIN YearDate y2 ON y2.YearID = i2.year
    WHERE it2.description = '{disease}' AND y2.YearID = '{year}'
  )
ORDER BY 
   "Infection per 100,000 people" ASC;
"""
        results = pyhtml.get_results_from_query("database/immunisation.db", sql_query)
    else:
        results = []

    
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
