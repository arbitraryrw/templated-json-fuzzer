import unittest
from jsonfuzzer.parser.injector import Injector


class TestPathFinder(unittest.TestCase):
    def setUp(self) -> None:
        self.injector = Injector()
        return super().setUp()

    def test_modify_attribute_in_structure_by_path_simple_dict(self):
        test_structure = {"user_id": "AAAAA", "address": "AAAAA"}
        test_parameter_paths = [["user_id"], ["address"]]

        expected_results = [
            {"user_id": "nice_one!", "address": "AAAAA"},
            {"user_id": "AAAAA", "address": "nice_one!"},
        ]

        for index, path in enumerate(test_parameter_paths):
            result = self.injector.modify_attribute_in_structure_by_path(
                structure=test_structure, path=path, value_to_inject="nice_one!"
            )

            self.assertEqual(result, expected_results[index])

    def test_modify_attribute_in_structure_by_path_dict_with_list_of_primitives(self):
        test_structure = {
            "ports": [
                80,
                443,
            ],
            "other_ports": [25],
        }
        test_parameter_paths = [["ports", 0], ["ports", 1], ["other_ports", 0]]

        expected_results = [
            {"ports": ["nice_one!", 443], "other_ports": [25]},
            {"ports": [80, "nice_one!"], "other_ports": [25]},
            {"ports": [80, 443], "other_ports": ["nice_one!"]},
        ]

        for index, path in enumerate(test_parameter_paths):
            result = self.injector.modify_attribute_in_structure_by_path(
                structure=test_structure, path=path, value_to_inject="nice_one!"
            )

            self.assertEqual(result, expected_results[index])

    def test_modify_attribute_in_structure_by_path_list_of_dicts(self):
        test_structure = [
            {"name": "a", "type": "b"},
            {"name": "c", "type": "d"},
            {"name": "e", "type": "f"},
        ]

        test_parameter_paths = [
            [0, "name"],
            [0, "type"],
            [1, "name"],
            [1, "type"],
            [2, "name"],
            [2, "type"],
        ]

        expected_results = [
            [
                {"name": "nice_one!", "type": "b"},
                {"name": "c", "type": "d"},
                {"name": "e", "type": "f"},
            ],
            [
                {"name": "a", "type": "nice_one!"},
                {"name": "c", "type": "d"},
                {"name": "e", "type": "f"},
            ],
            [
                {"name": "a", "type": "b"},
                {"name": "nice_one!", "type": "d"},
                {"name": "e", "type": "f"},
            ],
            [
                {"name": "a", "type": "b"},
                {"name": "c", "type": "nice_one!"},
                {"name": "e", "type": "f"},
            ],
            [
                {"name": "a", "type": "b"},
                {"name": "c", "type": "d"},
                {"name": "nice_one!", "type": "f"},
            ],
            [
                {"name": "a", "type": "b"},
                {"name": "c", "type": "d"},
                {"name": "e", "type": "nice_one!"},
            ],
        ]

        for index, path in enumerate(test_parameter_paths):
            result = self.injector.modify_attribute_in_structure_by_path(
                structure=test_structure, path=path, value_to_inject="nice_one!"
            )

            self.assertEqual(result, expected_results[index])

    def test_modify_attribute_in_structure_by_path_nested_list(self):
        test_structure = ["a", ["b", "c"], "d", ["e", ["f"]], "g"]
        test_parameter_paths = [[0], [1, 0], [1, 1], [2], [3, 0], [3, 1, 0], [4]]

        expected_results = [
            ["nice_one!", ["b", "c"], "d", ["e", ["f"]], "g"],
            ["a", ["nice_one!", "c"], "d", ["e", ["f"]], "g"],
            ["a", ["b", "nice_one!"], "d", ["e", ["f"]], "g"],
            ["a", ["b", "c"], "nice_one!", ["e", ["f"]], "g"],
            ["a", ["b", "c"], "d", ["nice_one!", ["f"]], "g"],
            ["a", ["b", "c"], "d", ["e", ["nice_one!"]], "g"],
            ["a", ["b", "c"], "d", ["e", ["f"]], "nice_one!"],
        ]

        for index, path in enumerate(test_parameter_paths):
            result = self.injector.modify_attribute_in_structure_by_path(
                structure=test_structure, path=path, value_to_inject="nice_one!"
            )

            self.assertEqual(result, expected_results[index])

    def test_modify_attribute_in_structure_by_path_nested_dict(self):
        test_structure = {
            "user_id": "AAAAA",
            "address": {
                "flat": "BBBBB",
                "parent": {
                    "child": {
                        "child_attribute_1": "AAA",
                        "child_attribute_2": "BBB",
                        "child_attribute_3": "CCC",
                    }
                },
                "street": {"number": "CCCCCC", "zone": "DDDDDD"},
                "country": "EEEEE",
            },
        }

        test_parameter_paths = [
            ["user_id"],
            ["address", "flat"],
            ["address", "parent", "child", "child_attribute_1"],
            ["address", "parent", "child", "child_attribute_2"],
            ["address", "parent", "child", "child_attribute_3"],
            ["address", "street", "number"],
            ["address", "street", "zone"],
            ["address", "country"],
        ]

        expected_results = [
            {
                "user_id": "nice_one!",
                "address": {
                    "flat": "BBBBB",
                    "parent": {
                        "child": {
                            "child_attribute_1": "AAA",
                            "child_attribute_2": "BBB",
                            "child_attribute_3": "CCC",
                        }
                    },
                    "street": {"number": "CCCCCC", "zone": "DDDDDD"},
                    "country": "EEEEE",
                },
            },
            {
                "user_id": "AAAAA",
                "address": {
                    "flat": "nice_one!",
                    "parent": {
                        "child": {
                            "child_attribute_1": "AAA",
                            "child_attribute_2": "BBB",
                            "child_attribute_3": "CCC",
                        }
                    },
                    "street": {"number": "CCCCCC", "zone": "DDDDDD"},
                    "country": "EEEEE",
                },
            },
            {
                "user_id": "AAAAA",
                "address": {
                    "flat": "BBBBB",
                    "parent": {
                        "child": {
                            "child_attribute_1": "nice_one!",
                            "child_attribute_2": "BBB",
                            "child_attribute_3": "CCC",
                        }
                    },
                    "street": {"number": "CCCCCC", "zone": "DDDDDD"},
                    "country": "EEEEE",
                },
            },
            {
                "user_id": "AAAAA",
                "address": {
                    "flat": "BBBBB",
                    "parent": {
                        "child": {
                            "child_attribute_1": "AAA",
                            "child_attribute_2": "nice_one!",
                            "child_attribute_3": "CCC",
                        }
                    },
                    "street": {"number": "CCCCCC", "zone": "DDDDDD"},
                    "country": "EEEEE",
                },
            },
            {
                "user_id": "AAAAA",
                "address": {
                    "flat": "BBBBB",
                    "parent": {
                        "child": {
                            "child_attribute_1": "AAA",
                            "child_attribute_2": "BBB",
                            "child_attribute_3": "nice_one!",
                        }
                    },
                    "street": {"number": "CCCCCC", "zone": "DDDDDD"},
                    "country": "EEEEE",
                },
            },
            {
                "user_id": "AAAAA",
                "address": {
                    "flat": "BBBBB",
                    "parent": {
                        "child": {
                            "child_attribute_1": "AAA",
                            "child_attribute_2": "BBB",
                            "child_attribute_3": "CCC",
                        }
                    },
                    "street": {"number": "nice_one!", "zone": "DDDDDD"},
                    "country": "EEEEE",
                },
            },
            {
                "user_id": "AAAAA",
                "address": {
                    "flat": "BBBBB",
                    "parent": {
                        "child": {
                            "child_attribute_1": "AAA",
                            "child_attribute_2": "BBB",
                            "child_attribute_3": "CCC",
                        }
                    },
                    "street": {"number": "CCCCCC", "zone": "nice_one!"},
                    "country": "EEEEE",
                },
            },
            {
                "user_id": "AAAAA",
                "address": {
                    "flat": "BBBBB",
                    "parent": {
                        "child": {
                            "child_attribute_1": "AAA",
                            "child_attribute_2": "BBB",
                            "child_attribute_3": "CCC",
                        }
                    },
                    "street": {"number": "CCCCCC", "zone": "DDDDDD"},
                    "country": "nice_one!",
                },
            },
        ]

        for index, path in enumerate(test_parameter_paths):
            result = self.injector.modify_attribute_in_structure_by_path(
                structure=test_structure, path=path, value_to_inject="nice_one!"
            )

            self.assertEqual(result, expected_results[index])

    def test_modify_attribute_in_structure_by_path_nested_dict_and_list(self):
        test_structure = {
            "id": "a",
            "address": {"street": "b", "flats": [{"number": 1}, {"number": 2}]},
            "about": {
                "languages": [
                    {"name": "d", "favourite": ["test1", "test2"]},
                    {"name": "e", "favourite": ["test3", "test4"]},
                ],
                "pet": "f",
            },
            "zone": "g",
        }
        test_parameter_paths = [
            ["id"],
            ["address", "street"],
            ["address", "flats", 0, "number"],
            ["address", "flats", 1, "number"],
            ["about", "languages", 0, "name"],
            ["about", "languages", 0, "favourite", 0],
            ["about", "languages", 0, "favourite", 1],
            ["about", "languages", 1, "name"],
            ["about", "languages", 1, "favourite", 0],
            ["about", "languages", 1, "favourite", 1],
            ["about", "pet"],
            ["zone"],
        ]

        expected_results = [
            {
                "id": "nice_one!",
                "address": {"street": "b", "flats": [{"number": 1}, {"number": 2}]},
                "about": {
                    "languages": [
                        {"name": "d", "favourite": ["test1", "test2"]},
                        {"name": "e", "favourite": ["test3", "test4"]},
                    ],
                    "pet": "f",
                },
                "zone": "g",
            },
            {
                "id": "a",
                "address": {
                    "street": "nice_one!",
                    "flats": [{"number": 1}, {"number": 2}],
                },
                "about": {
                    "languages": [
                        {"name": "d", "favourite": ["test1", "test2"]},
                        {"name": "e", "favourite": ["test3", "test4"]},
                    ],
                    "pet": "f",
                },
                "zone": "g",
            },
            {
                "id": "a",
                "address": {
                    "street": "b",
                    "flats": [{"number": "nice_one!"}, {"number": 2}],
                },
                "about": {
                    "languages": [
                        {"name": "d", "favourite": ["test1", "test2"]},
                        {"name": "e", "favourite": ["test3", "test4"]},
                    ],
                    "pet": "f",
                },
                "zone": "g",
            },
            {
                "id": "a",
                "address": {
                    "street": "b",
                    "flats": [{"number": 1}, {"number": "nice_one!"}],
                },
                "about": {
                    "languages": [
                        {"name": "d", "favourite": ["test1", "test2"]},
                        {"name": "e", "favourite": ["test3", "test4"]},
                    ],
                    "pet": "f",
                },
                "zone": "g",
            },
            {
                "id": "a",
                "address": {"street": "b", "flats": [{"number": 1}, {"number": 2}]},
                "about": {
                    "languages": [
                        {"name": "nice_one!", "favourite": ["test1", "test2"]},
                        {"name": "e", "favourite": ["test3", "test4"]},
                    ],
                    "pet": "f",
                },
                "zone": "g",
            },
            {
                "id": "a",
                "address": {"street": "b", "flats": [{"number": 1}, {"number": 2}]},
                "about": {
                    "languages": [
                        {"name": "d", "favourite": ["nice_one!", "test2"]},
                        {"name": "e", "favourite": ["test3", "test4"]},
                    ],
                    "pet": "f",
                },
                "zone": "g",
            },
            {
                "id": "a",
                "address": {"street": "b", "flats": [{"number": 1}, {"number": 2}]},
                "about": {
                    "languages": [
                        {"name": "d", "favourite": ["test1", "nice_one!"]},
                        {"name": "e", "favourite": ["test3", "test4"]},
                    ],
                    "pet": "f",
                },
                "zone": "g",
            },
            {
                "id": "a",
                "address": {"street": "b", "flats": [{"number": 1}, {"number": 2}]},
                "about": {
                    "languages": [
                        {"name": "d", "favourite": ["test1", "test2"]},
                        {"name": "nice_one!", "favourite": ["test3", "test4"]},
                    ],
                    "pet": "f",
                },
                "zone": "g",
            },
            {
                "id": "a",
                "address": {"street": "b", "flats": [{"number": 1}, {"number": 2}]},
                "about": {
                    "languages": [
                        {"name": "d", "favourite": ["test1", "test2"]},
                        {"name": "e", "favourite": ["nice_one!", "test4"]},
                    ],
                    "pet": "f",
                },
                "zone": "g",
            },
            {
                "id": "a",
                "address": {"street": "b", "flats": [{"number": 1}, {"number": 2}]},
                "about": {
                    "languages": [
                        {"name": "d", "favourite": ["test1", "test2"]},
                        {"name": "e", "favourite": ["test3", "nice_one!"]},
                    ],
                    "pet": "f",
                },
                "zone": "g",
            },
            {
                "id": "a",
                "address": {"street": "b", "flats": [{"number": 1}, {"number": 2}]},
                "about": {
                    "languages": [
                        {"name": "d", "favourite": ["test1", "test2"]},
                        {"name": "e", "favourite": ["test3", "test4"]},
                    ],
                    "pet": "nice_one!",
                },
                "zone": "g",
            },
            {
                "id": "a",
                "address": {"street": "b", "flats": [{"number": 1}, {"number": 2}]},
                "about": {
                    "languages": [
                        {"name": "d", "favourite": ["test1", "test2"]},
                        {"name": "e", "favourite": ["test3", "test4"]},
                    ],
                    "pet": "f",
                },
                "zone": "nice_one!",
            },
        ]

        for index, path in enumerate(test_parameter_paths):
            result = self.injector.modify_attribute_in_structure_by_path(
                structure=test_structure, path=path, value_to_inject="nice_one!"
            )

            self.assertEqual(result, expected_results[index])

    def test_generate_structure_payloads_by_path_simple_dict(self):
        test_structure = {"user_id": "AAAAA", "address": "AAAAA"}
        test_parameter_paths = [["user_id"], ["address"]]

        expected_results = [[], []]

        for index, path in enumerate(test_parameter_paths):
            result = self.injector.generate_structure_payloads_by_path(
                structure=test_structure, path=path, value_to_inject="nice_one!"
            )

            self.assertEqual(result, expected_results[index])

    def test_generate_structure_payloads_by_path_nested_dict(self):
        test_structure = {
            "top_level": "top",
            "nested_top": {"middle_level": "test"},
            "list_top": [{"name": {"type": "test"}}],
        }
        test_parameter_paths = [
            ["top_level"],
            ["nested_top", "middle_level"],
            ["list_top", 0, "name", "type"],
        ]

        expected_results = [
            [],
            [
                {
                    "top_level": "top",
                    "nested_top": "nice_one!",
                    "list_top": [{"name": {"type": "test"}}],
                }
            ],
            [
                {
                    "top_level": "top",
                    "nested_top": {"middle_level": "test"},
                    "list_top": [{"name": "nice_one!"}],
                },
                {
                    "top_level": "top",
                    "nested_top": {"middle_level": "test"},
                    "list_top": ["nice_one!"],
                },
                {
                    "top_level": "top",
                    "nested_top": {"middle_level": "test"},
                    "list_top": "nice_one!",
                },
            ],
        ]

        for index, path in enumerate(test_parameter_paths):
            result = self.injector.generate_structure_payloads_by_path(
                structure=test_structure, path=path, value_to_inject="nice_one!"
            )

            self.assertEqual(result, expected_results[index])

    def test_generate_structure_payloads_by_path_list_of_dict(self):
        test_structure = {
            "primitive": "string",
            "nested_dict": {"dict": "string"},
            "list_of_dicts": [
                {"config": {"name": "config1", "value": "value1"}},
                {"config": {"name": "config2", "value": "value2"}},
            ],
        }
        test_parameter_paths = [
            ["primitive"],
            ["nested_dict", "dict"],
            ["list_of_dicts", 0, "config", "name"],
            ["list_of_dicts", 0, "config", "value"],
            ["list_of_dicts", 1, "config", "name"],
            ["list_of_dicts", 1, "config", "value"],
        ]

        expected_results = [
            [],
            [
                {
                    "primitive": "string",
                    "nested_dict": "nice_one!",
                    "list_of_dicts": [
                        {"config": {"name": "config1", "value": "value1"}},
                        {"config": {"name": "config2", "value": "value2"}},
                    ],
                }
            ],
            [
                {
                    "primitive": "string",
                    "nested_dict": {"dict": "string"},
                    "list_of_dicts": [
                        {"config": "nice_one!"},
                        {"config": {"name": "config2", "value": "value2"}},
                    ],
                },
                {
                    "primitive": "string",
                    "nested_dict": {"dict": "string"},
                    "list_of_dicts": [
                        "nice_one!",
                        {"config": {"name": "config2", "value": "value2"}},
                    ],
                },
                {
                    "primitive": "string",
                    "nested_dict": {"dict": "string"},
                    "list_of_dicts": "nice_one!",
                },
            ],
            [
                {
                    "primitive": "string",
                    "nested_dict": {"dict": "string"},
                    "list_of_dicts": [
                        {"config": "nice_one!"},
                        {"config": {"name": "config2", "value": "value2"}},
                    ],
                },
                {
                    "primitive": "string",
                    "nested_dict": {"dict": "string"},
                    "list_of_dicts": [
                        "nice_one!",
                        {"config": {"name": "config2", "value": "value2"}},
                    ],
                },
                {
                    "primitive": "string",
                    "nested_dict": {"dict": "string"},
                    "list_of_dicts": "nice_one!",
                },
            ],
            [
                {
                    "primitive": "string",
                    "nested_dict": {"dict": "string"},
                    "list_of_dicts": [
                        {"config": {"name": "config1", "value": "value1"}},
                        {"config": "nice_one!"},
                    ],
                },
                {
                    "primitive": "string",
                    "nested_dict": {"dict": "string"},
                    "list_of_dicts": [
                        {"config": {"name": "config1", "value": "value1"}},
                        "nice_one!",
                    ],
                },
                {
                    "primitive": "string",
                    "nested_dict": {"dict": "string"},
                    "list_of_dicts": "nice_one!",
                },
            ],
            [
                {
                    "primitive": "string",
                    "nested_dict": {"dict": "string"},
                    "list_of_dicts": [
                        {"config": {"name": "config1", "value": "value1"}},
                        {"config": "nice_one!"},
                    ],
                },
                {
                    "primitive": "string",
                    "nested_dict": {"dict": "string"},
                    "list_of_dicts": [
                        {"config": {"name": "config1", "value": "value1"}},
                        "nice_one!",
                    ],
                },
                {
                    "primitive": "string",
                    "nested_dict": {"dict": "string"},
                    "list_of_dicts": "nice_one!",
                },
            ],
        ]

        for index, path in enumerate(test_parameter_paths):
            result = self.injector.generate_structure_payloads_by_path(
                structure=test_structure, path=path, value_to_inject="nice_one!"
            )

            self.assertEqual(result, expected_results[index])

    def test_generate_structure_payloads_by_path_nested_list(self):
        test_structure = [[[[["edge_case"]]]]]
        test_parameter_paths = [[0, 0, 0, 0, 0]]

        expected_results = [
            [[[[["nice_one!"]]]], [[["nice_one!"]]], [["nice_one!"]], ["nice_one!"]]
        ]

        for index, path in enumerate(test_parameter_paths):
            result = self.injector.generate_structure_payloads_by_path(
                structure=test_structure, path=path, value_to_inject="nice_one!"
            )

            self.assertEqual(result, expected_results[index])

    def test_remove_attribute_in_structure_by_path_simple(self):
        test_structure = {"user_id": "AAAAA", "address": "AAAAA"}
        test_parameter_paths = [["user_id"], ["address"]]

        expected_results = [{"address": "AAAAA"}, {"user_id": "AAAAA"}]

        for index, path in enumerate(test_parameter_paths):
            result = self.injector.remove_attribute_in_structure_by_path(
                structure=test_structure, path=path
            )

            self.assertEqual(result, expected_results[index])

    def test_remove_attribute_in_structure_by_path_list(self):
        test_structure = {
            "list_top": [
                1,
                2,
                3,
            ],
        }
        test_parameter_paths = [["list_top", 0], ["list_top", 1], ["list_top", 2]]

        expected_results = [
            {"list_top": [2, 3]},
            {"list_top": [1, 3]},
            {"list_top": [1, 2]},
        ]

        for index, path in enumerate(test_parameter_paths):
            result = self.injector.remove_attribute_in_structure_by_path(
                structure=test_structure, path=path
            )

            self.assertEqual(result, expected_results[index])

    def test_remove_attribute_in_structure_by_path_complex(self):
        test_structure = {
            "name": "AAAA",
            "list_top": [
                {"type": "BBBB", "priority": "high"},
                {"type": "CCCC", "priority": "Medium"},
            ],
            "data": [1, 2, 3],
        }
        test_parameter_paths = [
            ["name"],
            ["list_top", 0, "type"],
            ["list_top", 0, "priority"],
            ["list_top", 1, "type"],
            ["list_top", 1, "priority"],
            ["data", 0],
            ["data", 1],
            ["data", 2],
        ]

        expected_results = [
            {
                "list_top": [
                    {"type": "BBBB", "priority": "high"},
                    {"type": "CCCC", "priority": "Medium"},
                ],
                "data": [1, 2, 3],
            },
            {
                "name": "AAAA",
                "list_top": [
                    {"priority": "high"},
                    {"type": "CCCC", "priority": "Medium"},
                ],
                "data": [1, 2, 3],
            },
            {
                "name": "AAAA",
                "list_top": [{"type": "BBBB"}, {"type": "CCCC", "priority": "Medium"}],
                "data": [1, 2, 3],
            },
            {
                "name": "AAAA",
                "list_top": [
                    {"type": "BBBB", "priority": "high"},
                    {"priority": "Medium"},
                ],
                "data": [1, 2, 3],
            },
            {
                "name": "AAAA",
                "list_top": [{"type": "BBBB", "priority": "high"}, {"type": "CCCC"}],
                "data": [1, 2, 3],
            },
            {
                "name": "AAAA",
                "list_top": [
                    {"type": "BBBB", "priority": "high"},
                    {"type": "CCCC", "priority": "Medium"},
                ],
                "data": [2, 3],
            },
            {
                "name": "AAAA",
                "list_top": [
                    {"type": "BBBB", "priority": "high"},
                    {"type": "CCCC", "priority": "Medium"},
                ],
                "data": [1, 3],
            },
            {
                "name": "AAAA",
                "list_top": [
                    {"type": "BBBB", "priority": "high"},
                    {"type": "CCCC", "priority": "Medium"},
                ],
                "data": [1, 2],
            },
        ]

        for index, path in enumerate(test_parameter_paths):
            result = self.injector.remove_attribute_in_structure_by_path(
                structure=test_structure, path=path
            )

            self.assertEqual(result, expected_results[index])

    def test_remove_attribute_in_structure_by_path_edge_case(self):
        test_structure = [[[[[[{"my": ["worst", "nightmare"]}]]]]]]
        test_parameter_paths = [
            [0, 0, 0, 0, 0, 0, "my", 0],
            [0, 0, 0, 0, 0, 0, "my", 1],
        ]

        expected_results = [
            [[[[[[{"my": ["nightmare"]}]]]]]],
            [[[[[[{"my": ["worst"]}]]]]]],
        ]

        for index, path in enumerate(test_parameter_paths):
            result = self.injector.remove_attribute_in_structure_by_path(
                structure=test_structure, path=path
            )

            self.assertEqual(result, expected_results[index])

    def test_generate_missing_attribute_permutations_for_structure_by_path_simple(self):
        test_structure = {"user_id": "AAAAA", "address": "AAAAA"}
        test_parameter_paths = [["user_id"], ["address"]]

        expected_results = [[{"address": "AAAAA"}], [{"user_id": "AAAAA"}]]

        for index, path in enumerate(test_parameter_paths):
            result = self.injector.generate_missing_attribute_permutations_for_structure_by_path(
                structure=test_structure, path=path
            )

            self.assertEqual(result, expected_results[index])

    def test_generate_missing_attribute_permutations_for_structure_by_path_complex(
        self,
    ):
        test_structure = {
            "name": "AAAA",
            "list_top": [
                {"type": "BBBB", "priority": "high"},
                {"type": "CCCC", "priority": "Medium"},
            ],
            "data": [1, 2, 3],
        }
        test_parameter_paths = [
            ["name"],
            ["list_top", 0, "type"],
            ["list_top", 0, "priority"],
            ["list_top", 1, "type"],
            ["list_top", 1, "priority"],
            ["data", 0],
            ["data", 1],
            ["data", 2],
        ]

        expected_results = [
            [
                {
                    "list_top": [
                        {"type": "BBBB", "priority": "high"},
                        {"type": "CCCC", "priority": "Medium"},
                    ],
                    "data": [1, 2, 3],
                }
            ],
            [
                {"name": "AAAA", "data": [1, 2, 3]},
                {
                    "name": "AAAA",
                    "list_top": [{"type": "CCCC", "priority": "Medium"}],
                    "data": [1, 2, 3],
                },
                {
                    "name": "AAAA",
                    "list_top": [
                        {"priority": "high"},
                        {"type": "CCCC", "priority": "Medium"},
                    ],
                    "data": [1, 2, 3],
                },
            ],
            [
                {"name": "AAAA", "data": [1, 2, 3]},
                {
                    "name": "AAAA",
                    "list_top": [{"type": "CCCC", "priority": "Medium"}],
                    "data": [1, 2, 3],
                },
                {
                    "name": "AAAA",
                    "list_top": [
                        {"type": "BBBB"},
                        {"type": "CCCC", "priority": "Medium"},
                    ],
                    "data": [1, 2, 3],
                },
            ],
            [
                {"name": "AAAA", "data": [1, 2, 3]},
                {
                    "name": "AAAA",
                    "list_top": [{"type": "BBBB", "priority": "high"}],
                    "data": [1, 2, 3],
                },
                {
                    "name": "AAAA",
                    "list_top": [
                        {"type": "BBBB", "priority": "high"},
                        {"priority": "Medium"},
                    ],
                    "data": [1, 2, 3],
                },
            ],
            [
                {"name": "AAAA", "data": [1, 2, 3]},
                {
                    "name": "AAAA",
                    "list_top": [{"type": "BBBB", "priority": "high"}],
                    "data": [1, 2, 3],
                },
                {
                    "name": "AAAA",
                    "list_top": [
                        {"type": "BBBB", "priority": "high"},
                        {"type": "CCCC"},
                    ],
                    "data": [1, 2, 3],
                },
            ],
            [
                {
                    "name": "AAAA",
                    "list_top": [
                        {"type": "BBBB", "priority": "high"},
                        {"type": "CCCC", "priority": "Medium"},
                    ],
                },
                {
                    "name": "AAAA",
                    "list_top": [
                        {"type": "BBBB", "priority": "high"},
                        {"type": "CCCC", "priority": "Medium"},
                    ],
                    "data": [2, 3],
                },
            ],
            [
                {
                    "name": "AAAA",
                    "list_top": [
                        {"type": "BBBB", "priority": "high"},
                        {"type": "CCCC", "priority": "Medium"},
                    ],
                },
                {
                    "name": "AAAA",
                    "list_top": [
                        {"type": "BBBB", "priority": "high"},
                        {"type": "CCCC", "priority": "Medium"},
                    ],
                    "data": [1, 3],
                },
            ],
            [
                {
                    "name": "AAAA",
                    "list_top": [
                        {"type": "BBBB", "priority": "high"},
                        {"type": "CCCC", "priority": "Medium"},
                    ],
                },
                {
                    "name": "AAAA",
                    "list_top": [
                        {"type": "BBBB", "priority": "high"},
                        {"type": "CCCC", "priority": "Medium"},
                    ],
                    "data": [1, 2],
                },
            ],
        ]

        for index, path in enumerate(test_parameter_paths):
            result = self.injector.generate_missing_attribute_permutations_for_structure_by_path(
                structure=test_structure, path=path
            )

            self.assertEqual(result, expected_results[index])

    def test_generate_missing_attribute_permutations_for_structure_by_path_edge_case(
        self,
    ):
        test_structure = [[[[[[{"my": ["worst", "nightmare"]}]]]]]]
        test_parameter_paths = [
            [0, 0, 0, 0, 0, 0, "my", 0],
            [0, 0, 0, 0, 0, 0, "my", 1],
        ]

        expected_results = [
            [
                [],
                [[]],
                [[[]]],
                [[[[]]]],
                [[[[[]]]]],
                [[[[[[]]]]]],
                [[[[[[{}]]]]]],
                [[[[[[{"my": ["nightmare"]}]]]]]],
            ],
            [
                [],
                [[]],
                [[[]]],
                [[[[]]]],
                [[[[[]]]]],
                [[[[[[]]]]]],
                [[[[[[{}]]]]]],
                [[[[[[{"my": ["worst"]}]]]]]],
            ],
        ]

        for index, path in enumerate(test_parameter_paths):
            result = self.injector.generate_missing_attribute_permutations_for_structure_by_path(
                structure=test_structure, path=path
            )

            self.assertEqual(result, expected_results[index])


if __name__ == "__main__":
    unittest.main()
