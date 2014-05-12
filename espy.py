from elasticsearch import Elasticsearch
es = Elasticsearch([
    {'host': 'ops.digiman.us', 'port': '9200'}
])

res = es.get(index="logstash-2014.05.09", doc_type='syslog', id='CRXF7n9cSBaSTkrfMqxhBQ')
print(res['_source'])

res = es.search(index="logstash-2014.05.09", body={"query": {"match_all": {}}})
#print ("%(body)s")