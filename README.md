# PyFer

This repository intend of to help you to use [ferret](https://github.com/MontFerret/ferret) from python. We build 
c-library from golang source and write class wrapper.  

# Installation

    pip install pythonferret
    
# Example

You can run embedded fql-script: 

    from pferret import wrapper
    
    compiler = wrapper.Ferret(cdp='')
    
    script = '''
    LET doc = DOCUMENT("https://github.com/topics")
    
    FOR el IN ELEMENTS(doc, ".py-4.border-bottom")
        LIMIT 10
        LET url = ELEMENT(el, "a")
        LET name = ELEMENT(el, ".f3")
        LET description = ELEMENT(el, ".f5")
    
        RETURN {
            name: TRIM(name.innerText),
            description: TRIM(description.innerText),
            url: "https://github.com" + url.attributes.href
        }
    '''.encode('utf-8')
    r = wrapper.StrReader(script)
    res = compiler.execute_json(r)
    print(res)
    res = compiler.execute(r)
    print(res)
