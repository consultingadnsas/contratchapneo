import requests

BASE = 'http://127.0.0.1:8000'
IP = '8.8.8.8'  # Google DNS, should map to United States in GeoIP

s = requests.Session()
# 1. GET to obtain session and csrftoken cookie — include X-Forwarded-For so middleware records country
r = s.get(f'{BASE}/stats/visit/', headers={'X-Forwarded-For': IP})
print('GET status', r.status_code, 'cookies:', s.cookies.get_dict())

# 2. POST with X-Forwarded-For header
headers = {
    'X-CSRFToken': s.cookies.get('csrftoken', ''),
    'X-Forwarded-For': IP
}
r = s.post(f'{BASE}/stats/visit/', headers=headers)
print('POST status', r.status_code, r.json())

# 3. GET stats again to see country breakdown
r = s.get(f'{BASE}/stats/visit/')
print('GET2 status', r.status_code, r.json())
