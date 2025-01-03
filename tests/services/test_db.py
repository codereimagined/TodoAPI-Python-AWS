import os
import unittest
from unittest.mock import MagicMock

os.environ['TABLE_NAME'] = 'test_table'
from services import db


class DBTestCase(unittest.TestCase):
    def test_add_new_item(self):
        # Create a mock table instance
        mock_table = MagicMock()

        # Prepare the item data to add
        item_data = {"name": "Test Item", "description": "A test description"}

        # Call the function
        result = db.add_new_item(item_data, mock_table)

        # Assert that put_item was called with the correct item
        self.assertIn("id", item_data)  # Ensure id was added to item_data
        self.assertEqual(result["id"], item_data["id"])  # Check if the id is returned
        mock_table.put_item.assert_called_once_with(Item=item_data)  # Ensure put_item was called

    def test_get_item_by_id_non_existent(self):
        mock_table = MagicMock()

        item = db.get_item_by_id("non-existent", mock_table)

        self.assertIsNone(item)

    def test_get_item_by_id_existent(self):
        mock_table = MagicMock()
        mock_table.get_item.return_value = {"Item": {"id": "existent"}}

        item = db.get_item_by_id("existent", mock_table)

        self.assertIsNotNone(item)
        self.assertEqual(item, {"id": "existent"})

    def test_delete_item_by_id(self):
        mock_table = MagicMock()

        result = db.delete_item_by_id("some_id", mock_table)

        self.assertIsNone(result)

    def test_get_all_items(self):
        mock_table = MagicMock()
        mock_table.scan.return_value = {"Items": [{"id": "existent1"}, {"id": "existent2"}]}

        items = db.get_all_items(mock_table)

        self.assertEqual(len(items), 2)
        mock_table.scan.assert_called_once()


if __name__ == '__main__':
    unittest.main()
