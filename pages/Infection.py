import component.navbar
import component.footer

def get_page_html(form_data):
    print("About to return about page...")
    page_html= f"""
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
        <main class="container">
        <section class="section" id="infection-section">
           <h1 class="page-title">Infection</h1>

        <!-- Filters -->
        <form class="filters" id="filters" method="GET" action="">
        <div class="filter">
          <label for="economic_phase">Economic Phase</label>
          <select id="economic_phase" name="economic_phase">
            <option value="">All</option>
            <!-- Fill options from DB later -->
          </select>
        </div>

        <div class="filter">
          <label for="preventable_disease">Preventable disease</label>
          <select id="preventable_disease" name="preventable_disease">
            <option value="">All</option>
            <!-- Fill options from DB later -->
          </select>
        </div>

        <div class="filter">
          <label for="year">Year</label>
          <select id="year" name="year">
            <option value="">All</option>
            <!-- Fill options from DB later -->
          </select>
        </div>
        </form>

        <!-- Main data table -->
        <div class="table-wrap">
        <table class="table" id="infection-table" aria-describedby="infection-caption">
            <caption id="infection-caption" class="sr-only">
            */Infection data table filtered by the dropdowns above.
          </caption>
          <thead>
            <tr>
              <th scope="col">Preventable Disease</th>
              <th scope="col">Country</th>
              <th scope="col">Economic Phase</th>
              <th scope="col">Year</th>
              <th scope="col">Cases per 100,000 people</th>
            </tr>
          </thead>
          <tbody>
            <!-- Inject <tr> rows from Python/SQLite here -->
            <tr class="placeholder">
              <td colspan="5">No data yet — choose filters or load from database.</td>
            </tr>
            </tbody>
            </table>
             </div>
            </section>

    <!-- Section separator line -->
    <hr class="section-divider" />

    <section class="section" id="summary-section">
      <h2 class="section-title">Data Summary</h2>

      <div class="table-wrap">
        <table class="table" id="summary-table" aria-describedby="summary-caption">
          <caption id="summary-caption" class="sr-only">
            Summary of infection data (aggregated).
          </caption>
          <thead>
            <tr>
              <th scope="col">Preventable Disease</th>
              <th scope="col">Economic Phase</th>
              <th scope="col">Year</th>
              <th scope="col">Cases</th>
            </tr>
          </thead>
          <tbody>
            <!-- Inject summary rows from Python/SQLite here -->
            <tr class="placeholder">
              <td colspan="4">Summary will appear after data loads.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </main>

         <!-- Integrated Footer -->
            {component.footer.footer}
</body>
</html>   
 """
   
    return page_html   