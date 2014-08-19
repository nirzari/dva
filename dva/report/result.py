""" Result parsing functions """
import textwrap
import aggregate
from ..work.common import RESULT_PASSED, RESULT_FAILED, RESULT_ERROR

COMMON_COMMAND_KEYS_ORDERED=('command', 'match', 'result', 'value', 'actual', 'expected', 'comment')

def command_repr(command):
    '''repr a single command as list of lines'''
    ret = []
    format_value = lambda key, value: textwrap.wrap(('%s: ' % key) + str(value), initial_indent='  ',
                        subsequent_indent='  ', break_on_hyphens=False,  break_long_words=True, width=70)
    ret.append('-')
    for key in COMMON_COMMAND_KEYS_ORDERED:
        if key not in command:
            continue
        ret.extend(format_value(key, command[key]))
    for key in set(command) - set(COMMON_COMMAND_KEYS_ORDERED):
        ret.extend(format_value(key, command[key]))
    return ret


def get_test_result(test_data, verbose=False):
    '''get formated test result'''
    ret = test_data['result']
    log = ['%s:%s: %s' % (test_data['stage'], test_data['name'], test_data['result'])]
    if test_data['result'] != RESULT_PASSED or verbose:
         for command in test_data['log']:
            log.extend(command_repr(command))
    return ret, log


def get_stage_result(stage_data, verbose=False):
    '''get formated stage result'''
    ret = stage_data['stage_result']
    log = []
    if ret != RESULT_PASSED or verbose:
        log = ['-']
        txt = '%s: %s\n%s' % (stage_data['stage_name'], stage_data['stage_result'], stage_data['stage_exception'])
        log.extend(textwrap.wrap(txt, break_on_hyphens=False, break_long_words=True, width=70, initial_indent='  ',
                                    subsequent_indent='  '))
    return ret, log

def get_hwp_result(hwp_data, verbose=False):
    '''get overal hwp result'''
    ret = RESULT_PASSED
    log = []
    for hwp in hwp_data:
        hwp_status = RESULT_PASSED
        hwp_index = len(log)
        for res in hwp_data[hwp]:
            if 'test' in res:
                # test case result
                sub_result, sub_log = get_test_result(res['test'], verbose)
            else:
                # stage result
                sub_result, sub_log = get_stage_result(res, verbose)
            if sub_result in [RESULT_ERROR, RESULT_FAILED] and ret == RESULT_PASSED:
                hwp_status = sub_result
            log.extend(sub_log)
        hwp_header = '%s: %s' % (hwp, ret)
        log.insert(hwp_index, '-' * len(hwp_header))
        log.insert(hwp_index, hwp_header)
        log.insert(hwp_index, '')
        if hwp_status != RESULT_PASSED and ret == RESULT_PASSED:
           ret = hwp_status
    return ret, log

def get_overall_result(data, verbose=False):
    """
    Get human-readable representation of the result; partitioned by ami
    returns a tuple of an overal result and list of tuples overal_result, [(ami_resutl, ami_log), ...]
    """
    agg_data = aggregate.apply(data, 'ami', 'cloudhwname')
    ret = RESULT_PASSED
    log = []
    for ami in agg_data:
        ami_log = []
        sub_result, sub_log = get_hwp_result(agg_data[ami], verbose)
        if sub_result != RESULT_PASSED and ret == RESULT_PASSED:
            ret = sub_result
        ami_header = '# %s: %s' % (ami, ret)
        sub_log.insert(0, '-' * len(ami_header))
        sub_log.insert(0, ami_header)
        sub_log.insert(0, '')
        # ami
        log.append((sub_result, '\n'.join(sub_log)))
    return ret, log
