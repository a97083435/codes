import yaml
import socket
import maxminddb
import platform
import os
import requests
import flag
from tqdm import tqdm
from pathlib import Path

Country_mmdb_path = './Country.mmdb'

def push(list, outfile):
    country_count = {}
    count = 1
    clash = {'proxies': [], 'proxy-groups': [
            {'name': 'automatic', 'type': 'url-test', 'proxies': [], 'url': 'https://www.google.com/favicon.ico',
             'interval': 300}, {'name': '🌐 Proxy', 'type': 'select', 'proxies': ['automatic']}],
             'rules': ['MATCH,🌐 Proxy']}
    if int(len(list)) < 1:
        print('\n 没有可用节点 \n')
        return '没有可用节点'
    for i in tqdm(range(int(len(list))), desc="alive Parse"):
        x = list[i]
        clash['proxies'].append(x)
        clash['proxy-groups'][0]['proxies'].append(x['name'])
        clash['proxy-groups'][1]['proxies'].append(x['name'])
    """    
    with maxminddb.open_database(Country_mmdb_path) as countrify:
        for i in tqdm(range(int(len(list))), desc="good Parse"):
            x = list[i]
            try:
                float(x['password'])
            except:
                try:
                    float(x['uuid'])
                except:
                    try:
                        ip = str(socket.gethostbyname(x["server"]))
                    except:
                        ip = str(x["server"])
                    try:
                        country = str(countrify.get(ip)['country']['iso_code'])
                    except:
                        country = 'UN'
                    if country == 'TW' or country == 'MO' or country == 'HK':
                        flagcountry = 'CN'
                    else:
                        flagcountry = country
                    try:
                        country_count[country] = country_count[country] + 1
                        x['name'] = str(flag.flag(flagcountry)) + " " + country + " " + str(count)
                    except:
                        country_count[country] = 1
                        x['name'] = str(flag.flag(flagcountry)) + " " + country + " " + str(count)
                    clash['proxies'].append(x)
                    clash['proxy-groups'][0]['proxies'].append(x['name'])
                    clash['proxy-groups'][1]['proxies'].append(x['name'])
                    count = count + 1
            # except:
            # print(list[i])
            # pass
    """ 
    with open(outfile, 'w') as writer:
        yaml.dump(clash, writer, sort_keys=False)
        writer.close()




def checkenv():
    home = str(Path.home())
    mmdbfl = home + Country_mmdb_path
    operating_system = str(platform.platform())
    if operating_system.startswith('macOS'):
        if 'arm64' in operating_system:
            clashname='./clash-darwinarm64'
        else:
            clashname='./clash-darwinamd64'
    elif operating_system.startswith('Linux'):
        clashname='./clash-linuxamd64'
    elif operating_system.startswith('Windows'):
        clashname='clash-windowsamd64.exe'
    else:
        print('Unsupported Platform')
        exit(1)
    print('Running on '+ operating_system)

    return clashname, operating_system

