import re


skeleton = '''// public ACTWeapon GetWeapon(int weaponID) {{ }} // RVA: 0xFD98EC Offset: 0xFD98EC

var offset = 0xFD98EC;
var {0} = il2cpp.add(offset);

Interceptor.attach(ACTWeapon,
{{
    onEnter: function(args)
    {{
        console.log("[+] ACTWeapon Hook onEnter()");
        console.log("    args[0] : " + args[0]);
        
    
    }},
    onLeave: function(retVal)
    {{
        console.log("");
    }}
    
}});'''



def extract_methods_from_cs2(filename='dump.cs'):
    r = re.compile(r'(\/\/ RVA:.+Offset:\s(.+)\sVA.+\s\s)(public.+\s((\w+)\(.*\)).+)')
    methods = dict() # methods e.g.,) key : public void Reset() { } // RVA: 0x210DE98 Offset: 0x210DE98,  value :{'func': 'Reset()', 'func_name': 'Reset', 'offset': '0x210DE98'}
    with open('dump.cs', 'r') as f:

        lines = f.read()
        m = r.findall(lines)
        for i in m:
            entire = (i[2] + ' ' + i[0]).replace('\n','')
            func = i[3]
            func_name = i[-1]
            offset = i[1]

            methods.update({entire: {'func': func, 'func_name': func_name, 'offset': offset}})

    return methods.copy()


def extract_methods_from_cs(filename='dump.cs'):
    r = re.compile(r'public.+\s((\w+)\(.*\)).+Offset:\s(.+)')
    methods = dict() # methods e.g.,) key : public void Reset() { } // RVA: 0x210DE98 Offset: 0x210DE98,  value :{'func': 'Reset()', 'func_name': 'Reset', 'offset': '0x210DE98'}
    with open('dump.cs', 'r') as f:
        while True:
            line = f.readline()

            if not line:
                break;
            m = r.search(line)
            if m:
                func = m.groups()[0]
                func_name = m.groups()[1]
                offset = m.groups()[2]
                methods.update({m.group(): {'func': func, 'func_name': func_name, 'offset': offset}}) # function name will be replaced to function parameter. there is no need to exit function name for now.


    return methods.copy()

# Press the green button in the gutter to run the script.

def dump_jscode(methods, keyword=None):

    # {0} = entire function with offset, {1} name of function, {2} offset
    skeleton = '''// {0}

    var offset = {2};
    var {1} = il2cpp.add(offset);

    Interceptor.attach({1},
    {{
        onEnter: function(args)
        {{
            console.log("[+] {1} Hook onEnter() {2}");
            console.log("    args[0] : " + args[0]);


        }},
        onLeave: function(retVal)
        {{
            console.log("[+] {1} Hook onLeave() {2}");
            console.log("    retval : " + retVal);
            console.log("    int retval : " + retVal.toInt32());
        }}

    }});'''
    if not keyword:
        with open('jscode.js', 'w') as wf:
            for method, values in methods.items():
                wf.write(skeleton.format(method, values['func_name'], values['offset']) + '\n')
    else:
        with open('jscode_with_keyword_{0}.js'.format(keyword), 'w') as wf:
            for method, values in methods.items():
                if keyword in method.lower():
                    wf.write(skeleton.format(method, values['func_name'], values['offset']) + '\n')


if __name__ == '__main__':
    # TODO merge extract methods func into one
    methods = extract_methods_from_cs2()
    dump_jscode(methods, keyword='drop')


    # extract_format_values(methods)
    with open('methods.cs', 'w') as wf:
        for method in methods:
            wf.write(method+'\n')






# See PyCharm help at https://www.jetbrains.com/help/pycharm/
