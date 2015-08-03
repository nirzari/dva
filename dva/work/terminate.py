'''
terminate all created instances
'''
import re
import sys
from data import record_cloud_config
from stage import terminate_instance

ID_PARAMS = {
    'cloud': None,
    'enabled': True,
    'hostname': None,
    'cloudhwname': None,
    'platform':None,
    'version':None,
    'itype':None,
    'ami':None
}

def main(conf, istream, ostream, cloud, verbose):

    id_region_list = []
    file_data = istream.readlines()
    for line in file_data:
        # If there is a chance that broken validation data.yaml file may contain more than
        # one occurrence of 'id_region' string in a line, 're.search' should be replaced with
        # 're.findall'. All further code should be updated as 're.findall'
        # returns a list, not a _sre.SRE_Match object.

        id_region = re.search("id_region:\ [a-z0-9-_]*", line)
        if id_region:
            id_region_list.append(id_region.group(0))

    id_region_set = set(id_region_list)
    unique_id_region_list=list(id_region_set)
    for id_region in unique_id_region_list:
        instance_id_region = id_region[11:].split('_')
	p = ID_PARAMS.copy()
        p['id'] = instance_id_region[0]
        p['region'] = instance_id_region[1]
        p['cloud'] = cloud
        record_cloud_config(p, conf)
        print p['id'] + " in a region " + p['region'] + " will be terminated."
        try:
            terminate_instance(p)
            print p['id'], p['region'], "was terminated"
        except KeyboardInterrupt:
            sys.exit() 
        except Exception as e:
            print "Unexpected error: {0}".format(e)
            raise
