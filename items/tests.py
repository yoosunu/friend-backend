from rest_framework.test import APITestCase
from .models import Item, Tag
from users.models import User
from category.models import Category

# Create your tests here.


class TestItems(APITestCase):

    TITLE = "item test"
    DESCRIPTION = "item test!"
    URL = "/api/v1/items/"
    NAME = "Jasper"

    def setUp(self):
        user = User.objects.create(name=self.NAME)
        tag = Tag.objects.create(tags="game")
        category = Category.objects.create(kind="item")
        item = Item.objects.create(
            title=self.TITLE,
            description=self.DESCRIPTION,
            category=category,
        )
        item.tags.set([tag])

    # def test_get(self):
    #     response = self.client.get(self.URL)
    #     data = response.json()

    #     self.assertEqual(
    #         response.status_code,
    #         200,
    #         "connection error.",
    #     )
    #     self.assertIsInstance(
    #         data,
    #         list,
    #     )
    #     self.assertEqual(
    #         len(data),
    #         1,
    #     )
    #     self.assertEqual(
    #         data[0]["title"],
    #         self.TITLE,
    #     )
    #     self.assertEqual(
    #         data[0]["description"],
    #         self.DESCRIPTION,
    #     )

    def test_post(self):

        new_item_title = "new one"
        new_description = "new desc"

        response = self.client.post(
            self.URL,
            data={
                "title": new_item_title,
                "description": new_description,
                "category": 1,
            },
        )

        data = response.json()
        print(data)

        # self.assertEqual(
        #     response.status_code,
        #     200,
        #     "connection error",
        # )
        # self.assertEqual(
        #     data[0]["title"],
        #     new_item_title,
        # )
        # self.assertEqual(
        #     data[0]["description"],
        #     new_description,
        # )


class TestItem(APITestCase):

    NAME = "Test item"
    DESCRIPTION = "TEST DESCR"

    def setUp(self):
        Item.objects.create(
            title=self.NAME,
            description=self.DESCRIPTION,
        )

    def test_get(self):
        pass
