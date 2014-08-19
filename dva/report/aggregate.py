'''
data aggregation tools for report purposes
'''

import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

def aggregation_factory(level=0):
    '''chain defaultdicts to create an aggregate for data'''
    if level == 0:
        return []
    return defaultdict(lambda: aggregation_factory(level=level - 1))

def apply(data, *field_names):
    '''apply aggregation to data based on field names provided'''
    aggregate = aggregation_factory(len(field_names))
    for item in data:
        ptr = aggregate
        for field in field_names:
            ptr = ptr[item[field]]
        ptr.append(item)
    return aggregate

