import sys, os
from urllib import urlencode
from flask_testing import TestCase
from flask import url_for, request
import unittest
import json

project_home = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from myads_service import app            
from myads_service.models import db, Query, Institute, Library

class TestSite(TestCase):
    '''Tests that each route is an http response'''
    
    def create_app(self):
        '''Start the wsgi application'''
        a = app.create_app(**{
               'SQLALCHEMY_BINDS': {'myads': 'sqlite:///'},
               'SQLALCHEMY_ECHO': True,
               'TESTING': True,
               'PROPAGATE_EXCEPTIONS': True,
               'TRAP_BAD_REQUEST_ERRORS': True,
               'MYADS_BUMBLEBEE_OPTIONS': {'foo': 'bar'}
            })
        db.create_all(app=a, bind=['myads'])
        return a


    def test_store_data(self):
        '''Tests the ability to query site config'''
        
        r = self.client.get(url_for('bumblebee.configuration'),
                content_type='application/json')
        self.assertStatus(r, 200)
        self.assert_(r.json == {'foo': 'bar'}, 'missing json response')
        
        r = self.client.get(url_for('bumblebee.configuration') + '/foo',
                content_type='application/json')
        self.assertStatus(r, 200)
        self.assert_(r.json == 'bar', 'missing json response')
        
        r = self.client.get(url_for('bumblebee.configuration') + '/foox',
                content_type='application/json')
        self.assertStatus(r, 404)

class TestOpenURL(TestCase):
    '''Tests that each route is an http response'''
    
    def create_app(self):
        '''Start the wsgi application'''
        a = app.create_app(**{
               'SQLALCHEMY_BINDS': {'myads': 'sqlite:///', 'institutes': 'sqlite:///'},
               'SQLALCHEMY_ECHO': True,
               'TESTING': True,
               'PROPAGATE_EXCEPTIONS': True,
               'TRAP_BAD_REQUEST_ERRORS': True,
               'MYADS_BUMBLEBEE_OPTIONS': {'foo': 'bar'}
            })
        db.create_all(app=a, bind=['institutes'])
        return a
    
    def setUp(self):
        # Add a stub insitute
        self.institute = Institute(id=0,
            canonical_name='Name',
            city='City',
            street='Street',
            state='State',
            country='Country',
            ringgold_id=0,
            ads_id='X')
        db.session.add(self.institute)
        db.session.commit()
        # and a stub library server
        self.library = Library(id=0,
            libserver='server',
            iconurl='icon',
            libname='name',
            institute=0)
        db.session.add(self.library)
        db.session.commit()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def test_openurl_data(self):
        '''Tests the ability to retrieve OpenURL server data'''
        
        r = self.client.get(url_for('bumblebee.configuration') + '/link_servers',
                content_type='application/json')
        self.assertStatus(r, 200)
        expected = [{"name": "name", "link": "server", "gif":"icon"}]
        self.assertEqual(r.json, expected)
        
if __name__ == '__main__':
    unittest.main()
