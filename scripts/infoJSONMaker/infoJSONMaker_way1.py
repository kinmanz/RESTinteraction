#!/usr/bin/python
# -*- coding: utf-8 -*-

# Python 2.6.6
"""
Updated: Luchko Serega

Args:
    aduser: login to teamcity
    adpassword: password to teamcity
    buildid: build id
Example for run:
    python scripts/infoJSONMaker/infoJSONMaker_way1.py --aduser Sergey.Luchko --adpassword myPassword --buildid 511736
to get build id use %teamcity.build.id% in Command Line Runner in TeamCity
    python scripts/infoJSONMaker/infoJSONMaker_way1.py --aduser Your.Login --adpassword Your.Password --buildid %teamcity.build.id%

To set up script just change OUT_DIR on which you want. It directory where file will be placed.
"""

import argparse, json, re, xml.etree.ElementTree as Et
from io import open
from infoJSONMaker_way1_helper import tc_get_build_info, tc_get_vcs_info, filter_by_tag

# path where file will placed, don't forget about end slash
OUT_DIR = u'User_Part/'


def write_to_json_file(ad_user, ad_password, build_id):
    print "Get build info..."

    xml_tree_build = Et.fromstring(tc_get_build_info(ad_user, ad_password, build_id))
    xml_tree_build_vcs = Et.fromstring(
        tc_get_vcs_info(ad_user, ad_password, xml_tree_build.find("revisions/revision/vcs-root-instance").attrib["id"]))

    # SET attributes
    print "Setting attributes..."
    GROUP, PRODUCT_NAME, VERSION = [s.strip() for s in
                                    xml_tree_build.find("buildType").attrib["projectName"].split("::")]
    APPLICATION_ID = filter_by_tag(xml_tree_build.findall("properties/property"), "name", "ps_application_id")
    GIT_HASH = xml_tree_build.find("revisions/revision").attrib['version']
    GIT_BRANCH = re.sub('refs/heads/', '',
                        filter_by_tag(xml_tree_build_vcs.findall("properties/property"), "name", "branch"))
    BUILD_NUMBER = xml_tree_build.find(".").attrib['number']
    BUILD_URL = xml_tree_build.find(".").attrib['webUrl']
    DATE = xml_tree_build.find("lastChanges/change").attrib['date']
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
    path_to_file = OUT_DIR + u'{0}.{1}.info.json'.format(GROUP, PRODUCT_NAME)
    dump = json.dumps(dict_to_json, ensure_ascii=False, indent=2, sort_keys=True)
    with open(path_to_file, 'w', encoding='UTF-8') as f:
        f.write(u'{0}'.format(dump))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Starting builder')
    parser.add_argument('--aduser', action="store", dest='ad_user', default=True, help="Login of TeamCity user")
    parser.add_argument('--adpassword', action="store", dest='ad_password', default=True,
                        help="Password of TeamCity user")
    parser.add_argument('--buildid', action="store", dest='buildid', default=True, help="Build configuration ID")
    args = parser.parse_args()

    write_to_json_file(args.ad_user, args.ad_password, args.buildid)
    print "Done."
