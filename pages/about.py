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
            <img src="" alt="Persona Image">
            <p><b>Name:</b> John Doe</p>
            <p><b>Age:</b> 34</p>
            <p><b>Info:</b> Health policy advisor working with vaccination data.</p>
            <p><b>Purpose:</b> Uses website to compare infection trends and vaccination rates.</p>
        </section>

        <section class="team" id="team">
            <h1>Team Members:</h1>
      
            <p><b>Name:</b> Syed Tawsif Mahmood</p>
            <p><b>Student ID:</b>s4161542</p>
            
            <p><b>Name:</b> Kiet Lark</p>
            <p><b>Student ID:</b> s4153663</p>
        </section>




     <!-- Integrated Footer -->
            {component.footer.footer}
     
        </main>
        </body>
        </html>
    """
    return page_html     