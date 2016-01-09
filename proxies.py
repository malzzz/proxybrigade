import argparse

from proxybrigade import proxymanager


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--ec2',
                        action='store',
                        dest='ec2_num',
                        type=int,
                        default=0,
                        help='instantiate ec2 proxies')
    parser.add_argument('--public',
                        action='store',
                        dest='pub_num',
                        type=int,
                        default=0,
                        help='get public proxies')
    args = parser.parse_args()

    if args.pub_num > 0:
        print 'Getting {} Public Proxies'.format(args.pub_num)

        proxymanager.publicproxy.how_many_to_get = args.pub_num
        proxymanager.publicproxy.get_proxies()
        if len(proxymanager.publicproxy.proxy_list) > 0:
            print 'Public Proxies: ',
            for proxy in proxymanager.publicproxy.proxy_list:
                print proxy
                print '                ',
        else:
            print 'Public Proxies: None are up'

    if args.ec2_num > 0:
        print 'Instantiating {} AWS EC2 Proxy Servers'.format(args.ec2_num)

        proxymanager.ec2proxy.create_instances(args.ec2_num)

        print 'EC2 Proxies: ',
        for proxy in proxymanager.ec2proxy.proxy_list:
            print proxy
            print '             ',


if __name__ == '__main__':
    main()
