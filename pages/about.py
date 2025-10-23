import component.navbar
import component.footer
import pyhtml

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
        <link rel="stylesheet" href="static/about.css">
        </head>

        <body>
        <!-- Navbar -->
        {component.navbar.navbar}
        
        <main>
        <section class="mission" id="mission">
        <h1><b>Mission:</b></h1>
        <p> The website provides accurate and up-to-date infection and vaccination data to support informed analysis and evidence-based decision-making. 
        It serves as a reliable and authentic platform that ensures the information presented is genuine, current, and clearly structured for easy understanding and research use</p>
        </section>

        <section class="usage" id="usage">
        <h1>How to use this site:</h1>
        <p> To use this website, navigate through the various sections using the menu bar at the top.
        Explore the interactive charts and graphs to analyze infection trends and vaccination rates.
        Utilize the filters and options available to customize the data view according to your research needs.</p>
        </section>
         
        
        <section class="personas" id="personas">
        <h1>Personas:</h1>
            """
    sql_query = "SELECT * FROM Persona;"
    results = pyhtml.get_results_from_query("database/immunisation.db", sql_query)
    for row in results:
            page_html += f"""
            <div class="user-persona">
                <image src="{row[6]}" alt="Persona Image" width="150" height="150"/>
                <p><b>Name:</b> {row[1]}</p>
                <p><b>Age:</b> {row[2]}</p>
                <p><b>Sex:</b> {row[3]}</p>
                <p><b>Occupation:</b> {row[4]}</p>
                <p><b>Purpose:</b> {row[5]}</p>
            </div>
            """

    page_html += """
        </section>

        <section class="team" id="team">
            <h1>Team Members:</h1>
        """
    sql_query = "SELECT * FROM Team_Member;"
    results = pyhtml.get_results_from_query("database/immunisation.db", sql_query)
        
    for row in results:
            page_html += f"""
            <div class="member">
                <p><b>Student ID:</b> {row[0]} , <b>Name:</b> {row[1]}</p>
            </div>
            """



    page_html += f"""    </section>
     <!-- Integrated Footer -->
            {component.footer.footer}
    </main> 
     </body>
    </html>
    """

    return page_html




        