import subprocess
from services.crawlerManager.node import Node

class ScanService:
    def run_wfuzz(self, target_url: str, wordlist: str) -> Node:
        command = f"wfuzz -w {wordlist} -o json {target_url}FUZZ"
        process = subprocess.run(command, capture_output=True, text=True, shell=True)
        
        if process.returncode == 0:
            # Parse the JSON output and build the Node tree
            # Implement the parsing logic based on the wfuzz JSON format
            pass
        
        return None