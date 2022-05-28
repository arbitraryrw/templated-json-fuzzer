import unittest
from jsonfuzzer.core.fuzzer import Fuzzer


class TestFuzzer(unittest.TestCase):
    def setUp(self) -> None:
        self.fuzzer = Fuzzer()
        return super().setUp()

    def test_generate_structure_permutations_for_payload_duplicate(self) -> None:
        """
        Avoid duplicate payloads test case

        """
        test_structure = {
            "top_level": "top",
            "nested_top": {"middle_level": "test"},
            "list_top": [{"name": {"type": "test"}}, {"name": {"type": "test"}}],
        }

        test_structure_param_paths = [
            ["top_level"],
            ["nested_top", "middle_level"],
            ["list_top", 0, "name", "type"],
            ["list_top", 1, "name", "type"],
        ]

        expected_result = [
            {
                "top_level": "top",
                "nested_top": "manzanas",
                "list_top": [{"name": {"type": "test"}}, {"name": {"type": "test"}}],
            },
            {
                "top_level": "top",
                "nested_top": {"middle_level": "test"},
                "list_top": [{"name": "manzanas"}, {"name": {"type": "test"}}],
            },
            {
                "top_level": "top",
                "nested_top": {"middle_level": "test"},
                "list_top": ["manzanas", {"name": {"type": "test"}}],
            },
            {
                "top_level": "top",
                "nested_top": {"middle_level": "test"},
                "list_top": "manzanas",
            },
            {
                "top_level": "top",
                "nested_top": {"middle_level": "test"},
                "list_top": [{"name": {"type": "test"}}, {"name": "manzanas"}],
            },
            {
                "top_level": "top",
                "nested_top": {"middle_level": "test"},
                "list_top": [{"name": {"type": "test"}}, "manzanas"],
            },
        ]

        result = self.fuzzer.generate_structure_permutations_for_payload(
            structure=test_structure,
            paramater_paths=test_structure_param_paths,
            value_to_inject="manzanas",
        )

        self.assertEqual(result, expected_result)

    def test_generate_structure_permutations_for_payload_duplicate_list(self) -> None:
        """
        Avoid duplicate payloads test case

        _extended_summary_
        """
        test_structure = {
            "top_level": "top",
            "nested_top": {"middle_level": "test"},
            "list_top": [{"name": {"type": "test"}}, {"name": {"type": "test"}}],
        }

        test_structure_param_paths = [
            ["top_level"],
            ["nested_top", "middle_level"],
            ["list_top", 0, "name", "type"],
            ["list_top", 1, "name", "type"],
        ]

        expected_result = [
            {
                "top_level": "top",
                "nested_top": "manzanas",
                "list_top": [{"name": {"type": "test"}}, {"name": {"type": "test"}}],
            },
            {
                "top_level": "top",
                "nested_top": {"middle_level": "test"},
                "list_top": [{"name": "manzanas"}, {"name": {"type": "test"}}],
            },
            {
                "top_level": "top",
                "nested_top": {"middle_level": "test"},
                "list_top": ["manzanas", {"name": {"type": "test"}}],
            },
            {
                "top_level": "top",
                "nested_top": {"middle_level": "test"},
                "list_top": "manzanas",
            },
            {
                "top_level": "top",
                "nested_top": {"middle_level": "test"},
                "list_top": [{"name": {"type": "test"}}, {"name": "manzanas"}],
            },
            {
                "top_level": "top",
                "nested_top": {"middle_level": "test"},
                "list_top": [{"name": {"type": "test"}}, "manzanas"],
            },
        ]

        result = self.fuzzer.generate_structure_permutations_for_payload(
            structure=test_structure,
            paramater_paths=test_structure_param_paths,
            value_to_inject="manzanas",
        )

        self.assertEqual(result, expected_result)

    def test_generate_structure_missing_attribute_permutations_simple(self) -> None:
        test_structure = {"user_id": "AAAAA", "address": "AAAAA"}

        test_structure_param_paths = [["user_id"], ["address"]]

        expected_result = [{"address": "AAAAA"}, {"user_id": "AAAAA"}]

        result = self.fuzzer.generate_structure_missing_attribute_permutations(
            structure=test_structure,
            paramater_paths=test_structure_param_paths,
        )

        self.assertEqual(result, expected_result)

    def test_generate_structure_missing_attribute_permutations_list(self) -> None:
        test_structure = [[1, 2], [3, 4, 5], [6], 7]

        test_structure_param_paths = [
            [0, 0],
            [0, 1],
            [1, 0],
            [1, 1],
            [1, 2],
            [2, 0],
            [3],
        ]

        expected_result = [
            [[3, 4, 5], [6], 7],
            [[2], [3, 4, 5], [6], 7],
            [[1], [3, 4, 5], [6], 7],
            [[1, 2], [6], 7],
            [[1, 2], [4, 5], [6], 7],
            [[1, 2], [3, 5], [6], 7],
            [[1, 2], [3, 4], [6], 7],
            [[1, 2], [3, 4, 5], 7],
            [[1, 2], [3, 4, 5], [], 7],
            [[1, 2], [3, 4, 5], [6]],
        ]

        result = self.fuzzer.generate_structure_missing_attribute_permutations(
            structure=test_structure,
            paramater_paths=test_structure_param_paths,
        )

        self.assertEqual(result, expected_result)

    def test_generate_structure_missing_attribute_permutations_list_of_dicts(
        self,
    ) -> None:
        test_structure = [
            {"name": "AAAA", "priority": "High"},
            {"name": "BBBB", "priority": "Medium"},
            {"name": "CCCC", "priority": "Low"},
        ]

        test_structure_param_paths = [
            [0, "name"],
            [0, "priority"],
            [1, "name"],
            [1, "priority"],
            [2, "name"],
            [2, "priority"],
        ]

        expected_result = [
            [
                {"name": "BBBB", "priority": "Medium"},
                {"name": "CCCC", "priority": "Low"},
            ],
            [
                {"priority": "High"},
                {"name": "BBBB", "priority": "Medium"},
                {"name": "CCCC", "priority": "Low"},
            ],
            [
                {"name": "AAAA"},
                {"name": "BBBB", "priority": "Medium"},
                {"name": "CCCC", "priority": "Low"},
            ],
            [{"name": "AAAA", "priority": "High"}, {"name": "CCCC", "priority": "Low"}],
            [
                {"name": "AAAA", "priority": "High"},
                {"priority": "Medium"},
                {"name": "CCCC", "priority": "Low"},
            ],
            [
                {"name": "AAAA", "priority": "High"},
                {"name": "BBBB"},
                {"name": "CCCC", "priority": "Low"},
            ],
            [
                {"name": "AAAA", "priority": "High"},
                {"name": "BBBB", "priority": "Medium"},
            ],
            [
                {"name": "AAAA", "priority": "High"},
                {"name": "BBBB", "priority": "Medium"},
                {"priority": "Low"},
            ],
            [
                {"name": "AAAA", "priority": "High"},
                {"name": "BBBB", "priority": "Medium"},
                {"name": "CCCC"},
            ],
        ]

        result = self.fuzzer.generate_structure_missing_attribute_permutations(
            structure=test_structure,
            paramater_paths=test_structure_param_paths,
        )

        self.assertEqual(result, expected_result)

    def test_generate_structure_missing_attribute_permutations_complex(self) -> None:
        test_structure = {
            "name": "AAAA",
            "list_top": [
                {"type": "BBBB", "priority": "high"},
                {"type": "CCCC", "priority": "Medium"},
            ],
            "data": [1, 2, 3],
        }

        test_structure_param_paths = [
            ["name"],
            ["list_top", 0, "type"],
            ["list_top", 0, "priority"],
            ["list_top", 1, "type"],
            ["list_top", 1, "priority"],
            ["data", 0],
            ["data", 1],
            ["data", 2],
        ]

        expected_result = [
            {
                "list_top": [
                    {"type": "BBBB", "priority": "high"},
                    {"type": "CCCC", "priority": "Medium"},
                ],
                "data": [1, 2, 3],
            },
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
            {
                "name": "AAAA",
                "list_top": [{"type": "BBBB"}, {"type": "CCCC", "priority": "Medium"}],
                "data": [1, 2, 3],
            },
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

        result = self.fuzzer.generate_structure_missing_attribute_permutations(
            structure=test_structure,
            paramater_paths=test_structure_param_paths,
        )

        self.assertEqual(result, expected_result)

    def test_generate_structure_missing_attribute_permutations_edge_case(self) -> None:
        test_structure = [[[[[[{"my": ["worst", "nightmare"]}]]]]]]

        expected_result = [
            [],
            [[]],
            [[[]]],
            [[[[]]]],
            [[[[[]]]]],
            [[[[[[]]]]]],
            [[[[[[{}]]]]]],
            [[[[[[{"my": ["nightmare"]}]]]]]],
            [[[[[[{"my": ["worst"]}]]]]]],
        ]

        test_structure_param_paths = [
            [0, 0, 0, 0, 0, 0, "my", 0],
            [0, 0, 0, 0, 0, 0, "my", 1],
        ]

        result = self.fuzzer.generate_structure_missing_attribute_permutations(
            structure=test_structure,
            paramater_paths=test_structure_param_paths,
        )

        self.assertEqual(result, expected_result)
