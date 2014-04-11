import yaml


FIELD_EVENT = 'event'
FIELD_TEST = 'test'
EVENT_END_TEST_SUITE = 'end-test-suite'
EVENT_END_TEST = 'end-test'


f = open('spec.example.yaml')
data = yaml.safe_load(f)
f.close()

print data