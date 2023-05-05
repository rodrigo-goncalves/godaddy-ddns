import network
from time import sleep


def local_deepsleep():
    from machine import deepsleep
    deepsleep(60 * 1000 * 60)


def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('YourSSID', 'W1fiP4ssword')

    while True:
        if wlan.isconnected():
            break

        sleep(2)


def send_telegram_message(message, status=None):
    print(message)
    
    if status:
        message = 'Status code: {}\nMessage: "{}"'.format(status, message)

    url = 'https://api.telegram.org/bot111111:jasdjfha7sdfha7sydf78as8df7a8sd/sendMessage?chat_id=344889734&text='
    res = get('{}{}'.format(url, message))
    res.close()
    print('Telegram message sent successfully!')


try:
    from urequests import get, put
except:
    import upip
    upip.install('micropython-urequests')

    import machine
    machine.reset()

wifi_connect()

#Enter vaules for all variables, Latest API call requries them.
#
domain = "yourdomain.co.uk"            # your domain
type = "A"                                    # Record type A, CNAME, MX, etc.
name = "@"                                # name of record to update.
ttl = 600                                   # Time to Live min value 600
port = 1                                    # Required port, Min value 1
weight = 10                                 # Required weight, Min value 1
key = "uh345iu2h34ui52h34ui5h"             # key for godaddy developer API
secret = "5j2348592u34r238409rjfjksaldjf"       # secret for godaddy developer API

# include config file. Alternatively comment this out and edit above lines.
#. update_gd_dns_cfg.sh

headers = {'Authorization': 'sso-key {}:{}'.format(key, secret)}
request_url = "https://api.godaddy.com/v1/domains/{}/records/{}/{}".format(domain, type, name)

try:
    print('Trying to send request to GoDaddy...')
    result = get(request_url, headers=headers)
    print('Request successfully sent')
except Exception as err:
    result.close()
    send_telegram_message('1 - Caught on exception as "{}"'.format(err))
    local_deepsleep()

if result.status_code >= 300:
    result.close()
    send_telegram_message(result.status_code, '2 - "{}"'.format(err), status_code)
    local_deepsleep()

from ure import search, compile

regex = compile('[0-9][0-9]?[0-9]?\.[0-9][0-9]?[0-9]?\.[0-9][0-9]?[0-9]?\.[0-9][0-9]?[0-9]?')

try:
    current_ip = search(regex, str(result.text)).group(0)
    print('Current IP is {}'.format(current_ip))
except Exception as err:
    result.close()
    message = '3 - Error to parse request return with regex: "{}"'.format(err)
    send_telegram_message(message)
    local_deepsleep()

if not current_ip:
    result.close()
    message = '4 - Regex failed to parse and get current ip: "{}"'.format(err)
    send_telegram_message(message)
    local_deepsleep()

result.close()


try:
    # Get public ip address there are several websites that can do this.
    public_ip_obj = get("http://ipinfo.io/json")
except Exception as err:
    public_ip_obj.close()
    send_telegram_message('5 - Caught on exception as "{}"'.format(err))
    local_deepsleep()

try:
    public_ip = search(regex, public_ip_obj.text).group(0)
    print('Public IP is {}'.format(public_ip))
except Exception as err:
    public_ip_obj.close()
    message = '6 - Error to parse request return with regex: "{}"'.format(err)
    send_telegram_message(message)
    local_deepsleep()

public_ip_obj.close()

if public_ip != current_ip:
    put_headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    put_headers.update(headers)

    put_data = [{'data': public_ip,
                'port': port,
                'priority': 10,
                'protocol': 'string',
                'service': 'string',
                'ttl': ttl,
                'weight': weight},]

    put_url = 'https://api.godaddy.com/v1/domains/{}/records/{}/{}'.format(domain, type, name)

    try:
        result = put(put_url, json=put_data, headers=put_headers)
    except Exception as err:
        result.close()
        send_telegram_message('7 - Caught on exception as "{}"'.format(err))
        local_deepsleep()

    if result.status_code >= 300:
        result.close()
        send_telegram_message(result.status_code, '8 - "{}"'.format(err), status_code)
        local_deepsleep()

    result.close()

    message = 'IP successfully updated'

    send_telegram_message(message)

local_deepsleep()
