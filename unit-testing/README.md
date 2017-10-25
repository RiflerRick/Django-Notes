# Django-Unit-Testing

Django actually helps us to write unit tests in the way that django has its own way of handling tests, we can write the tests that we need to run following the rubrics defined by django and all we need to do is to run the command “./manage.py test”. Doing so will actually run the tests written in the tests.py files in our apps.

For instance if we need to write unit tests in django, follow [this link](https://docs.djangoproject.com/en/1.11/topics/testing/). 

An example of a test module
```python
from django.test import TestCase
from myapp.models import Animal

class AnimalTestCase(TestCase):
    def setUp(self):
        Animal.objects.create(name="lion", sound="roar")
        Animal.objects.create(name="cat", sound="meow")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Animal.objects.get(name="lion")
        cat = Animal.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')
```
The django.test.TestCase is a subclass of unittest.TestCase which is a standard built-in module of python.

Here is an example of running test cases in django

```
# Run all the tests in the animals.tests module
$ ./manage.py test animals.tests

# Run all the tests found within the 'animals' package
$ ./manage.py test animals

# Run just one test case
$ ./manage.py test animals.tests.AnimalTestCase

# Run just one test method
$ ./manage.py test animals.tests.AnimalTestCase.test_animals_can_speak
```



