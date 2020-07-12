import re
import os
import glob
import shutil
import datetime 


def move_string_in(num,stringx): 
    to_join = [] 
    for i in stringx.split('\n'): 
        i = num * " " + i 
        to_join.append(i) 
    return "\n".join(to_join) 

def bracketed_print(l,number=0): 
    mystr = ""
    if len(l) > 1:
        for i in l[:-1]: 
            mystr = mystr+number*" "+"\""+str(i[0])+"\""+": "+"\""+str(i[1])+"\""+',\n' 
        mystr =  mystr+number*" "+"\""+str(l[-1][0])+"\""+": "+"\""+str(l[-1][1])+"\""+'\n'  
        mystr = (number//2)*" "+"{"+'\n'+mystr+(number//2)*" "+"}"
    if len(l) == 1:
        mystr = (number//2)*" "+"{"+'\n'+"\"" + str(l[0])+"\""+": "+"\""+str(l[0]) + "\"" + (number//2)*" "+"}"
    return mystr

def sqaure_over_bracet_print(name, l, number=0):  
    if name != '':  
        mystr = ""  
        if len(l)>1:  
            for i in l[:-1]:  
                mystr = mystr + bracketed_print(i,2*number) +',\n'  
            mystr = mystr + bracketed_print(l[-1],2*number) +'\n'  
            mystr = '"'+name+'"'+" :"+"["+'\n'+mystr+"]"  
        if len(l)==1:  
            mystr = '"'+name+'"'+" :"+"["+'\n'+mystr+bracketed_print(l[0],2*number)+"\n"+"]"   
    else:  
        mystr = ""  
        if len(l)>1:  
            for i in l[:-1]:  
                mystr = mystr + bracketed_print(i,2*number) +',\n'  
            mystr = mystr + bracketed_print(l[-1],2*number) +'\n'  
            mystr = "["+'\n'+mystr + "]"  
        if len(l)==1:  
            mystr = "["+'\n'+mystr+bracketed_print(l[0],2*number)+"\n"+"]"           
    return mystr  


    


def cat_json_style_writer(stringx): 
    cat = re.search(r"category=\"(.*?)\"", stringx).group(1)
    return '"category"{} "{}"'.format(":",cat)

def shape_shape_type_size_id(stringx): 
    mystring = re.search(r"<entry.*?>\n", stringx).group() 
    shape = re.search(r"shape=\"(.*?)\"", mystring).group(1) 
    shape_type = re.search(r"shape_type=\"(.*?)\"", mystring).group(1) 
    size = re.search(r"size=\"(.*?)\"", mystring).group(1) 
    xml_id = re.search(r"eid=\"(.*?)\"", mystring).group(1) 
    if shape and shape_type and size and xml_id: 
        return [("shape", shape), ("shape_type", shape_type), ("size", size), ("xml_id", xml_id)] 


def lexicalizations_json_style_writer(stringx):
    lex_list = re.findall(r"<lex.*?</lex>", stringx)
    lex_jlist = []
    if lex_list:
        for i in lex_list:
            i_comm = re.search(r"comment=\"(.*?)\"", i)
            i_xmlid = re.search(r"lid=\"(.*?)\"", i)
            i_lex =  re.search(r">(.*?)<", i)
            if i_comm and i_xmlid and i_lex:
                lex_jlist.append([("comment", i_comm.group(1)), ("lex", i_lex.group(1)), ("xml_id", i_xmlid.group(1))])
    return lex_jlist


def modifiedtripleset_json_style_writer(stringx):
    m_list = re.findall(r"<modifiedtripleset>.*?\</modifiedtripleset>", stringx, re.DOTALL)[0]
    m_list_mtriple = re.search(r"<mtriple>(.*?)\</mtriple>", m_list).group(1)
    m_to_jason_list = []
    if m_list_mtriple:
        m_split = m_list_mtriple.split("|")
        if len(m_split)==3:
            m_to_jason_list.append(("object", m_split[0]))
            m_to_jason_list.append(("property", m_split[1]))
            m_to_jason_list.append(("subject", m_split[2]))
    return m_to_jason_list




def originaltripleset_json_style_writer(stringx): 
    o_list = re.findall(r"<originaltripleset>.*?\</originaltripleset>", stringx, re.DOTALL) 
    list_of_ortriples = [] 
    for o in o_list: 
        o_list_otriple = re.search(r"<otriple>(.*?)\</otriple>", o).group(1) 
        o_to_jason_list = [] 
        if o_list_otriple: 
            o_split = o_list_otriple.split("|") 
            if len(o_split)==3: 
                o_to_jason_list.append(("object", o_split[0])) 
                o_to_jason_list.append(("property", o_split[1])) 
                o_to_jason_list.append(("subject", o_split[2])) 
        list_of_ortriples.append(o_to_jason_list) 
    return list_of_ortriples 




def name_over_name_brace_over_square(strangename, name, l, number=0): 
    mystr = "" 
    if len(l)==1: 
        mystr = '"'+strangename+'"'+" :"+"["+'\n'+move_string_in(2, sqaure_over_bracet_print(name, l, number))+"\n"+(number//2)*" "+"]"         
    if len(l)>1: 
        for i in l[:-1]: 
            mystr = mystr+move_string_in(2, bracketed_print(i, number))+",\n" 
        mystr = mystr+move_string_in(2, bracketed_print(l[-1], number)) 
        mystr = '"'+strangename+'"'+" :{"+'\n' + move_string_in(2, name+ " :["+'\n' + mystr  +"\n"+ (number//2)*" "+"]\n")+"}" 
    return mystr


def many_name_over_name_brace_over_square(strangename, name, l, number=0): 
    mystr = "" 
    if len(l)==1: 
        return name_over_name_brace_over_square(strangename, name, l, number=0) 
    else: 
        for i in l[:-1]: 
            mystr = mystr + sqaure_over_bracet_print('',i,number)+',\n' 
        mystr = mystr + sqaure_over_bracet_print('',l[-1],number) 
    return '"'+strangename+'"'+" :"+"[" + '\n' + move_string_in(2, '"'+name+'"'+" :"+ mystr) + "\n" + "]" 


     
def entry_to_jason(e):  
    mystring = ''  
    mystring = mystring + cat_json_style_writer(e)+',\n'  
    list_of_lexicalizations = lexicalizations_json_style_writer(e)  
    mystring=mystring + sqaure_over_bracet_print("lexicalizations", list_of_lexicalizations) + ",\n" 
    list_of_modifiedtripleset = [modifiedtripleset_json_style_writer(e)] 
    mystring= mystring + sqaure_over_bracet_print("modifiedtripleset", list_of_modifiedtripleset) + ",\n" 
    mystring= mystring + name_over_name_brace_over_square("originaltriplesets", "originaltripleset", originaltripleset_json_style_writer(e))+',\n'   
    for i in shape_shape_type_size_id(e)[:-1]:  
        mystring=mystring+"\""+i[0]+"\""+": "+"\""+i[1]+"\""+',' + '\n'   
    mystring=mystring+"\""+shape_shape_type_size_id(e)[-1][0]+"\""+": "+"\""+shape_shape_type_size_id(e)[-1][1]+"\""+'\n'  
    return mystring  


def to_jason(file):
    with open(file, 'r') as testxml: 
        input_text = testxml.read()      

    entry_listing = re.findall("<entry.*?entry>", input_text, re.DOTALL)

    with open("{}json".format(file[:-3]), 'w') as tow1:
        if len(entry_listing) == 1: 
             for e in entry_listing: 
                 tow1.write("{\n") 
                 tow1.write(move_string_in(3, "%s: {" % str(1+entry_listing.index(e)) +"\n" )) 
                 tow1.write(move_string_in(3,entry_to_jason(e))) 
                 tow1.write(move_string_in(3, "}")+"\n")  
                 tow1.write("}") 
        else: 
            for e in entry_listing[:-1]: 
                tow1.write("{\n")  
                tow1.write(move_string_in(3, "%s: {" % str(1+entry_listing.index(e)) +"\n" )) 
                tow1.write(move_string_in(3, entry_to_jason(e))) 
                tow1.write(move_string_in(3, "}")+"\n") 
                tow1.write("},\n")  
            tow1.write("{\n")  
            tow1.write(move_string_in(3, "%s: {" % str(1+entry_listing.index(entry_listing[-1]))) +"\n" ) 
            tow1.write(move_string_in(3,entry_to_jason(entry_listing[-1]))) 
            tow1.write(move_string_in(3,"}")+"\n") 
            tow1.write("}") 

            
if __name__ == '__main__':
    curdir = os.getcwd()    
    now_time = datetime.datetime.now()   
    now_time_str = "-".join(str(now_time).split(" ")).replace(":", "-").replace(".","")     
    target_dir = curdir + '/'+'json-data'+now_time_str  
    os.mkdir(target_dir)    
    for root, dirs, files in os.walk("."): 
        for f in files:
            if os.path.splitext(f)[1] == ".xml" and 'json-data' not in str(os.path.join(root, f)):
                shutil.copy(os.path.join(root, f), target_dir+'/'+str(f))
                
    for xfile in glob.glob('{}/*xml'.format(target_dir)):
        try:
            to_jason(xfile)
        except:
            print("File {} seems to be problematic".format(xfile))
            prfname = xfile[:-3]+"json"
            if not os.path.exists('prob_folder'):
                os.makedirs('prob_folder')
            shutil.move(os.path.abspath(prfname), 'prob_folder')
        else:
            print("doing well on {}".format(xfile))
        
