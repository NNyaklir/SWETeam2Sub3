import json
import os
from datetime import datetime

PROJECT_FILE="example.json" ##subject to change

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
    
## load feature    
def loadProject():
    if not os.path.exisits(PROJECT_FILE):
        return{"error":"No Project found. Please create one, or load another"}
    with open(PROJECT_FILE, "r") as file:
        return json.load(file)

