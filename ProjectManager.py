import json
import os
from datetime import datetime


## create project 
def createProject (projectID,name,target,methods):
    projectData ={
        "id" :projectID,
        "projectName" : name,
        "target": target,
        "methods" : methods,
        "results" :[],
        "logs" : [],
        "createAt": datetime.utcnow().isoformat() + "Z",
        "lastUpdate" : datetime.utcnow().isoformat() + "Z"
    }
    
##save feature
def saveProject(data,filename="project.json"):
    with open(filename,"w") as f:
        json.dump(data, f, indent=4)
        
