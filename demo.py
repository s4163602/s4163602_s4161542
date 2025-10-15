import pyhtml
import pages.home


pyhtml.need_debugging_help=True

#All pages that you want on the site need to be added as below
pyhtml.MyRequestHandler.pages["/"] = pages.home

#Host the site!
pyhtml.host_site()