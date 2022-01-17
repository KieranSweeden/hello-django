from django.test import TestCase
from .models import Item

# Create your tests here.


# To test full file, run the command: python3 manage.py test todo.test_views

# To test the full app (maybe you have multiple tests in different files)
# use python3 manage.py test


# Inherits from testcase class
class TestViews(TestCase):
    """
    Contains various functions for testing our views in
    making sure they're returning successful HTTP responses,
    using the proper templates and carrying out their
    functionalities properly. In this case, those
    functionalities includes toggling & deleting items.
    """

    def test_get_todo_list(self):
        """
        Test for retreiving the todo list (home page)
        """
        # Store the response
        response = self.client.get("/")

        # A successful response provides a status code of 200
        # If 200, it was successful
        self.assertEqual(response.status_code, 200)

        # To confirm the view is the correct one, use
        # self.assertTemplateUsed and within it's 2nd
        # parameter, tell it what view is expected
        self.assertTemplateUsed(response, "todo/todo_list.html")


    def test_get_add_item(self):
        """
        Test for getting the add_item page
        """
        # Similar to test above however...
        # We need to change the URL & the
        # Template we expect to use
        response = self.client.get("/add")
 
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "todo/add_item.html")

    def test_get_edit_item(self):
        """
        Test for getting the edit_item page
        """
        # Because this URL requires a variable
        # We need to supply it one using the item model
        item = Item.objects.create(name="Test Todo Item")

        # Use id from the test item created
        response = self.client.get(f"/edit/{item.id}")
 
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "todo/edit_item.html")
    

    def test_can_add_item(self):
        """
        Test for adding an item
        """
        # As adding an item requires a post http method
        # We're using a client.post method here
        # We're also providing a name, as if we've just
        # submitted through the item form
        response = self.client.post("/add", { "name": "Test Added Item" })

        # To confirm that we redirect to a particular page
        # we use assertRedirects
        self.assertRedirects(response, "/")


    def test_can_delete_item(self):
        """
        Test for deleting an item
        """
        item = Item.objects.create(name="Test Todo Item")

        # Use id from the test item created
        response = self.client.get(f"/delete/{item.id}")

        # Check the view redirects us as intended
        self.assertRedirects(response, "/")

        # To double check the item is absolutely deleted
        # We'll try to get it, using the filter and the
        # Newly created and most recently delete test item's id 
        existing_items = Item.objects.filter(id=item.id)

        # No items should match as it's been deleted
        # Meaning the newly created array should 
        # have no items remaining, meaning a length of 0
        self.assertEqual(len(existing_items), 0)
    
    def test_can_toggle_item(self):
        """
        Test for toggling an item
        """
        # Create an item with it's done status set to True
        item = Item.objects.create(name="Test Todo Item", done=True)

        # Toggle the done status of the newly created item
        # Using the toggle item view
        response = self.client.get(f"/toggle/{item.id}")
 
        # Double check we've been redirected to correct page
        self.assertRedirects(response, "/")

        # Grab the item again in it's updated state
        updated_item = Item.objects.get(id=item.id)

        # Use assert false to check that the done status
        # Is set to false
        self.assertFalse(updated_item.done)
    

    def test_can_edit_item(self):

        # Create an item
        item = Item.objects.create(name="Test Todo Item", done=True)

        # Test that an update can be posted, passing an update
        response = self.client.post(f"/edit/{item.id}", {"name": "Updated Name"})

         # Double check we've been redirected to correct page
        self.assertRedirects(response, "/")

        # Grab the item again in it's updated state
        updated_item = Item.objects.get(id=item.id)

        self.assertEqual(updated_item.name, "Updated Name")