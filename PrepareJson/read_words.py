import json

with open('words.json','r') as f:
    words=json.load(f)

for each in words:
    print each
    print '----hot:',words[each]['hot']
    print '----label:',words[each]['label']
    for pj in words[each]['sim']:
        print '----smi_news:',words[each]['sim'][pj]['title']
    print '============'
