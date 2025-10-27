import pyhtml
import pages.home
import pages.data_explorer.vaccination

pyhtml.need_debugging_help=True

pyhtml.MyRequestHandler.pages["/"] = pages.home
pyhtml.MyRequestHandler.pages["/data_explorer/vaccination"] = pages.data_explorer.vaccination

pyhtml.host_site()