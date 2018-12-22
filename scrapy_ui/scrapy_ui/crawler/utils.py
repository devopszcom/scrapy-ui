import re
import json


def convert_to_json(stats):
    result = re.sub(r'(?is)(datetime\.datetime\([\d\,\s]+\))', r'"\1"', stats).replace("'", '"')
    return json.loads(result)
