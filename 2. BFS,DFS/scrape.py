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

    


