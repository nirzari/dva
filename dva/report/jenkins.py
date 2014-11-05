'''
tool for uploading data to Jenkins
'''
import sys
import time
import logging
import tempfile
import json
import requests
import time
import urllib3
import xml.etree.ElementTree as ET
from ..tools.retrying import retrying, EAgain
from ..work.data import load_yaml, save_result
from ..work.common import RESULT_PASSED

logger = logging.getLogger(__name__)

def main(config, f, job, hashtag, desc, login="jenkins", passwd="jenkins"):
#    with open(istream, "rb") as f:
    file_data = f.read()
    params = {"parameter": [{'name':'report.xml', 'file': 'file0'},{"name": "desc", "value": hashtag}]}
    data, content_type = urllib3.encode_multipart_formdata([
        ("file0", (f.name, file_data)),
        ("json", json.dumps(params)),
        ("Submit", "Build"),
        ])
    url = job + 'build'
    r = requests.post(url, auth=(login, passwd), data=data, headers={"content-type": content_type})
    print "Waiting 10s for build to be finished."
    time.sleep(10)
    url = job + 'api/xml'
    xpath_str = "//build//*[contains(text(),'"+ hashtag +"')]/../../../url"
    params = {'depth': '1', 'xpath': xpath_str, 'wrapper': 'list'}
    r = requests.get(url, auth=(login, passwd), params=params)
    
    tree = ET.fromstring(r.text.replace('</url>','</url>\n'))
    notags = ET.tostring(tree, encoding='utf8', method='text')
    job_number = notags.splitlines()[0].rsplit('/',2)[1]

    url = job + 'default/' + job_number + '/testReport/submitDescription'
    params = {'description': desc}
    r = requests.get(url, auth=(login,passwd), params=params)

    print "Return code: " + str(r.status_code)
