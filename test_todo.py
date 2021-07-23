import todo_handler
import unittest
import json


class TestCreate(unittest.TestCase):
    """
    Test the create_item function from the todo_handler library
    """

    def test_create_item(self):
        """
        Test that the creation of a an item in the todolist in dynamodb returns a 200 status code and corresponding message.
        """
        title = "haircut"
        task = "book an appointment"
        event = {"body": json.dumps({"title": title, "task": task})}
        result = todo_handler.create_item(event, None)
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['body'], "Your todo item has been inserted successfully! Go " + task + "!")

    def test_invalid_input(self):
        """
        Test that the attempt to create an item without providing valid inputs returns a 400 status code and corresponding message.
        """
        event = {"body": None}
        result = todo_handler.create_item(event, None)
        self.assertEqual(result['statusCode'], 400)
        self.assertEqual(result['body'], "Please provide title and task")


class TestFetch(unittest.TestCase):
    """
    Test the fetch_items function from the todo_handler library
    """

    def test_fetch_all_items(self):
        """
            Test that sending id in the params, you get results with status code 200
        """
        event = {"body": None}
        result = todo_handler.fetch_items(event, None)
        self.assertEqual(result["statusCode"], 200)

    def test_fetch_single_item(self):
        """
            Test that by sending an id in the params, you get the corresponding item with status code 200 and the correct task
        """
        event = {"body": json.dumps({"id": "d6015715-c472-4a92-b0a1-73b9e6d15dd5"})}
        result = todo_handler.fetch_items(event, None)
        result_body = json.loads(result["body"])
        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(result_body[0]["Title"], "plants")
        self.assertEqual(result_body[0]["Task"], "water the plants")


if __name__ == '__main__':
    unittest.main()
