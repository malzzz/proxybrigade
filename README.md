# proxybrigade

proxybridage
============
This is a utility for getting proxy servers.  It has functions for getting either private or public proxy servers.  If you need private proxy servers, it can instantiate a specified number of AWS EC2 instances that run tinyproxy.  If public proxy servers are acceptable, it will retrieve a list of proxies and test them sequentially until the specified number is reached.

I made this as part of a larger application, but I thought it worked well as a stand-alone module in the case that someone needs to retrieve/use mutliple proxy servers.

Usage
-----
python proxies.py --ec2 [number of ec2 instances] --public [number of public proxies]

You can also import proxybrigade.proxymanager and use it as a module in your application.

To create AWS proxies: proxymanager.create_instances(how_many_to_create)
To terminate instances: proxymanager.terminate_instances()
List of AWS proxies: proxymanager.ec2proxy.proxy_list

For public proxies:
Specify the number to get: proxymanager.publicproxy.how_many_to_get = n
Get public proxies: proxymanager.publicproxy.get_proxies()
List of (up) public proxies: proxymanager.publicproxy.proxy_list

Assumptions
-----------
You have AWS properly configured and have the necessary credentials to create instances.

Dependencies
------------
boto3 (to access AWS)
pathos (for multiprocessing)
requests
termcolor

To-do
-----
Save the state of AWS EC2 instances so that they can be terminated via the command line
Add more sites for public proxies, currently it only queries one site
Multiprocessing for public proxy checking
Some clean-up since I put this together from another module I wrote fairly quickly.
