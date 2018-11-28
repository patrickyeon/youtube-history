#!/usr/bin/python

import argparse
import cookielib
import datetime
import re
import requests
import time

id_exp = 'href="\s*/watch\?v=([0-9A-Za-z_-]{11})'
more_exp = 'data-uix-load-more-href="/?(?P<more>[^"]+)"'

class mincookie(object):
    # ugly and I don't care
    def __init__(self, name, value):
        self.domain = '.youtube.com'
        self.path = '/'
        self.secure = False
        self.expires = int(time.time()) + 7*24*60*60
        self.is_expired = lambda t: False
        self.port = None
        self.version = 0
        self.name = name
        self.value = value
        self.discard = False

def extract(response):
    try:
        data = response.json()
        ids = re.findall(id_exp, data['content_html'])
        mobj = re.search(more_exp, data['load_more_widget_html'])
    except ValueError:
        ids = re.findall(id_exp, response.text)
        mobj = re.search(more_exp, response.text)
    if mobj is not None:
        mobj = 'https://youtube.com/{}'.format(mobj.group('more'))
    ids_even = [ids[i] for i in range(0, len(ids), 2)]
    ids_odd = [ids[i] for i in range(1, len(ids), 2)]
    # As of 2018-11-27, each video id is listed twice. Bail out if that changes
    assert ids_even == ids_odd
    return ids_even, mobj

def find_overlap(haystack, needle):
    for i in range(len(haystack) - len(needle) + 1):
         if haystack[i : i + len(needle)] == needle:
            return i
    return -1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--cookie-jar',
                        help='cookie file (Netscape format cookies.txt')
    parser.add_argument('-c', '--cookies',
                        help='cookies ("key1=val1; key2=val2")')
    parser.add_argument('--max', type=int, help='maximum count to list')
    parser.add_argument('--since',
                        help='comma-delimited list of ids, stop when reached')
    args = parser.parse_args()

    if args.cookie_jar:
        cookies = cookielib.MozillaCookieJar(args.cookie_jar)
        try:
            cookies.load()
        except IOError:
            # if it doesn't exist, that's ok. probably just want to write to it
            pass
    else:
        cookies = cookielib.CookieJar()

    if args.cookies:
        for kv in args.cookies.split('; '):
            k,v = kv.split('=', 1)
            cookies.set_cookie(mincookie(k, v))

    ids = []
    url = 'https://youtube.com/feed/history'
    sess = requests.Session()
    while (args.max < 0 or len(ids) < args.max) and url is not None:
        resp = sess.get(url, cookies=cookies)
        resp.raise_for_status()
        newids, url = extract(resp)
        ids.extend(newids)
        if args.since:
            idx = find_overlap(ids, args.since.split(','))
            if idx >= 0:
                ids = ids[:idx]
                break

    # put everything in reverse-chronological order
    ids.reverse()
    print '# {}'.format(datetime.datetime.now())
    print '# Adding {} video IDs'.format(len(ids))
    print '\n'.join(ids)

    if args.cookie_jar:
        cookies.save()
