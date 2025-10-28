import component.navbar
import component.footer

def get_page_html(form_data):
    print("About to return page home page...")
    page_html = f"""
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
            {component.navbar.navbar}
            <main>
                <section class="hero" id="hero">
                    <h1>Global Vaccination and Infection Data</h1>
                    <p>Unbiased data tracking vaccine impact across countries. Clear, transparent information for researchers and policymakers.</p>
                    <div class="hero-buttons">
                        <a href="/vaccination" class="btn btn-primary">Explore Vaccination</a>
                        <a href="/Infection" class="btn btn-outline">Explore Infection</a>
                    </div>
                </section>

                <section class="facts" id="facts">
                    <div class="facts-content">
                        <div class="facts-text">
                            <h2>Facts</h2>
                            <p>Comprehensive data tracking global health inventions and their outcomes.</p>
                        </div>
                        <div class="facts-grid">
                            <div class="fact-box">Data available from 2000 to 2024</div>
                            <div class="fact-box">Data about 5 antigens: RCV1, MCV1, MCV2, DTPCV1, and DTPCV3</div>
                            <div class="fact-box">Data about 3 diseases: 3 diseases, Measles, Rubella, Pertussis RCV1</div>
                            <div class="fact-box">19,232,497 reported infected cases</div>
                        </div>
                    </div>
                </section>

                <section class="insights" id="insights">
                    <div class="insights-content">
                        <h3>Dive deep into global health data</h3>
                        <p>Explore detailed vaccination rates, infection trends, and public health insights across different regions and economic groups.</p>
                        <div class="insight-buttons">
                            <a href="/vaccination_insight" class="btn btn-primary">Vaccination Insights</a>
                            <a href="/Infection_Insight" class="btn btn-outline">Infection Insights</a>
                        </div>
                    </div>
                </section>
                {component.footer.footer}
            </main>
        </body>
        </html>
    """
    return page_html
