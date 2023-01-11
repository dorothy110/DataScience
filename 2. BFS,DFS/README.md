# Find the Path!

## Overview

In this project I will practice inheritance, graph search, and web
scraping. `scrape.py`.


`scrape.py` will have the following
* GraphSearcher (a class)
* MatrixSearcher (a class)
* FileSearcher (a class)
* WebSearcher (a class)
* reveal_secrets (a function)

```
from collections import deque
import os
import pandas as pd
from bs4 import BeautifulSoup
import copy
import re
import requests
import time

class GraphSearcher:
    def __init__(self):
        self.visited = []
        self.order = []
        self.queue = []
        #Could use deque and be faster/more efficient ??

        
        
    def visit_and_get_children(self, node):
        """ Record the node value in self.order, and return its children
        param: node
        return: children of the given node
        """
        
        raise Exception("must be overridden in sub classes -- don't change me here!")
    
    
    
    def dfs_search(self, node):
        # 1. clear out visited set and order list
        self.visited.clear()
        self.order.clear()
        
        # 2. start recursive search by calling dfs_visit
        
        return self.dfs_visit(node)
    
    
    
    def dfs_visit(self, node):
        # 1. if this node has already been visited, just `return` (no value necessary)
        if node in self.visited:
            return None
        
        # 2. mark node as visited by adding it to the set
        self.visited.append(node)
        
        # 3. call self.visit_and_get_children(node) to get the children
        x = self.visit_and_get_children(node)
        
        # 4. in a loop, call dfs_visit on each of the children
        for c in x:
            self.dfs_visit(c)
         
        
        
    def bfs_search(self, node):
        self.visited.clear()
        self.order.clear()
        
        #print("its all clear", "\n")
        
        return self.bfs_visit(node)
    
    
    
    def bfs_visit(self, node):
        
        #check if node in visited
        if node in self.visited:
            return None
        
        self.visited.append(node)
        
        #print(self.visited, 'what was visited so far?', "\n")
        assert node in self.visited

        
        #find children of node
        y = self.visit_and_get_children(node)
        
        #print(y, "these are the children", "\n")
        
        #add the values to queue, extend to avoid list of lists
        self.queue.extend(y)
        
        #remove values in queue that are in visited
        for x in self.queue:
            if x in self.visited:
                self.queue.remove(x)
        
        ##print(self.queue, "this is the queue", "\n")
        
        #print(self.queue[0], "This is where it's going", "\n")
        
        copying_part = self.queue.pop(0)
        return self.bfs_visit(copying_part)
        

         
            
            
class MatrixSearcher(GraphSearcher):
    def __init__(self, df):
        super().__init__() # call constructor method of parent class
        self.df = df

    def visit_and_get_children(self, node):
        # TODO: Record the node value in self.order
        
        self.order.append(node)
        children = []
        for node, has_edge in self.df.loc[node].items():
            if has_edge == 1:
                children.append(node)
        
        # TODO: use `self.df` to determine what children the node has and append them
        return children
    
    
    
class FileSearcher(GraphSearcher):
    def __init__(self):
        super().__init__() #call constructor of parent
    
    
    def visit_and_get_children(self, node):
        children = []
        
        self.visited.append(node)
        
        #read text file and add list that has .txt in it to get children
        with open("file_nodes/"+node, 'r') as r:
            f = r.readlines()
            for line in f:
                if ".txt" in line:
                    l = line.replace("\n", "")
                    s = l.split(",")
                    children.extend(s)
                elif line != "\n":
                    l = line.replace("\n", "")
                    if l not in self.order:
                        self.order.append(l)

                    

        return children
    
    
    
    def concat_order(self):
        x = ""
        return x.join(self.order)
    
    


class WebSearcher(GraphSearcher):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver #generated from any driver of choice
        self.series = None #to use later
        self.data = []
        
    def visit_and_get_children(self, node):
        children = []
        self.order.append(node)
        self.driver.get(node)
        
        #从HTTP获取响应page_source，使用pandas收集table of data
        x = self.driver.page_source
        #rint(type(x))
        read_data = pd.read_html(x)[0]
        
        #rint(type(read_data))
        
        self.data.append(read_data)
       
        
        for i in self.driver.find_elements_by_tag_name('a'):
            children.append(i.get_attribute('href'))
         #test
        
            
        return children
        
    

        
        
    def table(self):
        
        for x in range(len(self.order)):
            if x == 0:
                df = self.data[x]
                continue
            z = self.data[x] #will be a pandas df
            df = pd.concat([df, z], ignore_index = True)
            
        self.series = df    
        return self.series
             
            
def reveal_secrets(driver, url, travellog):
     #generate a password from the "clues" column of the travellog DataFrame. For example, if travellog is the big DataFrame built after doing BFS (as shown earlier), the password will start with "17138..." 
        driver.get(url)
        ser1 = travellog
        string = ""
        for i in range(len(ser1)):
            string += str(ser1["clue"][i])
        print(string)
        
      #visit url with the driver      

        text = driver.find_element("id","password")
        btn = driver.find_element("id", "attempt-button")
        
      #automate typing the password in the box and clicking "GO" 
        text.clear()
        text.send_keys(string)
        btn.click()
        
      #wait until the pages is loaded (perhaps with time.sleep)
        time.sleep(3)
        
      #click the "View Location" button and wait until the result finishes loading
        btn2 = driver.find_element("id", "securityBtn")
        btn2.click()
        time.sleep(3)
        
        #save the image that appears to a file named 'Current_Location.jpg' 
        #(use the requests module to do the download, once you get the URL from selenium)
        # go to id = image
        element = driver.find_element("id","image")
        # get attribute element.get_attribute("attribute name")
        src = element.get_attribute("src")
        response = requests.get(src)
        with open('Current_Location.jpg','wb') as f:
            f.write(response.content)
        
        
        
        #return the current location that appears on the page (should be "BASCOM HALL")
        results = driver.find_element("id", "location").text        
        return results

    



```



