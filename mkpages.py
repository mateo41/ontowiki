"""     
This script is used to generate wiki pages which are in a special template
format. It has also been modified to output the format into json, so we
can visualize it using the JIT(Javascript Information Toolkit)  

Matt Rodriguez 
9/12/2011
"""
class Node:
    
    def __init__ (self, parent, parentid, concept, conceptid):
        self.parent = self.handle_bad_chars(parent)
        self.parentid = parentid
        self.concept = self.handle_bad_chars(concept)
        self.conceptid = conceptid 
        self.children = []
        self.correct_name = ""
        if self.concept != concept:
            self.correct_name = concept
   
    def handle_bad_chars(self, concept): 
         return concept.replace("[", "((").replace("]", "))")

    def add_child(self, child):
        self.children.append(child)

    def getid(self):
        return self.conceptid 

    def getparentid(self):
        return self.parentid
     
    def pretty_print(self):
        print "{{Ontology" 
        print "|Name=%s" %  self.concept
        print "|ParentName=%s" %  self.parent
        print "|Children=%s" % ";".join(self.children) 
        print "|Definition="
        print "|Label="
        print "|Reference="
        print "|Comments="
        print "|Source="
        print "|Citation="
        print "}}" 
   
    def serialize_json(self): 
        json_node = { "id": self.conceptid, "name": self.concept}  
        data = {"data":{"concept":self.concept, "relation": "subclass of " + self.parent}} 
        json_node.update(data)
        return json_node
               
    def robot_print(self):   
        keys = ["Name", "CorrectName", "ParentName", "Children", "Definition",
                 "Label", "Reference", "Comments", "Source", "Citation" ]
        vals = [ "" for i in range(len(keys))]
        attrs = dict(zip(keys,vals)) 
        attrs["Name"] = self.concept
        attrs["CorrectName"] = self.correct_name
        attrs["ParentName"] = self.parent
        attrs["Children"] = ";".join(self.children)
        f = lambda s: '|' + s[0] + '=' + s[1]
        pagevars = "".join(map(f, attrs.items())) 
        pagetext = "{{Ontology" + pagevars + "}}"
        print "%s@%s" % (self.concept, pagetext) 

class Ontology:
      
     def __init__(self):
         self.ontology = {}
         self.orphans = []

     def add_node(self, node):
         nodeid = node.getid() 
         self.ontology.update({nodeid: node}) 
         parentid = node.getparentid()
         if nodeid != parentid: 
            try: 
                self.ontology[parentid].add_child(node.conceptid) 
            except KeyError:
                #print "Parent %s,%s doesn't exist" % (parentid, node.parent)
                self.orphans.append(node)
     
     def handle_bad_chars(self, concept): 
         return concept.replace("[", "((").replace("]", "))")

     def parse(self, file_handle): 
         for line in file_handle:
             tokens = line.strip().replace('"',"").split("|")
             strip = lambda x: x.strip()
             parent, concept, conceptid, parentid  = map(strip, tokens)
             node = Node(parent, parentid, concept, conceptid )
             self.add_node(node)
             #print "Added node: %s,%s" % ( conceptid, concept ) 

     def pretty_print(self): 
         for k in self.ontology.keys():
             node = self.ontology[k]
             node.pretty_print()
    
     def robot_print(self):         
         for k in self.ontology.keys():
             node = self.ontology[k]
             node.robot_print()
      
     def make_json(self):
         #import pdb 
         #pdb.set_trace()
         root = self.ontology["1"]
         self.json = self.dfs(root,1,5) 
     
     def dfs(self, node, depth, limit): 
         print node.concept
         node_dict = node.serialize_json() 
         node_dict["children"] = []
         for child in node.children:
             #print child 
             if depth < limit:
                 node_dict["children"].append(self.dfs(self.ontology[child], depth + 1, limit))
         return node_dict    
     
     def get_json(self):
         return self.json

     def adopt_orphans(self):
         for node in self.orphans:      
             parentid = node.getparentid() 
             self.ontology[parentid].add_child(node.conceptid) 
      
      
def main():
    f = open("ontology3.csv")
    f.readline()
    onto = Ontology()
    onto.parse(f) 
    onto.adopt_orphans()
    #onto.pretty_print() 
    #onto.robot_print() 
    onto.make_json()
    print "var json = " + str(onto.get_json()) + ";" 



if __name__ == "__main__":
    main()
