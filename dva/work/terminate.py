'''
terminate all created instances
'''
import re
import sys
import os
from data import record_cloud_config
from stage import terminate_instance
from boto.exception import EC2ResponseError
from dva.cloud.base import PermanentCloudException

ID_PARAMS = {
    'cloud': None,
    'enabled': False,
    'hostname': None,
    'cloudhwname': None,
    'platform':None,
    'version':None,
    'itype':None,
    'ami':None
}

def main(conf, istream, ostream, cloud, no_action, verbose):

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
    print '=' * 72
    print 'Requested instances to terminate: {:>6}'.format(len(unique_id_region_list))
    print '=' * 72
    terminated_instances=0
    not_terminated_instances=[]
    not_found_instances=0
    p = ID_PARAMS.copy()
    p['enabled'] = not no_action
    for id_region in unique_id_region_list:
        instance_id_region = id_region[11:].split('_')
        p['id'] = instance_id_region[0]
        p['region'] = instance_id_region[1]
        p['cloud'] = cloud
        record_cloud_config(p, conf)
        
        try:
            terminate_instance(p)
            print '{0} in {1:>15} region was terminated.'.format(p['id'], p['region'])
            terminated_instances += 1
        except KeyboardInterrupt:
            sys.exit()
        except EC2ResponseError:
            print "The instance {0} in {1} region may not be terminated. Modify its 'disableApiTermination' instance attribute and try again.".format(p['id'], p['region'])
            not_terminated_instances.append((p['id'], p['region']))
        except PermanentCloudException:
            print '{0} in {1:>15} region was NOT FOUND.'.format(p['id'], p['region'])
            not_found_instances += 1
        except Exception as e:
            print 'Unexpected error: {0}'.format(e)
            raise
    print '\nTermination Summary'
    print '=' * 72
    print 'Requested instances to terminate: {:>5}'.format(len(unique_id_region_list))
    print 'Terminated: {:>27}'.format(terminated_instances)
    print 'Not found: {:>28}'.format(not_found_instances)
    print 'Not terminated: {:>23}'.format(len(not_terminated_instances))
    if not_terminated_instances:
        for instance in not_terminated_instances:
            print '{0} in {1:>12} region was NOT TERMINATED.'.format(instance[0], instance[1])
    else:
        print "\nAll found instances were terminated.\n"
    if no_action:
        print "NO ACTION was perfomed because of -n switch!\n" 
