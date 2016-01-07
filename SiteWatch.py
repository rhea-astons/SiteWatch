#!/usr/bin/env python

import sys, os, json, pickle, requests


push_url = 'https://api.pushbullet.com/v2/pushes'
pkl_file = 'data.pkl'


def notify(push_key, message):
  headers = {'Access-Token': push_key, 'Content-Type': 'application/json'}
  data = {'type': 'note', 'title': 'SiteWatch', 'body': message}
  r = requests.post(push_url, headers=headers, data=json.dumps(data))


def is_site_down(url):
  try:
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
      return False
  except:
    pass
  return True


def is_internet_up():
  if is_site_down('http://www.google.com') and is_site_down('http://www.yahoo.com'):
    return False
  return True


def store_data(data):
  out = open(pkl_file, 'wb')
  pickle.dump(data, out)
  out.close()


def load_data():
  data = {}
  if os.path.isfile(pkl_file):
    f = open(pkl_file, 'rb')
    data = pickle.load(f)
    f.close()
  return data


def main(push_key, sites):
  data = load_data()
  if is_internet_up():
    if 'lastFailed' in data and data['lastFailed']:
      notify(push_key, 'Internet was unreachable on last try.')

    for site in sites:
      if is_site_down(site):
        notify(push_key, site + ' is down!')
        data[site] = 'down'
      else:
        data[site] = 'up'
    data['lastFailed'] = False
  else:
    data['lastFailed'] = True
  store_data(data)


if __name__ == '__main__':
  main(sys.argv[1], sys.argv[2:])