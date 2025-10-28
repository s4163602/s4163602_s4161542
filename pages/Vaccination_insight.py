import pyhtml
import component.navbar
import component.footer

def get_page_html(form_data):
    print("Rendering Level 3 – Biggest Improvement in Vaccination Rates (4-column, styled threshold input)")

    db_path = "database/immunisation.db"

    def get_value(key, default=None):
        val = form_data.get(key)
        if isinstance(val, list) and len(val) > 0:
            return val[0]
        return val if val is not None else default

    # -------- form state --------
    var_antigen    = str(get_value("var_antigen") or "")
    var_start_year = str(get_value("var_start_year") or "")
    var_end_year   = str(get_value("var_end_year") or "")
    var_topn       = str(get_value("var_topn", "10") or "10")

    try:
        safe_topn = max(1, int(var_topn))
    except:
        safe_topn = 10

    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Vaccination Rate Improvements</title>
  <link rel="stylesheet" href="/static/style.css">
  <link rel="stylesheet" href="/static/main.css">
  <style>
    /* --- Threshold input styling --- */
    .threshold-input {{
      border: 1px solid #d1d5db;
      border-radius: 0.5rem;
      padding: 0.4rem 0.75rem;
      width: 5rem;
      font-size: 0.95rem;
      text-align: center;
      transition: all 0.2s ease-in-out;
      outline: none;
    }}
    .threshold-input:focus {{
      border-color: #2563eb;
      box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.3);
    }}
    .threshold-label {{
      margin-left: 0.5rem;
      font-size: 0.95rem;
      color: #374151;
      font-weight: 500;
    }}
  </style>
</head>

<body class="page-body">
  {component.navbar.navbar}
  <div class="page-container">

    <h2 id="table1" class="table-heading">Biggest Improvements in Vaccination Rate</h2>

    <form action="/vaccination_insight#table1" method="GET" class="filter-bar">
      <div class="left-group">
        <select name="var_antigen">
          <option value="">Antigen</option>"""

    # Antigen dropdown
    for a_id, a_name in pyhtml.get_results_from_query(db_path, "SELECT AntigenID, name FROM Antigen ORDER BY name;"):
        selected = " selected" if var_antigen == str(a_id) else ""
        page_html += f"<option value='{a_id}'{selected}>{a_name}</option>"
    page_html += "</select>"

    # Start Year
    page_html += "<select name='var_start_year'><option value=''>Start year</option>"
    for (year,) in pyhtml.get_results_from_query(db_path, "SELECT DISTINCT year FROM Vaccination ORDER BY year;"):
        selected = " selected" if var_start_year == str(year) else ""
        page_html += f"<option value='{year}'{selected}>{year}</option>"
    page_html += "</select>"

    # End Year
    page_html += "<select name='var_end_year'><option value=''>End year</option>"
    for (year,) in pyhtml.get_results_from_query(db_path, "SELECT DISTINCT year FROM Vaccination ORDER BY year;"):
        selected = " selected" if var_end_year == str(year) else ""
        page_html += f"<option value='{year}'{selected}>{year}</option>"
    page_html += "</select>"

    page_html += f"""
        <label class="threshold-label" for="var_topn">Top:</label>
        <input type="number" id="var_topn" name="var_topn" min="1" value="{safe_topn}" class="threshold-input" />
      </div>

      <div class="right-group">
        <input type="submit" value="Show" class="btn">
        <button type="button" class="download-btn" data-target="improvement-table">⬇ Download Excel</button>
      </div>
    </form>

    <div class="table-container">
      <table id="improvement-table" class="vaccination-table">
        <thead>
          <tr>
            <th>Country</th>
            <th>Vaccination Rate Increase</th>
            <th>Start Year</th>
            <th>End Year</th>
          </tr>
        </thead>
        <tbody>
    """

    if var_antigen and var_start_year and var_end_year:
        try:
            y0 = int(var_start_year)
            y1 = int(var_end_year)
        except:
            y0, y1 = None, None

        if y0 is not None and y1 is not None and y1 >= y0:
            query = f"""
            WITH base AS (
              SELECT v.country, v.year, AVG(v.coverage) AS coverage_avg
              FROM Vaccination v
              WHERE v.antigen = '{var_antigen}'
                AND v.year IN ({y0}, {y1})
                AND v.coverage BETWEEN 0 AND 100
              GROUP BY v.country, v.year
            ),
            paired AS (
              SELECT country,
                     MAX(CASE WHEN year = {y0} THEN coverage_avg END) AS start_cov,
                     MAX(CASE WHEN year = {y1} THEN coverage_avg END) AS end_cov
              FROM base
              GROUP BY country
            )
            SELECT c.name AS country_name,
                   ROUND(end_cov - start_cov, 1) AS increase_pct,
                   {y0} AS start_year,
                   {y1} AS end_year
            FROM paired p
            JOIN Country c ON c.CountryID = p.country
            WHERE p.start_cov IS NOT NULL AND p.end_cov IS NOT NULL
              AND end_cov BETWEEN 0 AND 100
              AND start_cov BETWEEN 0 AND 100
            ORDER BY increase_pct DESC, country_name ASC
            LIMIT {safe_topn};
            """
            rows = pyhtml.get_results_from_query(db_path, query)

            if rows:
                for (country, increase_pct, start_year, end_year) in rows:
                    page_html += (
                        f"<tr>"
                        f"<td>{country}</td>"
                        f"<td>{increase_pct:.1f}%</td>"
                        f"<td>{start_year}</td>"
                        f"<td>{end_year}</td>"
                        f"</tr>"
                    )
            else:
                page_html += "<tr><td colspan='4' style='text-align:center;'>No matching data for these filters.</td></tr>"
        else:
            page_html += "<tr><td colspan='4' style='text-align:center;'>End year must be ≥ start year.</td></tr>"
    else:
        page_html += "<tr><td colspan='4' style='text-align:center;'>Select antigen, start year, and end year, then click Show.</td></tr>"

    page_html += """
        </tbody>
      </table>
    </div>

  </div>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.core.min.js"></script>
  <script>
    function exportTableToExcel(tableId, filename) {
      var table = document.getElementById(tableId);
      if (!table) return;
      var wb = XLSX.utils.table_to_book(table, { sheet: "Sheet1" });
      XLSX.writeFile(wb, filename);
    }

    document.querySelectorAll('.download-btn[data-target]').forEach(function(btn) {
      btn.addEventListener('click', function() {
        var targetId = this.getAttribute('data-target');
        var filename = "vaccination_improvement_4cols.xlsx";
        exportTableToExcel(targetId, filename);
      });
    });
  </script>
</body>
</html>
"""
    return page_html
