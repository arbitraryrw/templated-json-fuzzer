# Templated JSON Fuzzer

## Description

The purpose of this project is to implement a templated fuzzing engine for [Python Data Structures](https://docs.python.org/3/tutorial/datastructures.html) to handle deserialised [JSON input](https://docs.python.org/3/library/json.html#json.load). The project does this by implementing [Depth First Search](<https://en.wikipedia.org/wiki/Depth-first_search#:~:text=Depth%2Dfirst%20search%20(DFS),along%20each%20branch%20before%20backtracking.>) to build a map to each leaf in the tree, and then uses this map to inject values at arbitrary points. This project was created for educational purposes to practically apply algorithm knowledge in a secuity context.

For more details see the corresponding blog post at [nikola.dev](https://nikola.dev/posts/2022-05-29/json-fuzzing-algorithm).

# Design

The project is split into two main components, the `path_finder` and `injector`. path_finder takes a complex object and maps out the paths to each primitive object. injector takes the path structure and uses it to walk the complex object and inject arbitrary values.

To demonstrate the high level design of `path_finder` and `injector` from end to end let's walk through an example. The following structure has 6 primitive values. 4/6 are visualised for demo purposes `hobbies/0/priority` and `hobbies/1/name` are not visualised to avoid overloading the diagram. `path_finder` should generate paths to each primitive value in the structure, these paths are referred to as `parameter_paths`.

```json
                                         +----------------+
                                         |                |
                                         | [              |
                           +------------>|     "username" |
                           |             | ]              |
                           |             |                |
                           |             +----------------+
                           |
                           |             +----------------+
                           |             |                |
                           |             | [              |
{                          |             |     "hobbies", |
    "username": "Jane", ---+         +-->|     0,         |
    "hobbies": [                     |   |     "name"     |
        {                            |   | ]              |
            "name": "climbing", -----+   |                |
            "priority": "high"           +----------------+
        },
        {                                +----------------+
            "name": "skating",           |                |
            "priority": "medium" ---+    | [              |
        }                           |    |     "hobbies", |
    ],                              +--->|     1,         |
    "job": "Physicist" ---+              |     "priority" |
}                         |              | ]              |
                          |              |                |
                          |              +----------------+
                          |
                          |              +------------+
                          |              |            |
                          |              | [          |
                          +------------->|     "job"  |
                                         | ]          |
                                         |            |
                                         +------------+
```

`injector` can then use the `parameter_paths` to manipulate the structure. For example, `injector` could use the parameter path `hobbies/1/name` in the structure above to replace the value `skating` to `PAYLOAD`. Note that this should be the only value that is modified in the template JSON object.

```json
{
  "username": "Jane",
  "hobbies": [
    {
      "name": "climbing",
      "priority": "high"
    },
    {
      "name": "PAYLOAD",
      "priority": "medium"
    }
  ],
  "job": "Physicist"
}
```

# Path Finder Implementation

`path_finder` generates a list of lists that contains the path to each primitive value in a deserialised JSON structure. A path to a key attribute in a structure is known as a `parameter_path`. To demonstrate this, below is an example of the parameter paths generated for a basic JSON structure. Note, within the algorithm the result is represented as `[["name], ["age]]`, not as two separate lists as shown below for demonstration purposes.

```json
                          +-------------+
                          |             |
                          | [           |
                      +-->|     "name"  |
+------------------+  |   | ]           |
|                  |  |   |             |
| {                +--+   +-------------+
|   "name":"test", |
|   "age": "100"   |
| }                +--+   +-------------+
|                  |  |   |             |
+------------------+  |   | [           |
                      +-->|     "age"   |
                          | ]           |
                          |             |
                          +-------------+
```

Implementing `path_finder` in Python is straightforward using the [Depth First Search](https://en.wikipedia.org/wiki/Depth-first_search) algorithm. Python's dynamically typed nature means we can have a single function that accepts a deserialised JSON structure and recursively evaluates the result. The function determines if an input is a `list` or a `dict`, depending on which it is, the function either invokes a `list` handler, or a `dict` handler. If it is neither, we know we have hit the bottom of the nested structure (a Python primitive value). The `list` and `dict` handlers iterate on the input structure and recursively call the original function for each index / entry. Programmatically this looks like:

```python
def map_structure(structure, stack=None, depth=0):

    # call the list handler
    if isinstance(structure, dict):
        _dict_handler(input_dict=structure, stack=stack, depth=depth)

     # call the list handler
    if isinstance(structure, list):
        _list_handler(input_list=structure, stack=stack, depth=depth)

    return stack  # return the stack of parameters used to get to the primitive
```

The `list` and `dict` handlers are almost identical, the only difference is that the `list` handler iterates on an index and the `dict` handler iterates on a key. For demonstration purposes let's look at the `dict` handler:

```python
def _dict_handler(input_dict, stack=None, depth=0):
    # Check if there are any parent parameters, if not this is the first level
    if stack is None:
        stack = []

    parameter_paths = []  # List to store completed parameter paths

    for key, value in input_dict.items():  # Iterate on each key attribute
        stack = stack[:depth]  # Remove non-applicable keys for variable length children
        stack.append(key)  # append current key to parameter path chain

        # Call the previous function for each key in the structure
        result = self.map_structure(structure=value, stack=stack, depth=depth + 1)

        # We either extend / append depending on if the value is a primitive or list/dict.
        # This is done to avoid multi depth structures returning nested list / dict results
        if not isinstance(value, list) and not isinstance(value, dict):
            parameter_paths.append(result)
        else:
            parameter_paths.extend(result)

    return parameter_paths  # return the completed parameter path

```

The full source for all of the `path_finder` functions can be found in [path_finder.py](https://github.com/arbitraryrw/templated-json-fuzzer/blob/main/jsonfuzzer/parser/path_finder.py#L4-L112). To demonstrate how these functions work together, I've included log statements at the beginning and end of the `map_structure()` function. As well as log statements at the end of the `_list_handler` and `_dict_handler` functions. Consider the following structure. Note the structure has complex relationships with variable length / type children.

```python
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
```

Observe how the `list` and `dict` handlers recursively call the `map_structure()` function, building a stack of parameters used to navigate to a primitive value.

```python
Starting - structure: {'name': 'blah', 'hobbies': ['climbing', ['skating'], 'walking']} - stack: None - depth: 0
Starting - structure: blah - stack: ['name'] - depth: 1
Done - ['name']
Starting - structure: ['climbing', ['skating'], 'walking'] - stack: ['hobbies'] - depth: 1
Starting - structure: climbing - stack: ['hobbies', 0] - depth: 2
Done - ['hobbies', 0]
Starting - structure: ['skating'] - stack: ['hobbies', 1] - depth: 2
Starting - structure: skating - stack: ['hobbies', 1, 0] - depth: 3
Done - ['hobbies', 1, 0]
List handler done: [['hobbies', 1, 0]]
Starting - structure: walking - stack: ['hobbies', 2] - depth: 2
Done - ['hobbies', 2]
List handler done: [['hobbies', 0], ['hobbies', 1, 0], ['hobbies', 2]]
Dict handler done:  [['name'], ['hobbies', 0], ['hobbies', 1, 0], ['hobbies', 2]]

Final result: [['name'], ['hobbies', 0], ['hobbies', 1, 0], ['hobbies', 2]]
```

This approach scales with complex nested JSON structures. `path_finder` recursively traverses nested structures using [Depth First Search](https://en.wikipedia.org/wiki/Depth-first_search), meaning even unusual nested structures are handled elegantly.

```json
                                                            +--------+
                                                            |        |
                                                            | [      |
                                                            |     0, |
                                                            |     0, |
                                                   +------->|     0, |
                                                   |        |     0, |
                                                   |        |     0  |
                                                   |        | ]      |
+-----------------------------------------+        |        |        |
|                                         |        |        +--------+
| [                                       |        |
|     [                                   +--------+        +-----------+
|         [                               |                 |           |
|             [                           |                 | [         |
|                 [                       |                 |     0,    |
|                     "seriously",        |                 |     0,    |
|                     {                   |                 |     0,    |
|                         "why": "though" +---------------->|     0,    |
|                     },                  |                 |     1,    |
|                     "jeez"              |                 |     "why" |
|                 ]                       |                 | ]         |
|             ]                           |                 |           |
|         ]                               |                 +-----------+
|     ]                                   +--------+
| ]                                       |        |        +--------+
|                                         |        |        |        |
+-----------------------------------------+        |        | [      |
                                                   |        |     0, |
                                                   |        |     0, |
                                                   +------->|     0, |
                                                            |     0, |
                                                            |     2  |
                                                            | ]      |
                                                            |        |
                                                            +--------+
```

# Injector Implementation

The parameter paths generated by `path_finder` can then be used by `injector` to manipulate a template (the deserialised JSON structure). This post focuses on three types of manipulations categorised by test scenarios: modifying, removing, and reordering key-attributes. For simplicity, these three scenarios are grouped into two concepts algorithmically: generating parameter permutations (modifying key-attributes), and structural permutations (removing and reordering key-attributes). This section demonstrates these concepts with practical examples, and talks about the implementation.

### Parameter Permutations

Parameter permutations refers to modifying a key-attribute parameter. For example, changing a key-attribute from one value to another. This is the most common use case for most general purpose unit testing and fuzzing. To demonstrate this, the structure below will generate 3 parameter permutations for each parameter with the payload `PAYLOAD`. Note that `injector` only modifies only one parameter at a time and walks the template using the parameter path generated by `path_finder`.

```json
                                                   +---------------------------------+
                                                   |                                 |
                                                   | {                               |
                                                   |     "hobbies": [                |
                                                   |         {                       |
                                                   |             "name": "PAYLOAD",  |
                                                   |             "gear": [           |
                                         +-------->|                 "helmet",       |
                                         |         |                 "roller blades" |
                                         |         |             ]                   |
                                         |         |         }                       |
                                         |         |     ]                           |
                                         |         | }                               |
                                         |         |                                 |
                                         |         +---------------------------------+
                                         |
+---------------------------------+      |         +---------------------------------+
|                                 |      |         |                                 |
| {                               |      |         | {                               |
|     "hobbies": [                +------+         |     "hobbies": [                |
|         {                       |                |         {                       |
|             "name": "skating",  |                |             "name": "skating",  |
|             "gear": [           |                |             "gear": [           |
|                 "helmet",       +--------------->|                 "PAYLOAD",      |
|                 "roller blades" |                |                 "roller blades" |
|             ]                   |                |             ]                   |
|         }                       |                |         }                       |
|     ]                           +-------+        |     ]                           |
| }                               |       |        | }                               |
|                                 |       |        |                                 |
+---------------------------------+       |        +---------------------------------+
                                          |
                                          |        +--------------------------------+
                                          |        |                                |
                                          |        | {                              |
                                          |        |     "hobbies": [               |
                                          |        |         {                      |
                                          |        |             "name": "skating", |
                                          |        |             "gear": [          |
                                          +------->|                 "helmet",      |
                                                   |                 "PAYLOAD"      |
                                                   |             ]                  |
                                                   |         }                      |
                                                   |     ]                          |
                                                   | }                              |
                                                   |                                |
                                                   +--------------------------------+
```

From an implementation perspective, `path_finder` has already done the hard work. `injector` simply walks the JSON structure using the parameter paths. This takes the form of a glorified for loop with some deep copying logic to avoid unintentionally changing template values. Python is particularly useful here because the same logic works for both `dict` and `list` data types, see the snippet below. Note, the full source for this function can be found in [modify_attribute_in_structure_by_path()](https://github.com/arbitraryrw/templated-json-fuzzer/blob/main/jsonfuzzer/parser/injector.py#L9).

```python
target_dict = copy.deepcopy(structure)

current = target_dict
for index, k in enumerate(path):

    # We have not reached our destination yet, keep digging
    if index + 1 != len(path):
        current = current[k]  # Update current reference
        continue

    # We hit the target attribute
    current[k] = "VALUE_WE_WANT_TO_INJECT"
    break

return target_dict
```

## Structural Permutations

Structural permutations are split into two parts, removing key-attributes, and re-ordering key-attributes. Both of these concepts are grouped together under _structural permutations_ because they focus on manipulating the structure of a deserialised JSON object. Ultimately, both removing and re-ordering key attributes have the same end goal of generating output that can be used to test how an application validates the structure of a JSON object. Unlike parameter permutations which focus more on exercising an application's input validation logic.

From a test case perspective, structural permutations are particularly useful for complex JSON structures. This is because multiple parent child key-attribute relationships are: 1) harder to validate, and 2) harder to comprehensively test. This is a great way to validate how robust an application's JSON key-attribute structural validation is.

### Removing key attributes

Removing key attributes generates permutations of a structure with each point of the chronological parameter path removed. For example, the path `a/b/c` would generate three permutations. `a/b` removing `c`, `a` removing `b/c`, and `None` removing `a/b/c`. To demonstrate this, the structure below will generate 6 missing attribute permutations, one for each logical attribute.

**Pro tip**: it's easier to read the diagram bottom up.

```json
                                                       +----+
                                                       |    |
                                       +-------------->| {} |
                                       |               |    |
                                       |               +----+
                                       |
                                       |               +-------------------+
                                       |               |                   |
                                       |               | {                 |
                                       |     +-------->|     "hobbies": [] |
                                       |     |         | }                 |
                                       |     |         |                   |
                                       |     |         +-------------------+
                                       |     |
                                       |     |         +---------------------------------+
                                       |     |         |                                 |
                                       |     |         | {                               |
                                       |     |         |     "hobbies": [                |
                                       |     |         |         {                       |
                                       |     |         |             "gear": [           |
                                       |     |         |                 "helmet",       |
                                       |     |    +--->|                 "roller blades" |
                                       |     |    |    |             ]                   |
                                       |     |    |    |         }                       |
                                       |     |    |    |     ]                           |
                                       |     |    |    | }                               |
                                       |     |    |    |                                 |
+---------------------------------+    |     |    |    +---------------------------------+
|                                 -----+     |    |
| {                               |          |    |    +-------------------------------+
|     "hobbies": [                -----------+    |    |                               |
|         {                       |               |    | {                             |
|             "name": "skating",  ----------------+    |     "hobbies": [              |
|             "gear": [           |                    |         {                     |
|                 "helmet",       -------------------->|             "name": "skating" |
|                 "roller blades" |                    |         }                     |
|             ]                   -----------------+   |     ]                         |
|         }                       |                |   | }                             |
|     ]                           ----------+      |   |                               |
| }                               |         |      |   +-------------------------------+
|                                 |         |      |
+---------------------------------+         |      |   +---------------------------------+
                                            |      |   |                                 |
                                            |      |   | {                               |
                                            |      |   |     "hobbies": [                |
                                            |      |   |         {                       |
                                            |      |   |             "name": "skating",  |
                                            |      |   |             "gear": [           |
                                            |      +-->|                 "roller blades" |
                                            |          |             ]                   |
                                            |          |         }                       |
                                            |          |     ]                           |
                                            |          | }                               |
                                            |          |                                 |
                                            |          +---------------------------------+
                                            |
                                            |          +--------------------------------+
                                            |          |                                |
                                            |          | {                              |
                                            |          |     "hobbies": [               |
                                            |          |         {                      |
                                            |          |             "name": "skating", |
                                            |          |             "gear": [          |
                                            +--------->|                 "helmet"       |
                                                       |             ]                  |
                                                       |         }                      |
                                                       |     ]                          |
                                                       | }                              |
                                                       |                                |
                                                       +--------------------------------+
```

Note that there is automatic deduplication built in to avoid duplicate tests. For example, without deduplication the structure below would generate four missing payloads for `a` and `b` because they both have the same parent. The diagram below demonstrates that only 3 are generated.

```json
                                   +----+
                                   |    |
                              +--->| {} | <--Would generate this twice without deduplication
                              |    |    |
                              |    +----+
                              |
+------------------------+    |    +------------------------+
|                        |    |    |                        |
| {                      +----+    | {                      |
|     "deduplication": [ |         |     "deduplication": [ |
|         "a",           +-------->|         "b"            |
|         "b"            |         |     ]                  |
|     ]                  +---+     | }                      |
| }                      |   |     |                        |
|                        |   |     +------------------------+
+------------------------+   |
                             |     +------------------------+
                             |     |                        |
                             |     | {                      |
                             |     |     "deduplication": [ |
                             +---->|         "a"            |
                                   |     ]                  |
                                   | }                      |
                                   |                        |
                                   +------------------------+
```

From an implementation perspective, `injector` simply walks the JSON structure using the parameter path, exactly like the parameter permutations variant. The only difference is once the target attribute is reached, the value is deleted instead of replaced. The full source for this function can be found in [remove_attribute_in_structure_by_path()](https://github.com/arbitraryrw/templated-json-fuzzer/blob/main/jsonfuzzer/parser/injector.py#L49).

```python
# Take a deep copy to avoid accidentally changing the original template
target_dict = copy.deepcopy(structure)

current = target_dict
for index, k in enumerate(path):

    # We have not reached our destination yet, keep digging
    if index + 1 != len(path):  # path is the parameter path we want to remove
        current = current[k]  # update our current reference
        continue

    del current[k]  # delete the attribute
    break

return target_dict
```

### Reordering key attributes

Reordering key-attributes generates permutations for a structure with the payload at each point in the chronological parameter path. For example, the path `a/b/c` would generate two permutations. One for `a/b`, ignoring `c`, and one for `a`, ignoring `b/c`. It is not uncommon for applications to assume `b/c` exists if `a` exists, or `c` exists if `a/b` exists. To demonstrate this, the structure below will generate 3 permutations for each parent in the parameter path with the payload `STRUCTURE PAYLOAD`.

```json
                                                   +-----------------------------------------+
                                                   |                                         |
                                                   | {                                       |
                                                   |     "hobbies": [                        |
                                                   |         {                               |
                                         +-------->|             "name": "skating",          |
                                         |         |             "gear": "STRUCTURE PAYLOAD" |
                                         |         |         }                               |
                                         |         |     ]                                   |
                                         |         | }                                       |
+---------------------------------+      |         |                                         |
|                                 |      |         +-----------------------------------------+
| {                               |      |
|     "hobbies": [                +------+         +-----------------------------+
|         {                       |                |                             |
|             "name": "skating",  |                | {                           |
|             "gear": [           |                |     "hobbies": [            |
|                 "helmet",       +--------------->|         "STRUCTURE PAYLOAD" |
|                 "roller blades" |                |     ]                       |
|             ]                   |                | }                           |
|         }                       |                |                             |
|     ]                           +-------+        +-----------------------------+
| }                               |       |
|                                 |       |        +------------------------------------+
+---------------------------------+       |        |                                    |
                                          |        | {                                  |
                                          +------->|     "hobbies": "STRUCTURE PAYLOAD" |
                                                   | }                                  |
                                                   |                                    |
                                                   +------------------------------------+
```

Note that there is automatic deduplication built in to avoid duplicate tests. For example, the structure below would generate two structural payloads for `a` and `b` as they both have the same parent. The diagram below demonstrates that only one is generated.

```json
+------------------------+
|                        |      +------------------------------------------+
| {                      |      |                                          |
|     "deduplication": [ |      | {                                        |
|         "a",           +----->|     "deduplication": "STRUCTURE PAYLOAD" |
|         "b"            |      | }                                        |
|     ]                  |      |                                          |
| }                      |      +------------------------------------------+
|                        |
+------------------------+
```

From an implementation perspective, reordering key attributes uses the exact same function as the parameter permutations variant. The difference is what is targeted by the [modify_attribute_in_structure_by_path()](https://github.com/arbitraryrw/templated-json-fuzzer/blob/main/jsonfuzzer/parser/injector.py#L9) function. Instead of targeting a full parameter path from `path_finder`, we slice the path one index off at a time and inject a value at that point. The full source can be found in [generate_structure_payloads_by_path()](https://github.com/arbitraryrw/templated-json-fuzzer/blob/main/jsonfuzzer/parser/injector.py#L88), this looks like:

```python
def generate_structure_payloads_by_path(structure, path, value_to_inject):
    return[
            self.modify_attribute_in_structure_by_path(
                structure=structure,
                path=path[:-index],  # Cut the last key off, don't fuzz the primitive
                value_to_inject=value_to_inject,
            )
            for index, _ in enumerate(path)
            if path[:-index] != list()  # Avoid redundant payloads when there is nothing to change
    ]
```

## Usage

The demo entrypoint is `main.py`, you can run the demo using your python interpreter:

```
python3 main.py
```

## Testing

Unittest documentation [here](https://docs.python.org/3/library/unittest.html). Example usage of unittest discovering tests in the `test` directory.

```
python3 -m unittest discover -s test
```
