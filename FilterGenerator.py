import sys

def FilterGenerator(Labels):
    xmlstruct = """<?xml version='1.0' encoding='UTF-8'?>
    <feed xmlns='http://www.w3.org/2005/Atom' xmlns:apps='http://schemas.google.com/apps/2006'>
    	<title>Mail Filters</title>
            %s
    </feed>"""

    filters = ""
    for Label in Labels:
        filters += """
        	<entry>
        		<category term='filter'></category>
        		<title>Mail Filter</title>
        		<apps:property name='to' value='%s'/>
        		<apps:property name='label' value='%s'/>
        		<apps:property name='shouldArchive' value='true'/>
        		<apps:property name='sizeOperator' value='s_sl'/>
        		<apps:property name='sizeUnit' value='s_smb'/>
        	</entry>
        """%(Label,Label)
    with open('Filters.xml', 'w') as file_:
        file_.write(xmlstruct%filters)



if __name__ == '__main__':
    if (len(sys.argv) < 2 ):
        print("for spesific Labels add the labels after the op, for now you get default A B C D labels")
        FilterGenerator(['A','B','C','D'])
    else:
        FilterGenerator(sys.argv[1:])
