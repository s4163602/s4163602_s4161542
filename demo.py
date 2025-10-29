import pyhtml
import pages.home
import pages.about
import pages.Infection
import pages.Infection_Insight
import pages.vaccination
import pages.Vaccination_insight
pyhtml.need_debugging_help=True

pyhtml.MyRequestHandler.pages["/"] = pages.home
pyhtml.MyRequestHandler.pages["/about"] = pages.about
pyhtml.MyRequestHandler.pages["/vaccination"] = pages.vaccination
pyhtml.MyRequestHandler.pages["/Infection"] = pages.Infection
pyhtml.MyRequestHandler.pages["/Infection_Insight"] = pages.Infection_Insight
pyhtml.MyRequestHandler.pages["/vaccination_insight"] = pages.Vaccination_insight

pyhtml.host_site()



