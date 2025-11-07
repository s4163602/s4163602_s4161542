import pyhtml
import component.navbar

def get_page_html(form_data):
    print("Rendering Level 2 – Vaccination Rates Page with Two Distinct Tables (state preserved + Excel export)")

    db_path = "database/immunisation.db"

    def get_value(key, default=None):
        val = form_data.get(key)
        if isinstance(val, list) and len(val) > 0:
            return val[0]
        return val if val is not None else default

    var_antigen = str(get_value("var_antigen") or "")
    var_country = str(get_value("var_country") or "")
    var_region = str(get_value("var_region") or "")
    var_year = str(get_value("var_year") or "")
    var_threshold_raw = str(get_value("var_threshold", "90") or "90")
    var_antigen_summary = str(get_value("var_antigen_summary") or "")

    try:
        safe_threshold_int = max(0, min(100, int(float(var_threshold_raw))))
    except:
        safe_threshold_int = 90

    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Vaccination Rates</title>
  <link rel="stylesheet" href="/static/style.css">
  <link rel="stylesheet" href="/static/main.css">
</head>

<body class="page-body">
  {component.navbar.navbar}
  <div class="page-container">

  <h2 id="table1" class="table-heading">Vaccination Rates</h2>

  <form id="form-table1" action="/vaccination#table1" method="GET" class="filter-bar">
    <div class="left-group">
      <select name='var_antigen'><option value=''>Antigen</option>"""

    for a_id, a_name in pyhtml.get_results_from_query(db_path, "SELECT AntigenID, name FROM Antigen ORDER BY name;"):
        selected = " selected" if var_antigen == str(a_id) else ""
        page_html += f"<option value='{a_id}'{selected}>{a_name}</option>"
    page_html += "</select>"

    page_html += "<select name='var_country'><option value=''>Country</option>"
    for (country,) in pyhtml.get_results_from_query(db_path, "SELECT DISTINCT name FROM Country ORDER BY name;"):
        selected = " selected" if var_country == str(country) else ""
        page_html += f"<option value='{country}'{selected}>{country}</option>"
    page_html += "</select>"

    page_html += "<select name='var_region'><option value=''>Region</option>"
    for (region,) in pyhtml.get_results_from_query(db_path, "SELECT DISTINCT region FROM Country WHERE region IS NOT NULL ORDER BY region;"):
        selected = " selected" if var_region == str(region) else ""
        page_html += f"<option value='{region}'{selected}>{region}</option>"
    page_html += "</select>"

    page_html += "<select name='var_year'><option value=''>Year</option>"
    for (year,) in pyhtml.get_results_from_query(db_path, "SELECT DISTINCT year FROM Vaccination ORDER BY year;"):
        selected = " selected" if var_year == str(year) else ""
        page_html += f"<option value='{year}'{selected}>{year}</option>"
    page_html += "</select>"
    page_html += "</div>"

    page_html += f"""
    <div class="right-group">
      <input type="submit" value="Show" class="btn">
      <input type="hidden" name="var_antigen_summary" value="{var_antigen_summary}">
      <input id="hidden-threshold" type="hidden" name="var_threshold" value="{safe_threshold_int}">
    </div>
  </form>
