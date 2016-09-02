# -*- coding: utf-8 -*-

import urllib2
import base64

# TeamCity
# Based on https://confluence.jetbrains.com/display/TCD9/Build+Script+Interaction+with+TeamCity

TEAMCITY_HOST = "teamcity.billing.ru"
_quote = {"'": "|'", "|": "||", "\n": "|n", "\r": "|r", '[': '|[', ']': '|]'}


def tc_get_info(ad_user, ad_password, id, uri):
    login = ad_user
    password = ad_password
    request_id = id
    auth_string = base64.encodestring('%s:%s' % (login, password)).replace('\n', '')
    req = urllib2.Request(url="https://{host}{uri}/id:{build_id}".format(host=TEAMCITY_HOST,
                                                                         uri="/httpAuth/app/rest/" + uri,
                                                                         build_id=request_id),
                          headers={'Content-Type': 'application/xml',
                                   'Authorization': "Basic %s" % auth_string})
    response = urllib2.urlopen(req)
    result = response.read()
    return result


def tc_get_build_info(ad_user, ad_password, build_conf_id):
    return tc_get_info(ad_user, ad_password, build_conf_id, "builds")


def tc_get_vcs_info(ad_user, ad_password, vcs_conf_id):
    return tc_get_info(ad_user, ad_password, vcs_conf_id, "vcs-root-instances")


# filter list of elements by tag
def filter_by_tag(listOfElements, tag, key):
    for el in listOfElements:
        if el.attrib.get(tag) == key:
            return el.get("value")
    raise AttributeError("No such elements")
