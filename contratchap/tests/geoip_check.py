from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
import os

print('GEOIP_PATH from settings:', settings.GEOIP_PATH)
print('Files in GEOIP_PATH:')
print(os.listdir(settings.GEOIP_PATH))

try:
    g = GeoIP2(settings.GEOIP_PATH)
    print('GeoIP2 initialized')
    ip = '8.8.8.8'
    try:
        country = g.country_name(ip)
        print('country_name for', ip, '=>', country)
        country_code = g.country_code(ip)
        print('country_code =>', country_code)
    except Exception as e:
        print('Error getting country for IP:', e)
except Exception as e:
    print('Error initializing GeoIP2:', e)
