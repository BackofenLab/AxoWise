from py2neo import Graph

graph = Graph(password = "helloworld")
cursor = graph.run("MATCH (a:Doc) RETURN a")
while cursor.forward():
    print(cursor.current()["a"]["title"])