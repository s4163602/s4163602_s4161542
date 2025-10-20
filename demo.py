import pyhtml
import pages.home
import pages.about
import pages.Infection

pyhtml.need_debugging_help=True

#All pages that you want on the site need to be added as below
pyhtml.MyRequestHandler.pages["/"] = pages.home
pyhtml.MyRequestHandler.pages["/about"] = pages.about
pyhtml.MyRequestHandler.pages["/Infection"] = pages.Infection

#Host the site!
pyhtml.host_site()

