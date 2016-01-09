import boto3
import botocore.exceptions
import re
import termcolor
import requests

import config


class EC2Proxy(object):
    def __init__(self):
        self.ec2 = boto3.resource('ec2', region_name=config.current_region)
        self.ec2_instances = None
        self.proxy_list = []

    @staticmethod
    def get_cidr_ip():

        # Get local WAN ip and convert to CIDR to add add AWS security group
        url = "http://checkip.dyndns.org"
        request = requests.get(url)
        ipv4 = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}", request.text)
        cidr = ipv4[0] + '/32'
        return str(cidr)

    def edit_security(self, arg):

        security_group = self.ec2.SecurityGroup(config.security_group_id)

        try:
            # Prevent public proxy use, authorize only current local ip to connect to proxy
            if arg == 'auth':
                security_group.authorize_ingress(
                        IpProtocol='tcp',
                        FromPort=8888,
                        ToPort=8888,
                        CidrIp=self.get_cidr_ip()
                )

            # Deauthorize local ip from security group
            elif arg == 'deauth':
                security_group.revoke_ingress(
                        IpProtocol='tcp',
                        FromPort=8888,
                        ToPort=8888,
                        CidrIp=self.get_cidr_ip()
                )

        # Just in case ip rule already exists in security group
        except botocore.exceptions.ClientError:
            pass

    def create_instances(self, how_many):

        # Check if any tagged instances are up before creating new proxies
        tag_filter = {'Name': 'tag:Name', 'Values': [config.instance_tag]}
        state_filter = {'Name': 'instance-state-name', 'Values': ['running']}

        current_instances = [
            instance for instance in self.ec2.instances.filter(Filters=[tag_filter, state_filter])
            ]

        if len(current_instances) > 0:

            for instance in current_instances:
                proxy = instance.public_ip_address + ':8888'
                self.proxy_list.append(proxy)

        self.edit_security('auth')

        # If any 'httpsproxy' instances are up, determine how many more to create
        instance_count = how_many - len(self.proxy_list)

        if instance_count > 0:

            self.ec2_instances = self.ec2.create_instances(
                    ImageId=config.image_id,
                    InstanceType=config.instance_type,
                    MinCount=instance_count,
                    MaxCount=instance_count,
                    KeyName=config.key_name,
                    SecurityGroupIds=[config.security_group_id],
                    UserData=config.startup_script
            )

            # Wait for proxies to start up
            print('Waiting for instances to boot, please standby')
            for instance in self.ec2_instances:
                instance.wait_until_running()
                instance.create_tags(Tags=[{'Key': 'Name', 'Value': 'httpsproxy'}])

            ec2_proxies = [(instance.public_ip_address + ':8888') for instance in self.ec2_instances]
            self.proxy_list.extend(ec2_proxies)

    def terminate_instances(self):

        # Deauthorize current local ip from connecting
        self.edit_security('deauth')

        # Terminate all proxy instances
        for instance in self.ec2_instances:
            instance.terminate()


class PublicProxy(object):
    def __init__(self):
        self.proxy_list = []
        self.how_many_to_get = 0

    @staticmethod
    def samair_proxy():

        # Get raw html and parse ip addresses
        url = 'http://www.samair.ru/proxy/'
        headers = {'User-Agent': 'Mozilla/5.0',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
        ip_request = requests.get(url, headers=headers)
        ip_pattern = re.compile(r'class="(\w\w\w\w\w)">(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})')
        proxy_ips = re.findall(ip_pattern, ip_request.text)

        # Ports are masked with css; css file names are dynamic to complicate scraping
        css_pattern = re.compile(r'/styles/(\w\w\w\w\w).css')
        css_file = css_pattern.search(ip_request.text)
        css_location = 'http://www.samair.ru/styles/{}.css'.format(css_file.group(1))
        css_request = requests.get(css_location, headers=headers)
        port_pattern = re.compile(r'.(\w\w\w\w\w):after \{content:"(\d{2,5})"\}')
        ports = re.findall(port_pattern, css_request.text)
        port_index = dict(ports)

        # Build proxy list, in the form of 'ip:port'
        proxies = [(ip + ':' + port_index[css_port]) for css_port, ip in proxy_ips]
        return proxies, url

    def get_proxies(self):

        while len(self.proxy_list) < self.how_many_to_get:
            proxies_to_check, url = self.samair_proxy()
            print 'Checking {} proxies from {}'.format(len(proxies_to_check), url)
            for proxy in proxies_to_check:
                if len(self.proxy_list) == self.how_many_to_get:
                    break
                else:
                    self.proxy_list.extend(self.check_proxy(proxy))

    @staticmethod
    def check_proxy(address):

        proxy_up = []

        proxy_to_check = {
            'http': 'http://' + address,
            'https': 'http://' + address
        }

        try:
            requests.get('https://api.twitter.com/1/', timeout=5, proxies=proxy_to_check)

        except requests.ConnectionError:
            text = termcolor.colored('{}: Down'.format(address), 'red')
            print(text)

        except requests.Timeout:
            text = termcolor.colored('{}: Down'.format(address), 'red')
            print(text)

        except TypeError:
            text = termcolor.colored('{}: Down'.format(address), 'red')
            print(text)

        else:
            text = termcolor.colored('{}: Up'.format(address), 'yellow')
            print(text)
            proxy_up.append(address)

        return proxy_up


ec2proxy = EC2Proxy()
publicproxy = PublicProxy()

