from pferret import wrapper

compiler = wrapper.Ferret(cdp='')

with open('example.fql', 'r') as fd:
    fql = fd.read().encode('utf-8')

r = wrapper.StrReader(fql)
res = compiler.execute_json(r)
print(res)
res = compiler.execute(r)
print(res)
