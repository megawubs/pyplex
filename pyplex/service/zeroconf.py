import avahi, dbus, sys, platform, gobject, threading
from ..pyplexlogger.logger import pyPlexLogger
from dbus import DBusException
from dbus.mainloop.glib import DBusGMainLoop
from ..interfaces.server import Server

class ZeroconfService:
    """A simple class to publish a network service with zeroconf using
    avahi.
    """
    def __init__(self, name, port, stype="_plexclient._tcp", domain="", host="", text=""):
        self.name = name
        self.stype = stype
        self.domain = domain
        self.host = host
        self.port = port
        self.text = text
        self.l = pyPlexLogger('ZeroconfService').logger

    def publish(self):
        bus = dbus.SystemBus()
        self.server = dbus.Interface(
                         bus.get_object(
                                 avahi.DBUS_NAME,
                                 avahi.DBUS_PATH_SERVER),
                        avahi.DBUS_INTERFACE_SERVER)

        g = dbus.Interface(
                    bus.get_object(avahi.DBUS_NAME,
                                   self.server.EntryGroupNew()),
                    avahi.DBUS_INTERFACE_ENTRY_GROUP)

        g.AddService(avahi.IF_UNSPEC, avahi.PROTO_UNSPEC,dbus.UInt32(0),
                     self.name, self.stype, self.domain, self.host,
                     dbus.UInt16(self.port), self.text)

        g.Commit()
        self.group = g
        print 'Service published'
        self.l.info('Published avahi Service')
        self.l.info('Name: %s' % self.name)
        self.l.info('Port: %s' % self.port)
        self.l.info('Domain: %s' % self.domain)
        self.l.info('Host: %s' % self.host)
        self.l.info('Text: %s' % self.text)

    def unpublish(self):
        self.group.Reset()

class AvahiLookUp():
    # http://avahi.org/wiki/PythonBrowseExample
    # Looks for iTunes shares

    def __init__(self, TYPE):
        
        self.services = []
        self.servers = []
        loop = DBusGMainLoop()

        bus = dbus.SystemBus(mainloop=loop)
        dbus.set_default_main_loop(loop)

        self.server = dbus.Interface(bus.get_object(avahi.DBUS_NAME, '/'), 'org.freedesktop.Avahi.Server')

        sbrowser = dbus.Interface(bus.get_object(avahi.DBUS_NAME, self.server.ServiceBrowserNew(avahi.IF_UNSPEC, avahi.PROTO_UNSPEC, TYPE, 'local', dbus.UInt32(0))), avahi.DBUS_INTERFACE_SERVICE_BROWSER)

        sbrowser.connect_to_signal("ItemNew", self.myhandler)

        self.GObj = gobject.MainLoop()
        self.GObj.run()


    def service_resolved(self, *args):
        name = args[2]
        address = args[7]
        port = args[8]
        service = {"name": name, "address": address, "port": port}
        server = Server(address, port)
        self.services.append(service)
        self.servers.append(server)
        self.GObj.quit()

    def print_error(self, *args):
        print 'error_handler'
        print args[0]

    def myhandler(self, interface, protocol, name, stype, domain, flags):
        if flags & avahi.LOOKUP_RESULT_LOCAL:
                pass

        self.server.ResolveService(interface, protocol, name, stype, 
            domain, avahi.PROTO_UNSPEC, dbus.UInt32(0), 
            reply_handler=self.service_resolved, error_handler=self.print_error)