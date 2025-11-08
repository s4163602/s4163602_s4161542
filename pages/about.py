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
        <p> This website aims to deliver accurate, reliable, and up-to-date information on infection and vaccination data. Its purpose is to support informed analysis, academic study, and evidence-based decision-making in the medical and health sectors. The platform ensures that all data presented is authentic, verified, and clearly structured, enabling users to easily interpret and apply the information for research, professional insights, and policy development.</p>
        </section>

        <section class="usage" id="usage">
        <h1>How to use this site:</h1>
        <p> To explore the website, use the navigation menu at the top of the page. The Data Explorer section allows you to view and compare infection and vaccination trends through interactive tables. You can apply various filters and selection options to customize the data according to specific diseases, years, or economic phases etc. The Insights section provides analytical comparisons and key observations based on the latest datasets, helping users draw meaningful conclusions. Each section is designed to be intuitive and informative, ensuring a seamless experience for researchers, students, and professionals seeking credible health data.</p>
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




        