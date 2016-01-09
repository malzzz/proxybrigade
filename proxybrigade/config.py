#####################
# AWS configuration #
#####################

current_region = 'us-west-2'
all_regions = {
    'north-america': ['us-east-1', 'us-west-1', 'us-west-2'],
    'europe': ['eu-west-1', 'eu-central-1'],
    'asia': ['ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1', 'ap-northeast-2'],
    'south-america': ['sa-east-1']
}

security_group_id = 'sg-d93224bd'
image_id = 'ami-5189a661'
instance_type = 't2.micro'
key_name = 'awsproxy'
instance_tag = 'httpsproxy'

# Install tinyproxy and grab configuration from Dropbox
tinyproxy_conf_url = 'https://www.dropbox.com/s/vudsb80q6hzxc3n/tinyproxy.conf?dl=0'

startup_script = """#!/bin/bash
apt-get install tinyproxy
wget -O /etc/tinyproxy.conf {0}
service tinyproxy restart"""

startup_script = startup_script.format(tinyproxy_conf_url)
