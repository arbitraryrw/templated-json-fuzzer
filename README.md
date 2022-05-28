# Templated JSON Fuzzer

## Description

The purpose of this project is to implement a templated fuzzing engine for [Python Data Structures](https://docs.python.org/3/tutorial/datastructures.html) to handle deserialised [JSON input](https://docs.python.org/3/library/json.html#json.load). The project does this by implementing [Depth First Search](<https://en.wikipedia.org/wiki/Depth-first_search#:~:text=Depth%2Dfirst%20search%20(DFS),along%20each%20branch%20before%20backtracking.>) to build a map to each leaf in the tree, and then uses this map to inject values at arbitrary points.

## Design

The project is split into two main components, the `path_finder` and `injector`. `path_finder` takes a complex object and maps out the paths to each primitive object. `injector` takes the path structure and uses it to walk the complex object and inject arbitrary values.

To demonstrate `path_finder`, the following structure has 6 primitive values. 4/6 are visualed for demo purposes `hobbies/0/priorty` and `hobbies/1/name` are not visualised to avoid overloading the diagram:

```
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

This can then be used by the `injector` to add / remove values. For example, `injector` could use the param path `hobbies/1/name` in the structure above to inject the value `PAYLOAD`:

```
{
    "username": "Jane",
    "hobbies": [
        {
            "name": "climbing",
            "priority": "high"
        },
        {
            "name": "_PAYLOAD_",
            "priority": "medium"
        }
    ],
    "job": "Physicist"
}
```

Decoupling the structure parsing logic from the injection logic has three main benefits:

1. Reduces code complexity, makes the code more unit testable, and produces an output that is reusable / tracable.
2. Enables fuzzing logic to intelligently understand what was changed in a structure to achieve an output
3. Simplifies parent child relationship mappings. For example, path `a/b/c` tells us that `c` is a child of `b` which is a child of `a`. We can use to to test logical permutations such as `a/b`, ignoring `c`, or just `a` by itself, ignoring `b/c`.

The disadvantage is that it results in having to walk the complex structure multiple times, reducing the efficiency of the algorithm.

### Path Finder

`path_finder` will generate a list of lists that contains the paths to each primitive in a structure. To demonstrate this, below is an example of the primitive parameter paths in a basic structure. Note, within the algorithm this will be represented as `[["name], ["age]]`, not as two separate lists as shown above for demonstration purposes.

```
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

This same concept applies to complex nested structures, `path_finder` recursively traverses nested structures to identify the path to each primitive. By proxy it also handles unusual nested structures:

```
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

### Injector

`injector` uses parameter paths generated by `path_finder` to traverse structures and inject values at specific locations. There are helper functions to use this functionality to generate structure permutations automatically. There are three types of permutations that are supported:

1. Parameter permutations
1. Structural permutations
1. Missing attribute permutations

#### Parameter Permutations

Parameter permutations takes parameter paths, a payload, and a structure. It generates permutations of the structure with the payload for each parameter defined in the parameter paths. To demonstrate this, the structure below will genenerate 3 parameter permutations for each parameter with the payload `PAYLOAD`. Note that it only modifies only one parameter at a time.

```
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

#### Structural Permutations

Structural permutations takes parameter paths, a payload, and a structure. It generates permutations for a structure with the payload at each point in the chronological parameter path. For example, the path `a/b/c` would generate permutations for `a/b` and `a`. To demonstrate this, the structure below will genenerate 3 structural permutations for each parent in the parameter path with the payload `STRUCTURE PAYLOAD`.

```
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

Note that there is automatic deduplication built in to avoid duplicate tests. For example, the structure below would generate two structural payloads for `a` and `b` as they both have the same parent. However, only one is generated using the structural permutations helper functions.

```
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

#### Missing Attribute Permutations

Missing attribute permutations takes parameter paths and a structure. It generates permutations of the structure for each point in the chronological parameter path, removing one attribute a time. For example, the path `a/b/c` would generate permutations `a/b`, `a`, and `None`. To demonstrate this, the structure below will genenerate 6 missing attribute permutations, one for each parameter, and one for each parent.

```
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

Note that there is automatic deduplication built in to avoid duplicate tests. For example, the structure below would generate four missing payloads for `a` and `b` as they both have the same parent. However, only three are generated using the missing attribute permutations helper functions.>

```
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
