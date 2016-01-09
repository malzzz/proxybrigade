# proxybrigade

Description
-----------
This is a utility for getting proxy servers.  It has functions for getting either private or public proxy servers.  If you need private proxy servers, it can instantiate a specified number of AWS EC2 instances that run tinyproxy.  If public proxy servers are acceptable, it will retrieve a list of proxies and test them sequentially until the specified number is reached.

I made this as part of a larger application, but I thought it worked well as a stand-alone module in the case that someone needs to retrieve/use mutliple proxy servers.

Usage
-----
`$ python proxies.py --ec2 [number of ec2 instances] --public [number of public proxies]`

As a module:
```
import proxybrigade.proxymanager as proxymanager

# Create AWS EC2 proxies
proxymanager.create_instances(how_many_to_create)

# List of proxies
my_ec2_proxy_list = proxymanager.ec2proxy.proxy_list

# Terminate EC2 instances
proxymanager.terminate_instances()

# Specify the (n)umber of public proxies desired
proxymanager.publicproxy.how_many_to_get = n

# Get and test the proxies 
proxymanager.publicproxy.get_proxies()

# List of (up) public proxies 
my_public_proxy_list = proxymanager.publicproxy.proxy_list
```

Assumptions
-----------
You have AWS properly configured and have the necessary credentials to create instances.

Dependencies
------------
* boto3 (to access AWS)
* pathos (for multiprocessing)
* requests
* termcolor

To-do
-----
1.  Save the state of AWS EC2 instances so that they can be terminated via the command line.
2.  Add more sites for public proxies, currently it only queries one site.
3.  Multiprocessing for public proxy checking.
4.  Some clean-up since I put this together from another module I wrote fairly quickly.
