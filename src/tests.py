from server import *
import unittest
import json

class ServerTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    # load index
    def test_html_index(self):
        rv = self.app.get('/')
        assert rv.status_code == 200
        assert rv.mimetype == 'text/html'
 
    # get all food trucks (currently 518 in db)
    def test_get_all(self):
        rv = self.app.get('/api/foodtrucks')
        data = json.loads(rv.data)
        assert rv.status_code == 200
        assert len(data) == 518

    # get food truck with known id
    def test_get_by_id_1(self):
        rv = self.app.get('/api/foodtrucks/1')
        data = json.loads(rv.data)
        assert rv.status_code == 200
        assert rv.mimetype == 'application/json'
        assert data['name'] == 'Cheese Gone Wild'

    # get food truck with known id
    def test_get_by_id_2(self):
        rv = self.app.get('/api/foodtrucks/2')
        data = json.loads(rv.data)
        assert rv.status_code == 200
        assert rv.mimetype == 'application/json'
        assert data['name'] == 'Mini Mobile Food Catering'

    # get food truck with out of bounds id
    def test_get_by_id_3(self):
        rv = self.app.get('/api/foodtrucks/10000')
        data = json.loads(rv.data)
        assert rv.status_code == 200
        assert rv.mimetype == 'application/json'
        assert len(data) == 0

    # 20 food trucks within 3 km of known geolocation in SF
    def test_get_by_lat_1(self):
        rv = self.app.get('/api/foodtrucks?latitude=37.7715637663341&longitude=-122.418801505439')
        data = json.loads(rv.data)
        assert rv.status_code == 200
        assert rv.mimetype == 'application/json'
        assert len(data) > 0
        assert len(data) <= 20
        assert data[0]['name'] == 'Smokin Warehouse Barbecue'

    # 20 food trucks within 3 km of foreign geolocation (should be zero)
    def test_get_by_lat_2(self):
        rv = self.app.get('/api/foodtrucks?latitude=100&longitude=100')
        data = json.loads(rv.data)
        assert rv.status_code == 200
        assert rv.mimetype == 'application/json'
        assert len(data) == 0

    # invalid type for latitude
    def test_get_by_lat_3(self):
        rv = self.app.get('/api/foodtrucks?latitude=chicago')
        data = json.loads(rv.data)
        assert rv.status_code == 400
        assert rv.mimetype == 'application/json'
        assert data['message'] == 'could not convert string to float: chicago'

    # incomplete parameter list returns all food trucks
    def test_get_by_lat_4(self):
        rv = self.app.get('/api/foodtrucks?latitude=37.7715637663341')
        data = json.loads(rv.data)
        assert rv.status_code == 200
        assert rv.mimetype == 'application/json'
        assert len(data) == 518

    # 20 food trucks within 3 km of Austin (should be zero)
    def test_get_by_address_1(self):
        rv = self.app.get('/api/foodtrucks?address=austin')
        data = json.loads(rv.data)
        assert rv.status_code == 200
        assert rv.mimetype == 'application/json'
        assert len(data) == 0

    # 20 food trucks within 3 km of the heart of SF
    def test_get_by_address_2(self):
        rv = self.app.get('/api/foodtrucks?address=san+francisco')
        data = json.loads(rv.data)
        assert rv.status_code == 200
        assert rv.mimetype == 'application/json'
        assert len(data) > 0
        assert len(data) <= 20
        assert data[0]['name'] == 'John\'s Catering #5'

if __name__ == '__main__':
    unittest.main()
