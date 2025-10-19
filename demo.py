import pyhtml
import pages.home
import pages.about

pyhtml.need_debugging_help=True

#All pages that you want on the site need to be added as below
pyhtml.MyRequestHandler.pages["/"] = pages.home
pyhtml.MyRequestHandler.pages["/about"] = pages.about

#Host the site!
pyhtml.host_site()

