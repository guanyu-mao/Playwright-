import yaml
from collections import defaultdict

class DuplicateKeyLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = defaultdict(list)
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            value = self.construct_object(value_node, deep=deep)
            mapping[key].append(value)
        return dict(mapping)

def load_yaml_with_duplicates(file_path):
    with open(file_path , 'r') as file:
        return yaml.load(file, Loader=DuplicateKeyLoader)
