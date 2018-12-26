#
# Scan the local network for the "hue" bridge.
#
# https://docs.python.org/2/library/socket.html
# https://docs.python.org/2/library/urllib2.html
#
import socket
import urllib2


def get_lan_ip_octets():
    """
    Returns our LAN ip as a list of 4 str octets, raises an exception if the hostname isn't a LAN ip.
    """
    hostname = socket.gethostname()
    hostname = socket.gethostbyname(hostname)

    # make sure the hostname is valid
    octets = hostname.split(".")
    assert (len(octets) == 4), "Invalid hostname: %s" % hostname

    # make sure we're connected to a network
    if octets[0] == "127":
        raise Exception("hostname is '%s': looks like we're not connected to a LAN." % hostname)

    return octets


def host_is_bridge(address, port):
    """
    Returns true if this address appears to be a hue bridge.
    Hue bridges are detected by looking for a signature with the HTML.
    """
    signature = "hue personal wireless lighting"
    url = "http://{host}:{port}/".format(host=address, port=port)
    try:
        contents = urllib2.urlopen(url, timeout=0.1).read()
        if signature in contents:
            return True
        else:
            return False
    except urllib2.URLError:
        return False


def scan():
    """
    Returns the ip address of a hue bridge on the local network, or None if one is not found.
    """

    octets = get_lan_ip_octets()

    port = 80

    skip_octets = [
        "1",        # do not bother scanning the router
        octets[3],  # do not bother scanning ourselves
    ]

    for final_octet in range(0, 256):
        final_octet = str(final_octet)

        if final_octet in skip_octets:
            continue

        ip_address = '.'.join([
            octets[0],
            octets[1],
            octets[2],
            final_octet
        ])

        is_bridge = host_is_bridge(ip_address, port)
        if is_bridge:
            return ip_address

    ip_range = ".".join([
        octets[0],
        octets[1],
        octets[2],
        "*"
    ])
    raise Exception("No hue bridge found within '%s'." % ip_range)


if __name__ == '__main__':
    host = scan()
    print(host)
