import json
import os
from datetime import datetime

PROJECT_FILE = "project.json"  # Subject to change

# Create a project
def createProject(projectID, name, target, methods):
    projectData = {
        "id": projectID,
        "projectName": name,
        "target": target,
        "methods": methods,
        "results": [],
        "logs": [],
        "createAt": datetime.utcnow().isoformat() + "Z",
        "lastUpdate": datetime.utcnow().isoformat() + "Z"
    }
    saveProject(projectData)  # Save the project to file
    print(f"Project '{name}' created successfully!")

# Save feature
def saveProject(data, filename=PROJECT_FILE):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# Load feature
def loadProject():
    if not os.path.exists(PROJECT_FILE):  # Fixed the typo here
        return {"error": "No project found. Please create one or load another."}
    with open(PROJECT_FILE, "r") as file:
        return json.load(file)
