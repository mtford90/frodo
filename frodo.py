import json
import logging
import os
import subprocess

import yaml


logger = logging.getLogger('frodo')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)-15s %(levelname)-7s %(message)s [%(funcName)s (%(filename)s:%(lineno)s)]')
ch.setFormatter(formatter)
logger.addHandler(ch)


class ValidationError(Exception):
    pass


FIELD_EVENT = 'event'
FIELD_TEST = 'test'
EVENT_END_TEST_SUITE = 'end-test-suite'
EVENT_END_TEST = 'end-test'

import configuration



os.chdir('/Users/mtford/Playground/myc/app/Mosayc')
print os.getcwd()
results = {}
for test_name, test in configuration.tests.iteritems():
    env = test.get('env', None)
    print env
    for k, v in env.iteritems():
        env[k] = str(v)
    config = test['config']

    bash_cmd = "/Users/mtford/Scripts/XCTool/build/Products/Release/xctool " \
               "-workspace {workspace} " \
               "-scheme {scheme} " \
               "test -only '{target}:{test_case}' " \
               "-sdk {sdk} -reporter json-stream"
    fmt_bash_cmd = bash_cmd.format(workspace=config['workspace'],
                                   scheme=config['scheme'],
                                   target=test['target'],
                                   test_case=test['test_case'],
                                   sdk=config['sdk'])
    logger.debug('Executing \'%s\'' % fmt_bash_cmd)
    # try:
    process = subprocess.Popen(fmt_bash_cmd, stdout=subprocess.PIPE, env=env, shell=True)
    stdout, stderr = process.communicate()
    return_code = process.returncode
    if not return_code in (0, 1):  # xctool returns 1 as success...?
        print stderr
        exit(return_code)
    parsed_json = []
    err_count = 0
    max_err = 10
    for json_string in stdout.split('\n'):
        try:
            parsed_json.append(json.loads(json_string))
        except ValueError, e:
            logger.warn('Unable to parse \'%s\'', json_string)
            err_count += 1
            if err_count >= max_err:
                logger.error('Too many errors')
    num_success = 0
    num_fail = 0
    for parsed in parsed_json:
        event = parsed.get('event', None)
        if event:
            logger.debug('Event type %s' % event)
            if event == EVENT_END_TEST:
                if parsed.get('succeeded', False):
                    num_success += 1
                else:
                    num_fail += 1

    print '%d succeeded' % num_success
    print '%d failed' % num_fail