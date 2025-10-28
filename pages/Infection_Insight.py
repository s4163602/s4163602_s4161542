import component.navbar
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
        <title>Infection Insight</title>
        <!-- Use the same shared styles as other pages -->
        <link rel="stylesheet" href="/static/style.css">
        <link rel="stylesheet" href="/static/main.css">
        </head>

        <body class="page-body">
        {component.navbar.navbar}
        <div class="page-container">
    """

    
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
          <h2 class="table-heading">Global Infection Rate: {global_rate}</h2>

          <!-- Filters -->
          <form method="GET" class="filter-bar">
            <div class="left-group">
              <select id="disease" name="disease">
                <option value="">Infection Type</option>
    """
    
    sql_query = "SELECT description FROM Infection_Type"
    results = pyhtml.get_results_from_query("database/immunisation.db", sql_query)
    for row in results:
        val = str(row[0])
        selected = " selected" if disease == val else ""
        page_html += f"<option value=\"{val}\"{selected}>{val}</option>"

    page_html += """
              </select>

              <select id="year" name="year">
                <option value="">Year</option>
    """
    
    sql_query = "SELECT * FROM YearDate"
    results = pyhtml.get_results_from_query("database/immunisation.db", sql_query)
    for row in results:
        val = str(row[0])
        selected = " selected" if year == val else ""
        page_html += f"<option value=\"{val}\"{selected}>{val}</option>"

    page_html += f"""
              </select>
            </div>

            <div class="right-group">
              <input type="submit" value="Show" class="btn">
            </div>
          </form>

          <!-- Infection Table -->
          <div class="table-container">
            <table id="infection-insight-table" class="vaccination-table">
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
        table_rows = pyhtml.get_results_from_query("database/immunisation.db", sql_query)
    else:
        table_rows = []

    page_html += """
              <tbody id="summary-data">
    """
    if table_rows:
        for row in table_rows:
            page_html += f"""
                <tr>
                    <td>{row[0]}</td>
                    <td>{row[1]}</td>
                    <td>{row[2]}</td>
                    <td>{row[3]}</td>
                </tr>
            """
    else:
        page_html += """
                <tr><td colspan="4" style="text-align:center;">Select an infection type and year, then click Show.</td></tr>
        """

    page_html += f"""
              </tbody>
            </table>
          </div>

        </div> 

        </body>
        </html>
    """

    return page_html
