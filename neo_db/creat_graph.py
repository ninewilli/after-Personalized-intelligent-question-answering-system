from py2neo import Graph, Node, Relationship,NodeMatcher
from neo_db.config import graph
#graph.run("MATCH (n) OPTIONAL MATCH(n)-[r]-()DELETE n,r")

with open("raw_data/relation.txt",encoding='utf-8') as f:
    for line in f.readlines():
        rela_array=line.strip("\n").split(",")
        graph.run("MERGE(p: Person{cate:'%s',Name: '%s'})"%(rela_array[3],rela_array[0]))
        graph.run("MERGE(p: Person{cate:'%s',Name: '%s'})" % (rela_array[4], rela_array[1]))
        graph.run(
            "MATCH(e: Person), (cc: Person) \
            WHERE e.Name='%s' AND cc.Name='%s'\
            CREATE(e)-[r:%s{relation: '%s'}]->(cc)\
            RETURN r" % (rela_array[0], rela_array[1], rela_array[2],rela_array[2])
        )
        