## Part 1: Base Class `GraphSearcher` and DFS on Matrices (`MatrixSearcher`)


## Part 2: BFS on Matrix (`MatrixSearcher`) and Files (`FileSearcher` )

Add a `bfs_search` method to the base searcher `GraphSearcher`.  It  behave the same as
`dfs_search`, but use the BFS algorithm instead of DFS.  The
difference will be evident at the end if someone looks at the `.order`
attribute.

Note that without changing `MatrixSearcher`, it now supports both DFS
and BFS search since it inherits from `GraphSearcher`.

testing example:
```python
import pandas as pd
import scrape

df = pd.DataFrame([
    [0,1,0,1],
    [0,0,1,0],
    [0,0,0,1],
    [0,0,1,0],
], index=["A", "B", "C", "D"], columns=["A", "B", "C", "D"])

m = scrape.MatrixSearcher(df)
m.bfs_search(????)
m.order
```
From "A", for example, `m.order` should be `['A', 'B', 'D', 'C']`.  


### `FileSearcher` Class

Add another class, `FileSearcher`, which also inherits from
`GraphSearcher`.  You job is to implement the three methods `__init__`, `visit_and_get_children`, and `concat_order` and inherit other methods.
1. `__init__`: the constructor of `FileSearcher` which does not take additional parameter besides the instance itself
2. `visit_and_get_children`: visit the file to record its value and get its children
3. `concat_order`: concatenate the values in `self.order` to a string

The nodes of this graph are files in the `file_nodes` directory.  For
example, `1.txt` contains this:

```
M
2.txt,4.txt
```

```
#p3.ipynb
import scrape
f = scrape.FileSearcher()
print(f.visit_and_get_children("1.txt"), f.order, f.concat_order())
```

This means the value for node `1.txt` is "M", and the children of
`1.txt` are `2.txt` and `4.txt`.

All the files will have two lines like this, with a value on the first
line, and a comma-separated list of children on the second line.

The `visit_and_get_children` method should read a node file, record its vlaue in `self.order` and return a list of children.
The `concat_order` method should return all the values concatenated together.  

Could test this in your debug.ipynb notebook.:

```python
import scrape
f = scrape.FileSearcher()
print(f.visit_and_get_children("1.txt"), f.order, f.concat_order())
```

Expected result: `['2.txt', '4.txt'] ['M'] M`.  

Take a look at `bfs_test` in `tester.py` for an example of how `concat_order` should work.

In general, reading test cases is a great way to see how my classes
are supposed to work.  

## Part 3: Web Crawling (`WebSearcher`)

For this part of the project you'll need to install Chrome and a few
packages on your VM:

```
pip3 install selenium==4.1.2 Flask lxml html5lib
sudo apt -y install chromium-browser
```

When it's all done, run both of the following, and verify that both
commands print the same version and it is 106+ (like "106.X.X.X", but it
may be a bigger number if there are browser updates before P3 is
complete):

```
chromium-browser --version
chromium.chromedriver --version
```

**Note**: launching many web browsers via code can quickly eat up
  all the memory on your VM.  You can run the `htop` command to see
  how much memory you have (hit "q" to quit when done).  If you're low
  on memory (you might notice your VM being sluggish), you can run
  `pkill -f -9 chromium` shutdown all browser instances hanging around
  in the background.

### Launching the Website


```
python3 application.py
```

