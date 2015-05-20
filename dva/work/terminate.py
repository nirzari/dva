'''
terminate all created instances
'''
import re
from itertools import product
from stage import terminate_instance
from data import record_cloud_config

def main(conf, istream, ostream, cloud, verbose):

    amis = []
    regions = []
    file_data = istream.readlines()
    for line in file_data:
        ami_id = re.search("i-[a-z0-9]{8}", line)
        region = re.search("region: [a-z0-9-]*", line)
        if ami_id:
            amis.append(ami_id.group(0))
        if region:
            regions.append(re.sub("region:\s*", "", region.group(0)))
    amis = list(set(amis))
    regions =  list(set(regions))

    params = {}
    params['cloud'] = cloud
    params['enabled'] = True
    params['hostname'] = None
    params['cloudhwname']=None
    params['platform']=None
    params['version']=None
    params['itype']=None
    params['ami']=None

    print "There will be {0} termination calls".format(len(amis)*len(regions))
    for x in product(regions, amis):
        params['region'] = x[0]
        params['id'] = x[1]
        params['enabled'] = True
        record_cloud_config(params, conf)
	try:
            term_result = terminate_instance(params)
            print term_result >> ostmeam
            print params['id'], params['region'], "was terminated"
        except:
            pass
