#!/usr/bin/env python3

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

import sys
sys.stdout = Unbuffered(sys.stdout)

import time
import socket
from optparse import OptionParser

try:
    import dns.resolver, dns.zone
except ImportError:
    print("Please install dnspython3:")
    print("$ sudo pip install dnspython3")
    sys.exit(1)

sleeptime = 1
resolver_timeout = 2
resolver_lifetime = 2

def parsezonefile(zone, zonefile):
    zone = dns.zone.from_file(opts.zonefile, origin=opts.zone, relativize=False, check_origin=False)
    return zone

def compare_dns_reponse(name, rdataset, primary_nameserver, secondary_nameserver):
    checkfail = False
    primarycheck = False
    secondarycheck = False




    print("DNS Record :", name, "(" + dns.rdatatype.to_text(rdataset.rdtype) + ")\t\t\t",  end=" ")
    if rdataset.rdtype == dns.rdatatype.SOA or rdataset.rdtype == dns.rdatatype.NS:
        print("==> SKIP SOA and NS Type")
    else:
        try:
            primaryresolver = dns.resolver.Resolver(configure=False)
            primaryresolver.nameservers = primary_nameserver
            primaryresolver.timeout = resolver_timeout
            primaryresolver.lifetime = resolver_lifetime
            primaryanswer = primaryresolver.query(name, rdataset.rdtype, rdataset.rdclass)
        except dns.resolver.NXDOMAIN:
            print("==> Error!!!! Primary Nameserver has not record")
            checkfail = True
        except dns.exception.Timeout:
            print("Primary Timeout (retry)",  end=" ")
            time.sleep(5)
            # timeout, try init resolver
            primaryresolver = dns.resolver.Resolver(configure=False)
            primaryresolver.nameservers = primary_nameserver
            primaryresolver.timeout = resolver_timeout
            primaryresolver.lifetime = resolver_lifetime
            primaryanswer = primaryresolver.query(name, rdataset.rdtype, rdataset.rdclass)

        try:
            secondaryresolver = dns.resolver.Resolver(configure=False)
            secondaryresolver.nameservers = secondary_nameserver
            secondaryresolver.timeout = resolver_timeout
            secondaryresolver.lifetime = resolver_lifetime
            secondaryanswer = secondaryresolver.query(name, rdataset.rdtype, rdataset.rdclass)
        except dns.resolver.NXDOMAIN:
            print("==> Error!!!! Secondary Nameserver has not record")
            checkfail = True
        except dns.exception.Timeout:
            print("Secondary Timeout (retry)",  end=" ")
            time.sleep(5)
            # timeout, try init resolver
            secondaryresolver = dns.resolver.Resolver(configure=False)
            secondaryresolver.nameservers = secondary_nameserver
            secondaryresolver.timeout = resolver_timeout
            secondaryresolver.lifetime = resolver_lifetime
            secondaryanswer = secondaryresolver.query(name, rdataset.rdtype, rdataset.rdclass)

        if checkfail == False:
            if primaryanswer.rrset == secondaryanswer.rrset:
                print("==> Primary and Secondary Nameserver data is Equal")
            else:
                print("==> Error!!!! Primary and Secondary Nameserver data is not Equal")
        time.sleep(sleeptime)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-z", "--zone", dest="zone", metavar="DOMAIN",
                        help="name of the domain we're checking (eg: domain.com)")
    parser.add_option("-f", "--file", dest="zonefile", metavar="FILE",
                        help="zone file to load records from")
    parser.add_option("-p", "--primarynameserver", dest="primarynameserver", metavar="PNAMESERVER",
                        help="IP of primary nameserver use [default: 8.8.8.8] (Google DNS)", default="8.8.8.8")
    parser.add_option("-s", "--secondarynameserver", dest="secondarynameserver", metavar="SNAMESERVER",
                        help="IP of primary nameserver use [default: 1.1.1.1] (Cloudflare DNS)", default="1.1.1.1")
    (opts, remaining_args) = parser.parse_args()

    print("Primary Nameserver : ", opts.primarynameserver+" (" + socket.gethostbyname(opts.primarynameserver) + ")")
    print("Secondary Nameserver : ", opts.secondarynameserver+" (" + socket.gethostbyname(opts.secondarynameserver) + ")")

    primary_nameserver = [socket.gethostbyname(opts.primarynameserver)]
    secondary_nameserver = [socket.gethostbyname(opts.secondarynameserver)]

    zonefiler = parsezonefile(opts.zone, opts.zonefile)
    for (name, rdataset) in zonefiler.iterate_rdatasets():
        compare_dns_reponse(name, rdataset, primary_nameserver, secondary_nameserver)
