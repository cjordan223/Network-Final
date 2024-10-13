#!env python

# This is a mininet networt script for CST311 Programming Assignment 4.
__author__ = "NeoWeb"
__credits__ = ["Nathan Nawrocki", "Tyler Thompson",
               "Matthew Perona", "Conner Jordan"]

# Import necessary modules from the Mininet library
import time
from mininet.net import Mininet
from mininet.node import Controller, Host, Node
from mininet.node import OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.term import makeTerm

# Define a function for creating the Mininet network


def myNetwork():
    # Create a Mininet instance with some basic configurations
    net = Mininet(topo=None, build=False, ipBase='10.0.0.0/24')

    # Add a controller named 'c0' to the network
    info('*** Adding controller\n')
    c0 = net.addController(
        name='c0', controller=Controller, protocol='tcp', port=6633)

    # Add two switches named 's1' and 's2' to the network
    info('*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)

    # Add three routers with IP addresses to the network
    info('*** Add routers\n')
    r3 = net.addHost('r3', cls=Node, ip='10.0.1.254/24')
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')
    r4 = net.addHost('r4', cls=Node, ip='192.168.1.2/30')
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')
    r5 = net.addHost('r5', cls=Node, ip='192.168.2.2/30')
    r5.cmd('sysctl -w net.ipv4.ip_forward=1')

    # Add four hosts with IP addresses and default routes to the network
    info('*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.1.1/24',
                     defaultRoute='via 10.0.1.254')
    h2 = net.addHost('h2', cls=Host, ip='10.0.1.2/24',
                     defaultRoute='via 10.0.1.254')
    h3 = net.addHost('h3', cls=Host, ip='10.0.2.1/24',
                     defaultRoute='via 10.0.2.254')
    h4 = net.addHost('h4', cls=Host, ip='10.0.2.2/24',
                     defaultRoute='via 10.0.2.254')

    # Add links to connect hosts and switches, routers and switches
    info('*** Add links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s2)
    net.addLink(h4, s2)
    net.addLink(s1, r3, intfName2='r3-eth1', params2={'ip': '10.0.1.254/24'})
    net.addLink(r3, r4, intfName1='r3-eth0', intfName2='r4-eth0',
                params1={'ip': '192.168.1.1/30'}, params2={'ip': '192.168.1.2/30'})
    net.addLink(r4, r5, intfName1='r4-eth1', intfName2='r5-eth0',
                params1={'ip': '192.168.2.1/30'}, params2={'ip': '192.168.2.2/30'})
    net.addLink(s2, r5, intfName2='r5-eth1', params2={'ip': '10.0.2.254/24'})

    # Start the Mininet network
    info('*** Starting network\n')
    net.build()

    # Start the controllers
    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    # Start the switches
    info('*** Starting switches\n')
    s1.start([c0])
    s2.start([c0])

    info('*** Post configure switches and hosts\n')

    # Configure static routes on routers
    r3.cmd('route add -net 10.0.2.0/24 gw 192.168.1.2')
    r3.cmd('route add -net 192.168.2.0/30 gw 192.168.1.2')
    r4.cmd('route add -net 10.0.1.0/24 gw 192.168.1.1')
    r4.cmd('route add -net 10.0.2.0/24 gw 192.168.2.2')
    r5.cmd('route add -net 10.0.1.0/24 gw 192.168.2.1')
    r5.cmd('route add -net 192.168.1.0/30 gw 192.168.2.1')

    # Start xterm for all hosts with specific Python scripts
    makeTerm(h4, title='h4', term='xterm', display=None,
             cmd='python3 PA4_tls_chat_server_Team5.py; bash')
    time.sleep(1)
    makeTerm(h2, title='h2', term='xterm', display=None,
             cmd='python3 PA4_tls_web_server_Team5.py; bash')
    makeTerm(h1, title='h1', term='xterm', display=None,
             cmd='python3 PA4_tls_chat_client_Team5.py; bash')
    makeTerm(h3, title='h3', term='xterm', display=None,
             cmd='python3 PA4_tls_chat_client_Team5.py; bash')

    # Start xterm for Wireshark
    s1.cmd('wireshark &')

    # Start the Mininet command-line interface
    CLI(net)

    # Stop the Mininet network when the CLI is closed
    net.stop()


# Check if the script is being run as the main program
if __name__ == '__main__':
    # Set the log level to 'info'
    setLogLevel('info')

    # Call the 'myNetwork' function to create and configure the network
    myNetwork()
