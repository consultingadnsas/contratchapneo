import requests

BASE = 'http://127.0.0.1:8000'

s = requests.Session()
# 1. GET to obtain session and csrftoken cookie
r = s.get(f'{BASE}/stats/visit/')
print('GET status', r.status_code, 'cookies:', s.cookies.get_dict())

# 2. POST first time
headers = {'X-CSRFToken': s.cookies.get('csrftoken', '')}
r = s.post(f'{BASE}/stats/visit/', headers=headers)
print('POST1 status', r.status_code, r.json())

# 3. POST second time (same session)
headers = {'X-CSRFToken': s.cookies.get('csrftoken', '')}
r = s.post(f'{BASE}/stats/visit/', headers=headers)
print('POST2 status', r.status_code, r.json())

# 4. GET stats again
r = s.get(f'{BASE}/stats/visit/')
print('GET2 status', r.status_code, r.json())
