import pprint
import sys
import urllib2

import anyjson

import resource


class ResourceManager(object):

    def filter(self, **kwargs):
        if self.managed_class.api_returns_map:
            dict_manager = resource.DictManager(self.managed_class)
            return dict_manager.all(**kwargs)
            # a_dict = self.do_request(**kwargs)
            # return self.create_object_from_dict(a_dict)
        else:
            dict_list = self.do_request(**kwargs)
            return self.create_objects_from_dicts(dict_list)

    def get(self, **kwargs):
        a_dict = kwargs.copy()
        result_dict = self.do_request(**kwargs)
        print('*** result_dict = %r' % result_dict)
        a_dict.update(result_dict)
        return self.create_object_from_dict(a_dict)

    def get_url(self, **kwargs):
        uri = self.managed_class.URI

        for key, value in kwargs.items():
            if key == 'pk':
                key = self.managed_class.primary_key_name

            uri = uri.replace(':' + key, str(value))
            
        url = self.managed_class.BASE_URL + uri

        # print('*** url = %s' % url)

        return url

    def do_request(self, **kwargs):
        url = self.get_url(**kwargs)

        try:
            response = urllib2.urlopen(url)
        except urllib2.HTTPError as e:
            print >>sys.stderr, 'HTTPError %r while loading url: %s' % (e, url)
        
        return anyjson.deserialize(response.read())

    def create_objects_from_dicts(self, dict_list):
        objs = []

        for a_dict in dict_list:
            objs.append(self.create_object_from_dict(a_dict))

        return objs

    def create_object_from_dict(self, a_dict):
        return self.managed_class(**a_dict)

    def __init__(self, managed_class):
        self.managed_class = managed_class
