from pferret import wrapper

compiler = wrapper.Ferret(cdp='http://localhost:9222')

with open('example.fql', 'r') as fd:
    fql = fd.read()

params = {
    "take": 10
}
res = compiler.execute_json(fql, params=params)
print(res)
res = compiler.execute(fql, params=params)
print(res)
