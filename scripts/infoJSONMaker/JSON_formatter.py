#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Updated: Luchko Serega
Args:
    aduser: login to teamcity
    adpassword: password to teamcity
    buildid: build id
Example:
to get build id use %teamcity.build.id% in Command Line Runner in TeamCity
    python scripts/infoJSONMaker/JSON_formatter.py --aduser Your.Login --adpassword Your.Password --buildid %teamcity.build.id%
"""

import  argparse, json, re, xml.etree.ElementTree as Et
from io import open
from helper import tc_get_build_info, filter_by_tag

out_file = 'User_Part/CRM_CMS.OAPI_CMS_BACKEND.info.json'


def write_to_json_file(ad_user, ad_password, build_id):
    print "Get build info..."
    result = tc_get_build_info(ad_user, ad_password, build_id)
    xml_tree_build = Et.fromstring(result)

    # SET attributes
    print "Setting attributes..."
    GROUP = "CMS"
    PRODUCT_NAME = "OAPI"
    APPLICATION_ID = "6150"
    GIT_HASH = xml_tree_build.find("revisions/revision").attrib['version']
    GIT_BRANCH = re.sub('refs/heads/', '', filter_by_tag(xml_tree_build.findall("properties/property"), "name", "project_branch_tag"))
    BUILD_NUMBER = xml_tree_build.find(".").attrib['number']
    BUILD_URL = xml_tree_build.find(".").attrib['webUrl']
    DATE = xml_tree_build.find("lastChanges/change").attrib['date']

    VERSION = filter_by_tag(xml_tree_build.findall("properties/property"), "name", "major_version") + "." + \
              filter_by_tag(xml_tree_build.findall("properties/property"), "name", "patch_version")
    try:
        DETAIL = xml_tree_build.find("comment/text").text
    except AttributeError:
        DETAIL = "null"

    # Make JSON
    dict_to_json = {
        'release': {
            'version': VERSION
        },
        'product': {
            "group": GROUP,
            "name": PRODUCT_NAME,
            "version": VERSION
        },
        "application": {
            "name": PRODUCT_NAME,
            "appl_id": APPLICATION_ID,
            "version": VERSION,
            "date": DATE,
            "detail": DETAIL,
            "vcs": {
                "hash": GIT_HASH,
                "branch": GIT_BRANCH
            },
            "build": {
                "number": BUILD_NUMBER,
                "url": BUILD_URL
            }
        }
    }

    # Make JSON file
    print "Make JSON file..."
    dump = json.dumps(dict_to_json, ensure_ascii=False, indent=2, sort_keys=True)
    with open(out_file, 'w', encoding='UTF-8') as f:
        f.write(u'{0}'.format(dump))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Starting builder')
    parser.add_argument('--aduser', action="store", dest='ad_user', default=True, help="Login of TeamCity user")
    parser.add_argument('--adpassword', action="store", dest='ad_password', default=True, help="Password of TeamCity user")
    parser.add_argument('--buildid', action="store", dest='buildid', default=True, help="Build configuration ID")
    args = parser.parse_args()

    write_to_json_file(args.ad_user, args.ad_password, args.buildid)
    print "Done."
