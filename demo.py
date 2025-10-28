import pyhtml
import pages.home
import pages.about
import pages.Infection
import pages.Infection_Insight
import pages.vaccination
pyhtml.need_debugging_help=True

pyhtml.MyRequestHandler.pages["/"] = pages.home
pyhtml.MyRequestHandler.pages["/about"] = pages.about
pyhtml.MyRequestHandler.pages["/vaccination"] = pages.vaccination
pyhtml.MyRequestHandler.pages["/Infection"] = pages.Infection
pyhtml.MyRequestHandler.pages["/Infection_Insight"] = pages.Infection_Insight

#Host the site!
pyhtml.host_site()



