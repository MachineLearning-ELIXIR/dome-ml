####################################################################################################################################
# Reads the DOME specification YAML file located at /data/*.yaml 
# The specification file DOME.yaml and REQUIREMENTS.yaml defining the DOME recommendations  and minimal requirements
# will evolve over time. 

# Input: DOME specitication in YAML format. 
#
# Output 1: a set of questions that can be opened in a spreadsheet (Excel .xlsx file). 
# The spreadsheet can be used by machine learning designers to generate 
# a template methods section that incorporates the elements of 
# the DOME specification.
# The .xlsx file is generated depending on the contents of DOME.yaml
#
# Output 2: a second workbook in the spreadsheet listing minimal requirements for supervised machine learning in biology. 
#
# Important: The DOME version number will be supplied at the top of the excel sheet. 
#
# Authors: Ian Walsh, Dmytro Fishman, Dario Garcia-Gasulla, Tiina Titma, 
# Gianluca Pollastri, The ELIXIR Machine Learning focus group, 
# Jennifer Harrow, Fotis E. Psomopoulos, Silvio C.E. Tosatto
# Date: 11/12/2020
####################################################################################################################################
import yaml
import xlsxwriter
from random import randint
import seaborn as sns
import matplotlib
                
# to search through each node of the YAML specification
def dfs(visited, graph, node, depth, path=[], colorcode=[]):
    if node not in visited:
        print (node)
        print ("depth", depth)
        
        if node not in path:
                path.append(node)
                colorcode.append(depth)

        visited.add(node)
        depth+=1
        if graph.get(node)!=None:
                for neighbour in graph[node]:
                        dfs(visited, graph, neighbour, depth)
        else:
                depth-=1

        return path,colorcode



tags = ["Data", "Optimization", "Model", "Evaluation"]
workbook = xlsxwriter.Workbook('/results/DOME.xlsx')
# rows to spreadsheet with different colors
colors = sns.color_palette("pastel")
        

with open('/data/DOME.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        print(data)

        worksheet = workbook.add_worksheet("DOME methods questions")

        ############ TITLE ROW ############
        version = data['DOME_version']
        title = "The following questions are part of DOME version " + str(version) + " and should be answered to formulate a methods section for a supervised machine learning paper in biology"
        worksheet.set_column('A:O', 12)
        merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow'})
        merge_format2 = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'red'})
        merge_format.set_text_wrap()
        worksheet.merge_range('A1:B1', "DOME version " + str(version), merge_format2)
        worksheet.merge_range('C1:O1', title, merge_format)
        ###################################
        

        

        ###################### PARSE THE DOME METHODS YAML ######################
        start_depth = 0
        # Depth first search of YAML JSON tree
        # this is a gneral way to parse the YAML JSON tree structure 
        # i.e. depth of specification might grow and therefore this function can handle it
        
        row = 1
        for t in tags: 
                visited = set()
                path , colorcode = dfs(visited, data, t, 0)
                if (t in data["Notes"]):
                        path[0] = path[0] + " (" + data["Notes"][t] + ")"
                            
                print(",".join(path))
                print(colorcode)
                
                ###################### WRITE TO SPREADSHEET ######################
                for i in range(len(colorcode)):
                        print (colors[colorcode[i]])
                        c =  matplotlib.colors.to_hex(colors[colorcode[i]])
                        print (c)
                        color_format = workbook.add_format({'bg_color': c})
                        worksheet.set_row(row, cell_format=color_format)
                        indent = ""
                        for j in range(colorcode[i]):
                                indent += "-"
                        indent += " "
                        print(indent + path[i])
                        worksheet.write(row, 0, indent + path[i])
                        row+=1

                path.clear()
                colorcode.clear()

        
        
################ here read the REQUIREMENTS section of the DOME.yaml and create a requirements spreadsheet workbook ###########
with open('/data/REQUIREMENTS.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        print(data)


        worksheet_req = workbook.add_worksheet("Minimal requirements")

        ############ TITLE ROW ############
        version = data['DOME_version']
        title = "The following minimal requirements are part of DOME version " + str(version)
        worksheet_req.set_column('A:O', 12)
        merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow'})
        merge_format2 = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'red'})
        merge_format.set_text_wrap()
        worksheet_req.merge_range('A1:B1', "DOME version " + str(version), merge_format2)
        worksheet_req.merge_range('C1:O1', title, merge_format)
        ###################################
        

        

        ###################### PARSE THE REQUIREMENTS YAML ######################
        start_depth = 0
        # Depth first search of YAML JSON tree
        # this is a gneral way to parse the YAML JSON tree structure 
        # i.e. depth of specification might grow and therefore this function can handle it
        
        row = 1
        for t in tags: 
                visited = set()
                path , colorcode = dfs(visited, data, t, 0)
                if (t in data["Notes"]):
                        path[0] = path[0] + " (" + data["Notes"][t] + ")"
                            
                print(",".join(path))
                print(colorcode)
                
                ###################### WRITE TO SPREADSHEET ######################
                for i in range(len(colorcode)):
                        print (colors[colorcode[i]])
                        c =  matplotlib.colors.to_hex(colors[colorcode[i]])
                        print (c)
                        color_format = workbook.add_format({'bg_color': c})
                        worksheet_req.set_row(row, cell_format=color_format)
                        indent = ""
                        for j in range(colorcode[i]):
                                indent += "-"
                        indent += " "
                        print(indent + path[i])
                        worksheet_req.write(row, 0, indent + path[i])
                        row+=1

                path.clear()
                colorcode.clear()

workbook.close()
