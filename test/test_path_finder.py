import unittest
from jsonfuzzer.parser.path_finder import PathFinder


class TestPathFinder(unittest.TestCase):
    def setUp(self) -> None:
        self.path_finder = PathFinder()
        return super().setUp()

    def test_map_structure_simple_primitive(self):
        test_structure = {"a": "a"}
        expected_result = [["a"]]

        result = self.path_finder.map_structure(structure=test_structure)
        self.assertEqual(result, expected_result)

    def test_map_structure_simple_list(self):
        test_structure = {"a": ["b", "c"]}
        expected_result = [["a", 0], ["a", 1]]

        result = self.path_finder.map_structure(structure=test_structure)
        self.assertEqual(result, expected_result)

    def test_map_structure_simple_dict(self):
        test_structure = {"a": {"b": "b"}}
        expected_result = [["a", "b"]]

        result = self.path_finder.map_structure(structure=test_structure)
        self.assertEqual(result, expected_result)

    def test_map_structure_nested_dict(self):
        test_structure = {
            "a": {"b": {"c": {"d": {"e": "e"}, "f": "f"}, "g": "g"}, "h": "h", "i": "i"}
        }
        expected_result = [
            ["a", "b", "c", "d", "e"],
            ["a", "b", "c", "f"],
            ["a", "b", "g"],
            ["a", "h"],
            ["a", "i"],
        ]

        result = self.path_finder.map_structure(structure=test_structure)
        self.assertEqual(result, expected_result)

    def test_map_structure_nested_list(self):
        test_structure = {"a": ["b", ["c", ["d"], "e"], "f"]}
        expected_result = [["a", 0], ["a", 1, 0], ["a", 1, 1, 0], ["a", 1, 2], ["a", 2]]

        result = self.path_finder.map_structure(structure=test_structure)
        self.assertEqual(result, expected_result)

    def test_map_structure_list_of_dict(self):
        test_structure = {
            "id": "123",
            "data": {
                "colour": "red",
                "activity": [
                    {"name": "climbing", "priority": "high"},
                    {"name": "lounging", "priority": "medium"},
                    {"name": "running", "priority": "low"},
                ],
                "greeting": "updog",
            },
            "active": True,
        }
        expected_result = [
            ["id"],
            ["data", "colour"],
            ["data", "activity", 0, "name"],
            ["data", "activity", 0, "priority"],
            ["data", "activity", 1, "name"],
            ["data", "activity", 1, "priority"],
            ["data", "activity", 2, "name"],
            ["data", "activity", 2, "priority"],
            ["data", "greeting"],
            ["active"],
        ]

        result = self.path_finder.map_structure(structure=test_structure)
        self.assertEqual(result, expected_result)

    def test_map_structure_complex(self):
        test_structure = {
            "id": "123",
            "greeting": "updog",
            "notifications": [
                {
                    "date": "2022/01/01",
                    "data": [{"name": "mobile_notification", "priority": "high"}],
                },
                {
                    "date": "2022/01/01",
                    "data": [
                        {"name": "desktop_notification1", "priority": "high"},
                        {"name": "desktop_notification2", "priority": "medium"},
                    ],
                },
                {
                    "date": "2022/01/01",
                    "data": [{"name": "desktop_notification", "priority": "high"}],
                },
            ],
        }
        expected_result = [
            ["id"],
            ["greeting"],
            ["notifications", 0, "date"],
            ["notifications", 0, "data", 0, "name"],
            ["notifications", 0, "data", 0, "priority"],
            ["notifications", 1, "date"],
            ["notifications", 1, "data", 0, "name"],
            ["notifications", 1, "data", 0, "priority"],
            ["notifications", 1, "data", 1, "name"],
            ["notifications", 1, "data", 1, "priority"],
            ["notifications", 2, "date"],
            ["notifications", 2, "data", 0, "name"],
            ["notifications", 2, "data", 0, "priority"],
        ]

        result = self.path_finder.map_structure(structure=test_structure)
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
