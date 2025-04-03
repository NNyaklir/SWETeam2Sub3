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