#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys

from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch,Controller
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.log import lg
from mininet.node import Node
from mininet.topolib import TreeTopo
from mininet.link import Link
from mininet.topo import Topo

class MultiSwitch(OVSSwitch):
    "Custom Switch() subclass that connects to different controllers"
    def start(self, controllers):
        return OVSSwitch.start(self, [cmap[self.name]])

if __name__ == '__main__':
    lg.setLogLevel('info')

    #Add RemoteController
    c0 = RemoteController('c0', ip='127.0.0.1', port = 6633)
    c1 = Controller('c1', port = 6634)
    #c2 = Controller('c2',port=6635)
    cmap = {'s2': c0, 's1': c1}
    #cmap = {'s1':c1 , 's2':c2}
    net = Mininet(switch = MultiSwitch, build = False)
    #net = Mininet(build=False)
    #Add Controller
    net.addController(c1)
    #net.addController(c2)
    #Add hosts and switchs
    firstHost  = net.addHost('h1', ip = '192.168.1.101')
    secondHost = net.addHost('h2', ip = '192.168.1.102')
    thirdHost  = net.addHost('h3', ip = '192.168.1.103')
    leftSwitch  = net.addSwitch('s1')
    rightSwitch = net.addSwitch('s2')

    firstHost.cmd('python -m SimpleHTTPServer 80 &')
    secondHost.cmd('python -m SimpleHTTPServer 80 &')
    thirdHost.cmd('cd ..')
    thirdHost.cmd('python -m SimpleHTTPServer 80 &')

    # Add links
    net.addLink(firstHost,   leftSwitch)
    net.addLink(leftSwitch,  rightSwitch)
    net.addLink(rightSwitch, secondHost)
    net.addLink(rightSwitch, thirdHost)

    net.build()
    net.start()
    #opts = ' '.join( sys.argv[ 1: ] ) if len( sys.argv ) > 1 else ('-D -o UseDNS=no -u0' )
    #sshd( net, opts=opts )
    #net.build()
    #net.start()
    CLI(net)
    net.stop()
