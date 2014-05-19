espy
====

Elastic Search Python Middle Ware

--

pip install pandas
pip install vincent
pip install elasticsearch (this installs the elasticsearch-py module, don't know why they dont have the py on the end)

then in the folder where you put the python file, do: 
python sony_json.py

unless you have python 3 installed, if that is the case, you need to do pip3 on all the pip commands and python3 on the python command for it to run correctly.

Then, in separate command line window, cd to the folder, and start a server:
python -m SimpleHTTPServer 8000

Then in browser, go to localhost:8000 and you should be able to see graphs.

If you want to play around with adding more graphs, the docs are here:
http://vincent.readthedocs.org/en/latest/quickstart.html

and the code for adding a chart is actually pretty simple, it is at the bottom of the py file. you will just have to be sure to also edit the html file so you can see to it.