def filter(config):
    proxies_list = config["proxies"]
    # print(proxies_list)
    ss_supported_ciphers = ['aes-128-gcm', 'aes-192-gcm', 'aes-256-gcm',
                            'aes-128-cfb', 'aes-192-cfb', 'aes-256-cfb', 'aes-128-ctr', 'aes-192-ctr', 'aes-256-ctr',
                            'rc4-md5', 'chacha20-ietf', 'xchacha20', 'chacha20-ietf-poly1305',
                            'xchacha20-ietf-poly1305']
    ssr_supported_obfs = ['plain', 'http_simple', 'http_post', 'random_head', 'tls1.2_ticket_auth',
                          'tls1.2_ticket_fastauth']
    ssr_supported_protocol = ['origin', 'auth_sha1_v4', 'auth_aes128_md5', 'auth_aes128_sha1', 'auth_chain_a',
                              'auth_chain_b']
    vmess_supported_ciphers = ['auto', 'aes-128-gcm', 'chacha20-poly1305', 'none']
    iplist = {}
    passlist = []
    count = 1
    clash = {'proxies': [], 'proxy-groups': [
            {'name': 'automatic', 'type': 'url-test', 'proxies': [], 'url': 'https://www.google.com/favicon.ico',
             'interval': 300}, {'name': '🌐 Proxy', 'type': 'select', 'proxies': ['automatic']}],
             'rules': ['MATCH,🌐 Proxy']}
    # 去重复，重名，空名，int型password
    if True: #开关：True，False
        raw_length = len(proxies_list)
        length = len(proxies_list)
        begin = 0
        rm = 0
        name_none = 0
        while begin < length:
            if (begin + 1) == 1:
                print(f'\n-----去重开始-----\n起始数量{length}')
            elif (begin + 1) % 100 == 0:
                print(f'当前基准{begin + 1}-----当前数量{length}')
            elif (begin + 1) == length and (begin + 1) % 100 != 0:
                repetition = raw_length - length
                print(f'当前基准{begin + 1}-----当前数量{length}\n--------\n重复和int型password数量{repetition}\n重名数量{rm}\n空名数{name_none}\n-----去重完成-----\n')
            if proxies_list[begin]['name'] == None or proxies_list[begin]['name'] == '' or proxies_list[begin]['name'] == ' ':
                proxies_list[begin]['name'] = 'name-None' + '-' + proxies_list[begin]['type'] + '+' +  str(name_none)
                name_none += 1
            begin_2 = begin + 1
            name_same = 0
            while begin_2 <= (length - 1):
                if proxies_list[begin]['server'] == proxies_list[begin_2]['server'] and proxies_list[begin]['port'] == proxies_list[begin_2]['port']:
                    proxies_list.pop(begin_2)
                    length -= 1
                    begin_2 -= 1
                else:
                    if proxies_list[begin]['name'] == proxies_list[begin_2]['name']:
                        name_same += 1
                        proxies_list[begin_2]['name'] = str(proxies_list[begin_2]['name']) + '+' + str(name_same)
                begin_2 += 1
            #if name_same > 0:
                #print(f"{proxies_list[begin]['name']} 重名数量：{name_same}")
            rm += name_same
            
            #删除password为int型数字的节点
            if proxies_list[begin]['type'] == 'ss' or proxies_list[begin]['type'] == 'trojan' or proxies_list[begin]['type'] == 'ssr':
                if isinstance(proxies_list[begin]['password'],int):
                    print(f"{proxies_list[begin]['name']}的password为int类型纯数字！")
                    print(proxies_list[begin])
                    proxies_list.pop(begin)
                    length -= 1
                    begin -= 1
            begin += 1 

    #查找不能用的节点删除		
    for i in tqdm(range(int(len(proxies_list))), desc="Parse"):
        x = proxies_list[i]
        #将port强行int
        x['port'] = int(x['port'])
        if x['type'] == 'ss':
            try:
                if x['cipher'] not in ss_supported_ciphers:
                    continue
            except:
               continue
        elif x['type'] == 'vmess':
            try:
                if 'udp' in x:
                    if x['udp'] not in [False, True]:
                        continue
                if 'tls' in x:
                    if x['tls'] not in [False, True]:
                        continue
                if 'skip-cert-verify' in x:
                    if x['skip-cert-verify'] not in [False, True]:
                        continue
                if x['cipher'] not in vmess_supported_ciphers:
                    continue
            except:
                continue
        elif x['type'] == 'trojan':
            try:
                if 'udp' in x:
                    if x['udp'] not in [False, True]:
                        continue
                if 'skip-cert-verify' in x:
                    if x['skip-cert-verify'] not in [False, True]:
                        continue
            except:
                continue
        elif x['type'] == 'ssr':
            try:
                if x['cipher'] not in ss_supported_ciphers:
                    continue
                if x['obfs'] not in ssr_supported_obfs:
                    continue
                if x['protocol'] not in ssr_supported_protocol:
                    continue
            except:
                continue
        clash['proxies'].append(x)
        clash['proxy-groups'][0]['proxies'].append(x['name'])
        clash['proxy-groups'][1]['proxies'].append(x['name'])
    return clash
    
    """       
    with maxminddb.open_database(Country_mmdb_path) as countrify:
        for i in tqdm(range(int(len(list))), desc="Parse"):
            try:
                x = list[i]
                authentication = ''
                x['port'] = int(x['port'])
                try:
                    ip = str(socket.gethostbyname(x["server"]))
                except:
                    ip = x['server']
                try:
                    country = str(countrify.get(ip)['country']['iso_code'])
                except:
                    country = 'UN'
                if x['type'] == 'ss':
                    try:
                        if x['cipher'] not in ss_supported_ciphers:
                            ss_omit_cipher_unsupported = ss_omit_cipher_unsupported + 1
                            continue
                        if country != 'CN':
                            if ip in iplist:
                                ss_omit_ip_dupe = ss_omit_ip_dupe + 1
                                continue
                            else:
                                iplist[ip] = []
                                iplist[ip].append(x['port'])
                        x['name'] = str(flag.flag(country)) + ' ' + str(country) + ' ' + str(count) + ' ' + 'SSS'
                        authentication = 'password'
                    except:
                        continue
                elif x['type'] == 'ssr':
                    try:
                        if x['cipher'] not in ss_supported_ciphers:
                            continue
                        if x['obfs'] not in ssr_supported_obfs:
                            continue
                        if x['protocol'] not in ssr_supported_protocol:
                            continue
                        if country != 'CN':
                            if ip in iplist:
                                continue
                            else:
                                iplist.append(ip)
                                iplist[ip].append(x['port'])
                        authentication = 'password'
                        x['name'] = str(flag.flag(country)) + ' ' + str(country) + ' ' + str(count) + ' ' + 'SSR'
                    except:
                        continue
                elif x['type'] == 'vmess':
                    try:
                        if 'udp' in x:
                            if x['udp'] not in [False, True]:
                                continue
                        if 'tls' in x:
                            if x['tls'] not in [False, True]:
                                continue
                        if 'skip-cert-verify' in x:
                            if x['skip-cert-verify'] not in [False, True]:
                                continue
                        if x['cipher'] not in vmess_supported_ciphers:
                            continue
                        x['name'] = str(flag.flag(country)) + ' ' + str(country) + ' ' + str(count) + ' ' + 'VMS'
                        authentication = 'uuid'
                    except:
                        continue
                elif x['type'] == 'trojan':
                    try:
                        if 'udp' in x:
                            if x['udp'] not in [False, True]:
                                continue
                        if 'skip-cert-verify' in x:
                            if x['skip-cert-verify'] not in [False, True]:
                                continue
                        x['name'] = str(flag.flag(country)) + ' ' + str(country) + ' ' + str(count) + ' ' + 'TJN'
                        authentication = 'password'
                    except:
                        continue
                elif x['type'] == 'snell':
                    try:
                        if 'udp' in x:
                            if x['udp'] not in [False, True]:
                                continue
                        if 'skip-cert-verify' in x:
                            if x['skip-cert-verify'] not in [False, True]:
                                continue
                        x['name'] = str(flag.flag(country)) + ' ' + str(country) + ' ' + str(count) + ' ' + 'SNL'
                        authentication = 'psk'
                    except:
                        continue
                elif x['type'] == 'http':
                    try:
                        if 'tls' in x:
                            if x['tls'] not in [False, True]:
                                continue
                        x['name'] = str(flag.flag(country)) + ' ' + str(country) + ' ' + str(count) + ' ' + 'HTT'
                        # authentication = 'userpass'
                    except:
                        continue
                elif x['type'] == 'socks5':
                    try:
                        if 'tls' in x:
                            if x['tls'] not in [False, True]:
                                continue
                        if 'udp' in x:
                            if x['udp'] not in [False, True]:
                                continue
                        if 'skip-cert-verify' in x:
                            if x['skip-cert-verify'] not in [False, True]:
                                continue
                        x['name'] = str(flag.flag(country)) + ' ' + str(country) + ' ' + str(count) + ' ' + 'SK5'
                        # authentication = 'userpass'
                    except:
                        continue
                else:
                    print(x)
                    print('unsupported')
                    continue
                if ip in iplist and x['port'] in iplist[ip]:
                    if country != 'CN':
                        continue
                    else:
                        if x[authentication] in passlist:
                            continue
                        else:
                            passlist.append(x[authentication])
                            pass
                else:
                    try:
                        iplist[ip].append(x['port'])
                    except:
                        iplist[ip] = []
                        iplist[ip].append(x['port'])

                clash['proxies'].append(x)
                clash['proxy-groups'][0]['proxies'].append(x['name'])
                clash['proxy-groups'][1]['proxies'].append(x['name'])
                count = count + 1

            except:
                print('shitwentwrong' + str(x))
                continue
    return clash
    """