"""

    page_html += """
  <div class="table-container">
    <table id="vaccination-table-1" class="vaccination-table">
      <thead>
        <tr>
          <th>Antigen</th><th>Year</th><th>Country</th><th>Region</th><th>Coverage (%)</th>
        </tr>
      </thead>
      <tbody>
    """
    if var_antigen and var_year:
        query_1 = f"""
        SELECT a.name, v.year, c.name, c.region, ROUND(v.coverage, 1)
        FROM Vaccination v
        JOIN Country c ON v.country = c.CountryID
        JOIN Antigen a ON v.antigen = a.AntigenID
        WHERE v.antigen = '{var_antigen}' AND v.year = {int(var_year)}
          {"AND c.name = '" + var_country.replace("'", "''") + "'" if var_country else ""}
          {"AND c.region = '" + var_region.replace("'", "''") + "'" if var_region else ""}
        ORDER BY c.region, c.name;
        """
        results_1 = pyhtml.get_results_from_query(db_path, query_1)
        if results_1:
            for antigen, year, country, region, pct in results_1:
                page_html += f"<tr><td>{antigen}</td><td>{year}</td><td>{country}</td><td>{region}</td><td>{pct}%</td></tr>"
        else:
            page_html += "<tr><td colspan='5' style='text-align:center;'>No data matches filters.</td></tr>"
    else:
        page_html += "<tr><td colspan='5' style='text-align:center;'>Select filters and click Show.</td></tr>"
    page_html += "</tbody></table></div>"

    page_html += f"""
  <hr style="margin:2rem 0; border:none; border-top:1px solid #e5e7eb;">
  <h2 id="table2" class="table-heading">Data Summary by Threshold</h2>

  <form id="form-table2" action="/vaccination#table2" method="GET" class="filter-bar">
    <div class="left-group">
      <select name='var_antigen_summary'><option value=''>Antigen</option>"""
    for a_id, a_name in pyhtml.get_results_from_query(db_path, "SELECT AntigenID, name FROM Antigen ORDER BY name;"):
        selected = " selected" if var_antigen_summary == str(a_id) else ""
        page_html += f"<option value='{a_id}'{selected}>{a_name}</option>"
    page_html += f"""</select>
      <input type="number" name="var_threshold" min="0" max="100" value="{safe_threshold_int}" class="threshold-input" id="threshold-input">
    </div>
    <div class="right-group">
      <input type="submit" value="Show" class="btn">
      <input type="hidden" name="var_antigen" value="{var_antigen}">
      <input type="hidden" name="var_country" value="{var_country}">
      <input type="hidden" name="var_region" value="{var_region}">
      <input type="hidden" name="var_year" value="{var_year}">
    </div>
  </form>
"""

    page_html += f"""
  <div class="table-container">
    <table id="vaccination-table-2" class="vaccination-table">
      <thead>
        <tr>
          <th>Antigen</th><th>Year</th><th id="th-threshold">Countries ≥ {safe_threshold_int}%</th><th>Region</th>
        </tr>
      </thead>
      <tbody>
    """
    if var_antigen_summary:
        query_2 = f"""
        SELECT a.name AS antigen_name, v.year AS year, COUNT(c.CountryID) AS num_countries, c.region AS region
        FROM Vaccination v
        JOIN Country c ON v.country = c.CountryID
        JOIN Antigen a ON v.antigen = a.AntigenID
        WHERE v.antigen = '{var_antigen_summary}' AND v.coverage >= {safe_threshold_int}
        GROUP BY a.name, v.year, c.region
        ORDER BY v.year, num_countries DESC;
        """
        results_2 = pyhtml.get_results_from_query(db_path, query_2)
        if results_2:
            for antigen, year, num, region in results_2:
                page_html += f"<tr><td>{antigen}</td><td>{year}</td><td>{num}</td><td>{region}</td></tr>"
        else:
            page_html += "<tr><td colspan='4' style='text-align:center;'>No regions meet this threshold.</td></tr>"
    else:
        page_html += "<tr><td colspan='4' style='text-align:center;'>Select antigen and threshold to view summary.</td></tr>"
    page_html += "</tbody></table></div>"

    page_html += f"""
  </div>
<script>
  (function() {{
    var th = document.getElementById('th-threshold');
    var input = document.getElementById('threshold-input');
    var hidden = document.getElementById('hidden-threshold');

    function clamp(n) {{
      var v = parseInt(n, 10);
      if (isNaN(v)) v = {safe_threshold_int};
      return Math.max(0, Math.min(100, v));
    }}

    function sync() {{
      if (!input) return;
      var v = clamp(input.value);
      if (th) th.textContent = 'Countries ≥ ' + v + '%';
      if (hidden) hidden.value = v; // keep form 1 threshold aligned
    }}

    if (input) {{
      input.addEventListener('input', sync);
      input.addEventListener('change', sync);
      input.addEventListener('blur', sync);
      // initialize on load
      sync();
    }}
  }})();
</script>
</body>
</html>
"""
    return page_html
