import json

parsed = []
with open('../test/unit/data/one_failed_example.json', 'r') as f:
    for line in f:
        parsed += [json.loads(line)]

unique = list(set([x['event'] for x in parsed]))
print len(unique)
print unique

print [x for x in parsed if x['event'] == 'end-test']
print [x for x in parsed if x['event'] == 'end-test-suite']
print [x for x in parsed if x['event'] == 'begin-test']