# -*- coding: utf-8 -*-

import urllib2
import base64

# TeamCity
# Based on https://confluence.jetbrains.com/display/TCD9/Build+Script+Interaction+with+TeamCity

TEAMCITY_HOST = "teamcity.billing.ru"
_quote = {"'": "|'", "|": "||", "\n": "|n", "\r": "|r", '[': '|[', ']': '|]'}

def tc_get_build_info(ad_user, ad_password, build_conf_id):
    login = ad_user
    password = ad_password
    build_id = build_conf_id
    auth_string = base64.encodestring('%s:%s' % (login, password)).replace('\n', '')
    req = urllib2.Request(url="https://{host}{uri}/id:{build_id}".format(host=TEAMCITY_HOST,
                                                                         uri="/httpAuth/app/rest/builds",
                                                                         build_id=build_id),
                          headers={'Content-Type': 'application/xml',
                                   'Authorization': "Basic %s" % auth_string})
    response = urllib2.urlopen(req)
    result = response.read()
    return result


# filter list of elements by tag
def filter_by_tag(listOfElements, tag, key):
    for el in listOfElements:
        if el.attrib.get(tag) == key:
            return el.get("value")
    raise AttributeError("No such elements")