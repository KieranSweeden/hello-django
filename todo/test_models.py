from django.test import TestCase
from .models import Item

# To test this particular file
# Run: python3 manage.py test todo.test_models

# Inherits from testcase class
class TestModels(TestCase):

    def test_done_defaults_to_false(self):
        """
        This test makes sure that newly created items
        Have their done status set to False by default
        """

        # Create a new item
        item = Item.objects.create(name="Test Todo Item")

        # Check item's done status is set to
        # False by default
        self.assertFalse(item.done)
    
    def test_item_string_method_returns_name(self):
        """
        We haven't tested the string method (__str__) of our item model
        """

        # Create a new item
        item = Item.objects.create(name="Test Todo Item")

        # Test that the name returned, is the string we passed in
        self.assertEqual(str(item), "Test Todo Item")
