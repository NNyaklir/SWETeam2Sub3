import subprocess
import json
import urllib.parse
import logging
from typing import List
import os
from pathlib import Path

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Node:
    def __init__(self, node_id: str, name: str, severity: str, children: list = None):
        self.node_id = node_id
        self.name = name
        self.severity = severity
        self.children = children if children is not None else []

    def add_child(self, child: 'Node'):
        """Add a child node."""
        self.children.append(child)

    def to_dict(self) -> dict:
        """Recursively convert the Node (and its children) into a dictionary."""
        return {
            "node_id": self.node_id,
            "name": self.name,
            "severity": self.severity,
            "children": [child.to_dict() for child in self.children]
        }

    def __repr__(self):
        return f"Node(node_id={self.node_id!r}, name={self.name!r}, severity={self.severity!r}, children={self.children!r})"


def get_severity(status_code: int) -> str:
    """
    A more comprehensive mapping from HTTP status code to severity.
    """
    if status_code in {200, 204}:
        return "High"
    elif status_code in {403, 401}:
        return "Medium"
    elif status_code in {404, 301, 302, 500}:
        return "Low"
    else:
        return "Info"


def insert_url_into_tree(root: Node, url: str, severity: str):
    """
    Inserts the URL into the tree by splitting its path into segments.
    """
    parsed = urllib.parse.urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    if root.node_id != base:
        logger.warning(f"URL {url} does not match the root base {root.node_id}. Skipping insertion.")
        return

    segments = [seg for seg in parsed.path.split("/") if seg]
    current_node = root
    current_url = base
    for seg in segments:
        current_url += f"/{seg}"
        found = next((child for child in current_node.children if child.name == seg), None)
        if not found:
            new_node = Node(node_id=current_url, name=seg, severity="Low")
            current_node.add_child(new_node)
            current_node = new_node
        else:
            current_node = found
    current_node.severity = severity

def save_tree_to_file(tree: Node, project_id: str, target_url: str):
    """
    Saves the tree to a JSON file at: ./output/<project_id>/<url_host>/tree.json
    """
    parsed = urllib.parse.urlparse(target_url)
    host_folder = parsed.netloc.replace("https://", "_")
    host_folder = host_folder.replace(":", "_")

    output_path = Path("output") / project_id / host_folder
    output_path.mkdir(parents=True, exist_ok=True)

    tree_path = output_path / "tree.json"
    with open(tree_path, "w") as f:
        json.dump(tree.to_dict(), f, indent=2)

    logger.info(f"[+] Tree saved to {tree_path}")

def run_wfuzz_and_build_tree(
    target_url: str,
    wordlist: str,
    user_agent: str = None,
    proxy: str = None,
    delay: float = 0.0
) -> Node:
    """
    Runs wfuzz using subprocess with JSON output, parses the results,
    and builds a Node tree.

    Args:
        target_url (str): The target URL with the 'FUZZ' placeholder.
        wordlist (str): Path to the wordlist file.
        user_agent (str, optional): Custom User-Agent header.
        proxy (str, optional): Proxy address (host:port).
        delay (float, optional): Delay between requests in seconds.

    Returns:
        Node: The root of the resulting tree.
    """
    command = [
        "wfuzz",
        "-w", wordlist,
        "-o", "json"
    ]

    if user_agent:
        command += ["-H", f"\"User-Agent: {user_agent}\""]

    if proxy:
        command += ["-p", proxy]

    if delay and delay > 0:
        command += ["-s", str(delay)]

    command.append(target_url+"FUZZ")

    logger.info(f"[*] Running wfuzz command: {' '.join(command)}")

    process = subprocess.run(command, capture_output=True, text=True)

    if process.returncode != 0:
        logger.error(f"[!] Wfuzz error: {process.stderr}")
        return None

    json_start = process.stdout.find('[')
    if json_start == -1:
        logger.error("[!] JSON output not found in wfuzz stdout.")
        return None

    json_str = process.stdout[json_start:]
    try:
        results = json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"[!] Failed to parse JSON output from wfuzz: {e}")
        return None
    
    if not isinstance(results, list):
        logger.error("[!] Unexpected wfuzz output format.")
        return None

    parsed_target = urllib.parse.urlparse(target_url.replace("FUZZ", ""))
    base_url = f"{parsed_target.scheme}://{parsed_target.netloc}"
    root = Node(node_id=base_url, name=parsed_target.netloc, severity="Low")

    for result in results:
        url = result.get("url")
        status_code = result.get("code")
        if url is None or status_code is None:
            continue
        severity = get_severity(status_code)
        insert_url_into_tree(root, url, severity)

    return root


