#!/usr/bin/python3
import os
import re
import tarfile
import subprocess
import gzip

path = os.getcwd()

#Creates an index file website for my links to my projects.
def write_Index_HTML():
    f = open('index.html', 'w')
    hfile = """
<!DOCTYPE html>
<html>
<style>
body {
  font-family: Copperplate, Papyrus, fantasy;
}
</style>
<body>
        <link href="styles.css" rel="stylesheet" />
	    <body style="background-color:lavender;">

	    <h1 style="color:fuchsia;" > Alexis Indick's CSC344 Assignments</h1>
	    
	    <h2  style="color:purple;">Assignment 1</h2>

       
		<a href="/CSC344/a1/summary_main.c.html">Link</a>

		<h2 style="color:purple;">Assignment 2</h2>
        
        
		<a href="/CSC344/a2/summary_main.clj.html">Link</a>


		<h2 style="color:purple;"> Assignment 3</h2>

       
		<a href="/CSC344/a3/summary_main.scala.html">Link</a>



		<h2 style="color:purple;">Assignment 4</h2>

     
		<a href ="/CSC344/a4/summary_main.pl.html">Link</a>




		<h2 style="color:purple;">Assignment 5</h2>

        
		<a href="/CSC344/a5/summary_main.py.html">Link</a>




</body>
</html>

	 """
    f.write(hfile)
    f.close()

#Creates the summary in html of all my projects.
def summary_HTML(Path, assign):
    f = open(Path + '/summary_' + assign.name + '.html', 'w')
    o = subprocess.check_output(['wc', '-l', assign])
    num_Lines = int(re.search(r'\d+', str(o)).group())
    html = """
<!DOCTYPE html>
<html>
<head>
	<title>""" + assign.name + """</title>
	<style>
		body{
			font-family: monospace;
		}
		.Info{
			margin: 20px;
			margin-left: 150px;
			margin-right: 150px;
			padding: 20px;
			border-radius:12px;

		}
	</style>
</head>
<body>
	<h1 align="center">""" + assign.name + """</h1>
	<hr>
	<div class="Info" style="background-color:lavender; color:purple">
		<p>Number of Lines:<i> """ + str(num_Lines) + """</i></p>
		<p><a target="_blank" href='""" + assign.name + """'>Code</a></p>
		<p>Identifiers<br>
"""
    html = html + write_lists(assign)
    html = html + """
	</div>
</body>
</html>
"""
    f.write(html)


def write_lists(currentAssign):
    list_Ids = parse(currentAssign)
    a = " "
    for i in list_Ids:
        a = a + "<li>" + i + "</li>"
    return a


def parse(currentAssign):
    ab = list()
    f = open(currentAssign.path, 'r')
    for line in f:
        line = line.lstrip()
        while line.startswith('//') or line.startswith(';') or line.startswith('#'):
            line = next(f)
            line = line.lstrip()

        if line.startswith('/*'):
            line = next(f)
            line = line.lstrip()
            while not line.endswith('*/\n'):
                line = next(f)
                line = line.lstrip()
            line = next(f)
            line = line.lstrip()

        if line.startswith('%'):
            line = next(f)
            line = line.lstrip()
            while not line.endswith('.\n'):
                line = next(f)
                line = line.lstrip()
            line = next(f)
            line = line.lstrip()

        if line.startswith('"'):
            line = next(f)
            line = line.lstrip()
            while not line.endswith('"\n'):
                line = next(f)
                line = line.lstrip()
            line = next(f)
            line = line.lstrip()

        line = re.sub('(\)+.*(?=))', '', line)
        line = re.sub(r"(\/\/ *.*)|(\/\*(.|\n)*\*\/)",line)
        line = re.findall('(\s*[a-zA-Z]*\s*)', line)

        for word in line:
            word = re.sub('\s+', '', word)
            if not ab.__contains__(word) and word != '':
                ab.append(word)
    ab.sort()
    return ab


def get_assignments():
    assignment_list = [None] * 5
    assignment_path = ' '
    with os.scandir(path + '/..') as i:
        for entry in i:
            if 'a' in entry.name:
                assignment_path = path + '/../' + entry.name
                with os.scandir(path + '/../' + entry.name) as i:
                    for e in i:
                        if e.name.startswith('main', 0, 4):
                            if e.name.endswith('.c'):
                                assignment_list[0] = e
                                summary_HTML(assignment_path, e)
                            if e.name.endswith('.clj'):
                                assignment_list[1] = e
                                summary_HTML(assignment_path, e)
                            if e.name.endswith('.scala'):
                                assignment_list[2] = e
                                summary_HTML(assignment_path, e)
                            if e.name.endswith('.pl'):
                                assignment_list[3] = e
                                summary_HTML(assignment_path, e)
                            if e.name.endswith('.py'):
                                assignment_list[4] = e
                                summary_HTML(assignment_path, e)
    return assignment_list

#This is the code for making the tar file
def get_tar():
    t = tarfile.open('Assignments' + ".tar.gz", 'w|')
    with os.scandir(path + '/..') as i:
        for direct in i:

            if direct.name.startswith('a'):
                with os.scandir(direct) as d:
                    for f in d:
                        if f.name.startswith('main', 0, 4) or f.name.endswith('.html'):
                            t.add(f.path, direct.name + '/' + f.name)
        t.close()

#The call to the functions and subprocess is used to create new processes.
write_Index_HTML()
get_assignments()
get_tar()
email_address = input("Enter email address: ")
b = subprocess.Popen("echo 'Hello! I am sending you my project summaries :) ' | mutt -s Project5 Demo Email -a Assignments.tar.gz -- " +email_address, shell=True)
b.communicate()