Then, open `http://<YOUR-VM-IP>:5000` in your web browser. **Do not**
use the IP address that is printed to console in the ssh session (it
won't work).  It should look like this:

<img src="webpage.png" width=600>

If you click "TRAVEL HISTORY", you'll enter a graph of pages, each
with a table fragment.  Your job is to search the graph (using the
search methods you wrote earlier), collect all the table fragments,
and concatenate them into one big DataFrame.

### `WebSearcher` Class

Write a `WebSearcher` class that inherits from `GraphSearcher`.  The
constructor should take a Chrome webdriver object as a parameter so
that it is possible to create `WebSearcher` object with `ws =
scrape.WebSearcher(some_driver)`.

For example, one could run the following:

```python
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

options = Options()
options.headless = True
service = Service(executable_path="chromium.chromedriver")
driver = webdriver.Chrome(options=options, service=service)

ws = scrape.WebSearcher(driver)
```

The `visit_and_get_children` method of `WebSearcher` should treat the node as a URL.  It
should use the webdriver to visit that page and return the URLs of
other pages to which the visited page has hyperlinks.  See `web_test`
in the tester for examples of how it should behave.

The `visit_and_get_children` method should also use the following to read any table
fragments on a visited page and store them somewhere (for example, in
an attribute):

https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_html.html

`WebSearcher` should have a `table()` method that
[concatenates](https://pandas.pydata.org/docs/reference/api/pandas.concat.html)
all the fragments in the order they were visited and returns one big
DataFrame.  Use `ignore_index=True` when concatenating.

### Manual Debugging

Here is a code snippet you can use as you write your methods to help
test whether they're working (be sure to replace `YOUR_VM_IP`!):

```python
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import scrape

# kill previous chrome instance if still around (to conserve memory)
os.system("pkill -f -9 chromium")

options = Options()
options.headless = True
service = Service(executable_path="chromium.chromedriver")
driver = webdriver.Chrome(options=options, service=service)

# TODO: use IP address of your VM
start_url = "http://YOUR_VM_IP:5000/Node_1.html"

s = scrape.WebSearcher(driver)
print(s.visit_and_get_children(start_url))

s = scrape.WebSearcher(driver)
s.bfs_search(start_url)

print(s.table())

driver.close()
```

Expected output:

```
['http://YOUR_VM_IP:5000/Node_2.html', 'http://YOUR_VM_IP:5000/Node_4.html']
    clue   latitude   longitude                          description
0      1  43.089034  -89.416128              Picnic Point in Madison
1      7  38.105507  126.910613               Silver Beach in Hawaii
2      1  65.044901  -16.712836  Shore of a Volcanic Lake in Iceland
3      3  48.860945    2.335773                  The Louvre in Paris
4      8  51.180315   -1.829659                 Stonehenge in the UK
5      5  37.434183 -122.321990      Redwood forest in San Francisco
6      2  27.987586   86.925002                 Mt. Everest in Nepal
7      4  34.134117 -118.321495                 Hollywood Sign in LA
8      5  38.655100   90.061800                 Cahokia Mounds in IL
9      9  40.748400   73.985700          Empire State Building in NY
10     4  29.975300   31.137600        Great Sphinx of Giza in Egypt
11     1  47.557600   10.749800     Neuschwanstein Castle in Germany
12     5  38.624700   90.184800        The Gateway Arch in St. Louis
13     3  30.328500   35.444400                      Petra in Jordan
14     2  41.480800   82.683400                    Cedar Point in OH
15     6  43.070010  -89.409450          Quick Trip on Monroe Street
```


## Part 4: `reveal_secrets` function

Write a function (remember that functions aren't inside any class) in
`scrape.py` like the following:

```python
def reveal_secrets(driver, url, travellog):
    ....
```

```
#FindthePath.ipynb

ser1 = s.table()
string = ""
for i in range(len(ser1)):
    string += str(ser1["clue"][i])
string

url = "http://34.71.246.126:5000"

scrape.reveal_secrets(driver, url,s.table())

##password: 1713852459415326
```

The function should do the following:

1. generate a password from the "clues" column of the `travellog` DataFrame.  For example, if `travellog` is the big DataFrame built after doing BFS (as shown earlier), the password will start with "17138..."
2. visit `url` with the `driver`
3. automate typing the password in the box and clicking "GO"
4. wait until the pages is loaded (perhaps with `time.sleep`)
5. click the "View Location" button and wait until the result finishes loading
6. save the image that appears to a file named 'Current_Location.jpg' (use the `requests` module to do the download, once you get the URL from selenium)
7. return the current location that appears on the page (should be "BASCOM HALL")

**Hints for step 6:** jpeg files are a binary format (they don't contain text for a human to read).  You'll need to do some searching online to learn how to (a) download binary data and (b) write it to a file.  Remember to cite any code you copy/paste.  Here are some example Google searches you might start with to find how to do these things:

* "how to write bytes to a file in python"
* "how to fetch a binary file with python requests"
