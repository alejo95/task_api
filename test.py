import unittest
import json

from app import db
from app import create_app

from config import config


class TestAPI(unittest.TestCase):
    def setUp(self):
        enviroment = config['test']
        self.app = create_app(enviroment)
        self.client = self.app.test_client()

        self.content_type = 'application/json'
        self.path = 'http://127.0.0.1:5000/api/v1/tasks'
        self.path_first_task = self.path + "/1"

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_get_all_task(self):
        response = self.client.get(path=self.path)
        self.assertEqual(response.status_code, 200)

#    def test_get_first_task(self):
#        response = self.client.get(path=self.path_first_task, content_type=self.content_type)
#
#        self.assertEqual(response.status_code, 200)
#
#        data = json.load(response.data.decode("utf-8"))
#        task_id = data["data"]["id"]
#
#        self.assertEqual(task_id, 1)
#
#    def test_not_found(self):
#        new_path = self.path + '/100'
#        response = self.client.get(path=new_path, content_type=self.content_type)
#
#        self.assertEqual(response.status_code, 404)

    def test_create_task(self):
        data = {
            'title': 'tile',
            'description': 'description',
            'deadline': '2021-05-12 12:00:00'
        }
        response = self.client.post(path=self.path, data=json.dumps(data), content_type=self.content_type)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        task_id = data['data']['id']

        self.assertEqual(task_id, 1)

#    def test_update_task(self):
#        data = {"title": "Nuevo título"}
#
#        response = self.client.get(path=self.path_first_task, content_type=self.content_type, data=json.dumps(data))
#        self.assertEqual(response.status_code, 404)
#
#        data = json.load(response.data.decode("utf-8"))
#        task_id = data["data"]["id"]
#
#       self.assertEqual(task_id, 1)

    def test_delete_task(self):

        response = self.client.delete(path=self.path_first_task, content_type=self.content_type)

        self.assertEqual(response.status_code, 404)

        response = self.client.get(path=self.path_first_task, content_type=self.content_type)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()