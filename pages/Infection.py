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
        <main>
       <h1 class="main-heading">Infection</h1>

  <!-- Filter Section -->
  <div class="filter-section">
    <label for="economic-phase">Economic Phase:</label>
    <select id="economic-phase" name="economic-phase">
      <option value="">Select</option>
      <option value="developed">Developed</option>
      <option value="developing">Developing</option>
    </select>

    <label for="disease">Preventable Disease:</label>
    <select id="disease" name="disease">
      <option value="">Select</option>
      <option value="measles">Measles</option>
      <option value="polio">Polio</option>
    </select>

    <label for="year">Year:</label>
    <select id="year" name="year">
      <option value="">Select</option>
      <option value="2020">2020</option>
      <option value="2021">2021</option>
      <option value="2022">2022</option>
    </select>
  </div>

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
    <tbody id="infection-data">
      <tr>
        <td>Measles</td>
        <td>Australia</td>
        <td>Developed</td>
        <td>2022</td>
        <td>2.5</td>
      </tr>
      <tr>
        <td>Polio</td>
        <td>India</td>
        <td>Developing</td>
        <td>2021</td>
        <td>14.2</td>
      </tr>
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
    <tbody id="summary-data">
      <tr>
        <td>Measles</td>
        <td>Developed</td>
        <td>2022</td>
        <td>250</td>
      </tr>
      <tr>
        <td>Polio</td>
        <td>Developing</td>
        <td>2021</td>
        <td>1400</td>
      </tr>
    </tbody>
  </table>

  <!-- Integrated Footer -->
            {component.footer.footer}
     
        </main>
        </body>
        </html>
    """
    
    return page_html