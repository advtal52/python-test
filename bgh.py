import pybgh
import argparse
import time
import json
import textwrap

parser = argparse.ArgumentParser(
        prog='bgh',
        add_help=False,
        usage="%(prog)s -u tu@correo.tld -p 'tu pass' -a [get|set] -m [modo del aire] -f [modo de centilacion] -t [temperatura]"
        )
parser.add_argument("-h", "--help", action="store_true")


reqgroup = parser.add_argument_group('Required')
optgroup = parser.add_argument_group('Optional')

reqgroup.add_argument("-u", "--username",       dest = "username")
reqgroup.add_argument("-p", "--password",       dest = "password")

optgroup.add_argument("-a", "--action",         dest = "action",        default = "get")
optgroup.add_argument("-m", "--mode",           dest = "mode",          default = "auto")
optgroup.add_argument("-f", "--fanmode",        dest = "fanmode",       default = "auto")
optgroup.add_argument("-t", "--temperature",    dest = "temperature",   default = "24")

args = parser.parse_args()


myhelp=(textwrap.dedent('''\
<< Control remoto para BGH solidmation -- compilado en python >>

PIP: https://pypi.org/project/pybgh/
CLASS: https://github.com/mool/pybgh
WHOAMI: @advtal52

-----
AYUDA
-----
Argumentos requeridos:
        -u, --username          [nombre de usuario]
        -p, --password          [contraseña]

Argumentos opcionales:
        -h, --help              Muestra este mensage
        -a, --action            [get|set] (get)
        -m, --mode              [off|cool|heat|dry|fan_only|auto|no_change] (auto)
        -f, --fanmode           [low|mid|high|auto|no_change] (auto)
        -t, --temperature       [Temperatura] (24)
'''))



if args.help is True:
        print(myhelp)
        exit(-1)

if ( args.username is None or args.password is None ):
        print(myhelp)
else:
        print( "Action: {}; Username: {}; Password: {}; Mode: {}; Fanmode: {}; Temperature: {} ".format(
                args.action,
                args.username,
                args.password,
                args.mode,
                args.fanmode,
                args.temperature
                ))

        client = pybgh.BghClient(args.username, args.password)
#       home_all = json.dumps(client.get_homes(), indent=2)
#       print(home_all)

        home_id = client.get_homes()[0]['HomeID']
        device_id = next(iter(client.get_devices(home_id)))

        if ( args.action == "get"  ):
                home_json = json.dumps(client.get_homes()[0], indent=2)
                print('DATOS CUENTA')
                print(home_json)

                print('DATOS AIRE')
                aire_json=json.dumps(client.get_status(home_id, device_id)['data'], indent=2)
                print(aire_json)

        if ( args.action == "set" ):
                client.set_mode(device_id, args.mode, args.temperature, args.fanmode)
                time.sleep(5)
                aire_json=json.dumps(client.get_status(home_id, device_id)['data'], indent=2)
                print(aire_json)
