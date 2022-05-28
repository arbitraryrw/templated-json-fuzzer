import json
from jsonfuzzer.core.fuzzer import Fuzzer
from jsonfuzzer.util.util import Util
from jsonfuzzer.parser.path_finder import PathFinder

path_finder = PathFinder()
fuzzer = Fuzzer()


test_json = """
{
    "name": "blah",
    "hobbies": [
        "climbing",
        [
            "skating"
        ],
        "walking"
    ]
}
"""

structure = json.loads(test_json)

print(Util.pretty_print(structure))

paramater_paths = path_finder.map_structure(structure=structure)

print(paramater_paths)
print(Util.pretty_print(paramater_paths))


parameter_payloads = fuzzer.generate_structure_parameter_permutations_for_payload(
    structure=structure,
    paramater_paths=paramater_paths,
    value_to_inject="PAYLOAD",
)

print(f"Total of {len(parameter_payloads)} parameter payloads")
print(Util.pretty_print(parameter_payloads))


structure_payloads = fuzzer.generate_structure_permutations_for_payload(
    structure=structure,
    paramater_paths=paramater_paths,
    value_to_inject="STRUCTURE PAYLOAD",
)

print(f"Total of {len(structure_payloads)} structure payloads")
print(Util.pretty_print(structure_payloads))

print(structure_payloads)

missing_attribute_payloads = fuzzer.generate_structure_missing_attribute_permutations(
    structure=structure, paramater_paths=paramater_paths
)

print(f"Total of {len(missing_attribute_payloads)} missing attribute payloads")
print(Util.pretty_print(missing_attribute_payloads))
