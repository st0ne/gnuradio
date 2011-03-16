from xml.dom import minidom

def make_init_c(funclist, dom) :
    tempstring = "";
    tempstring = tempstring + '/*this file is auto generated by volk_register.py*/';

    tempstring = tempstring + '\n\n#include<volk/volk_runtime.h>\n';
    tempstring = tempstring + '#include<volk/volk_cpu.h>\n';
    tempstring = tempstring + '#include<volk_init.h>\n';
    for domarch in dom:
        arch = str(domarch.attributes["name"].value);
        incs = domarch.getElementsByTagName("include");
        for inc in incs:
            my_inc = str(inc.firstChild.data);
            tempstring = tempstring + "#if LV_HAVE_" + arch.swapcase() + "\n";
            tempstring = tempstring + "#include<" + my_inc + ">\n";
            tempstring = tempstring + "#endif\n"
    tempstring = tempstring + '\n\n';

    tempstring = tempstring + "extern struct VOLK_RUNTIME volk_runtime;\n\n";
    tempstring = tempstring + "struct VOLK_RUNTIME* get_volk_runtime(){\n";
    tempstring = tempstring + "    return &volk_runtime;\n";
    tempstring = tempstring + "}\n\n"
    tempstring = tempstring + "    void volk_runtime_init() {\nvolk_cpu_init();\n";

    for func in funclist:
        tempstring = tempstring + "    volk_runtime." + func + " = default_acquire_" + func + ";\n";

    for domarch in dom:
        arch = str(domarch.attributes["name"].value);
        envs = domarch.getElementsByTagName("environment");
        for env in envs:
            cmd = str(env.firstChild.data);
            tempstring = tempstring + "    if(volk_cpu.has_" + arch + "()){\n";
            tempstring = tempstring + "#if LV_HAVE_" + arch.swapcase() + "\n";
            tempstring = tempstring + "        " + cmd + "\n";
            tempstring = tempstring + "#endif\n"     
            tempstring = tempstring + "    }\n";
            
    tempstring = tempstring + "}\n";

    return tempstring