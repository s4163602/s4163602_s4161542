import component.navbar
import component.footer
def get_page_html(form_data):
    print("About to return page home page...")
    page_html= f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Global Vaccination Dashboard</title>
        <link rel="stylesheet" href="static/home.css">
        <link rel="stylesheet" href="static/main.css">
        </head>

        <body>
        <!-- Navbar -->
        {component.navbar.navbar}
        <!-- Main Scrollable Sections -->
        <main>
            <section class="hero" id="hero">
            <h1>Global Vaccination and Infection Data</h1>
x            <div class="hero-buttons">
                <button class="btn btn-primary">Explore Vaccination</button>
                <button class="btn btn-outline">Explore Infection</button>
            </div>
            </section>

            <section class="facts" id="facts">
            <div class="facts-content">
                <div class="facts-text">
                <h2>Vaccination Progress<br>from 2000 to 2025</h2>
                <p>Comprehensive data tracking global health inventions and their outcomes.</p>
                </div>
                <div class="facts-grid">
                <div class="fact-box">Fact</div>
                <div class="fact-box">Fact</div>
                <div class="fact-box">Fact</div>
                <div class="fact-box">Fact</div>
                </div>
            </div>
            </section>

            <!-- Insights + Integrated Footer -->
            <section class="insights" id="insights">
            <div class="insights-content">
                <h3>Dive deep into global health data</h3>
                <p>Explore detailed vaccination rates, infection trends, and public health insights across different regions and economic groups.</p>
                <div class="insight-buttons">
                <button class="btn btn-primary">Vaccination Insights</button>
                <button class="btn btn-outline">Infection Insights</button>
                </div>
            </div>

            <!-- Integrated Footer -->
            {component.footer.footer}
            </section>
        </main>
        </body>
        </html>
    """
    return page_html