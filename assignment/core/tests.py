from django.test import TestCase
from core.solutions import Rectangle

class RectangleTests(TestCase):
    """
    Automated tests to verify the custom Rectangle class behaves 
    exactly as requested in the assignment requirements.
    """
    
    def setUp(self):
        self.rect = Rectangle(length=10, width=5)
        
    def test_initialization(self):
        """Test that the class initializes with length and width."""
        self.assertEqual(self.rect.length, 10)
        self.assertEqual(self.rect.width, 5)
        
    def test_is_iterable(self):
        """Test that the class can be iterated over."""
        # The iter() function will raise a TypeError if the object is not iterable
        iter_obj = iter(self.rect)
        self.assertIsNotNone(iter_obj)

    def test_iteration_output_format(self):
        """Test that iteration yields the exact required dictionary formats."""
        result = list(self.rect)
        expected_output = [{'length': 10}, {'width': 5}]
        self.assertEqual(result, expected_output)