import pprint
import anyjson
import urllib2


class Field(object):
    primary_key = False

    def __init__(self, field_name, primary_key=False):
        self.field_name = field_name
        self.primary_key = primary_key


class IntegerField(Field):
    pass


class TextField(Field):
    pass


class BooleanField(Field):
    pass


class ResourceMetaClass(type):

    def __init__(cls, name, bases, dct):
        super(ResourceMetaClass, cls).__init__(name, bases, dct)

        from resourcemanager import ResourceManager

        cls.objects = ResourceManager(cls)

        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)

            if isinstance(attr, Field):
                # print('Class %s has Field: %s' % (cls, attr_name))
                attr.attr_name = attr_name
                cls.fields[attr.field_name] = attr
                # print(cls.fields)

            if getattr(attr, 'primary_key', False):
                cls.primary_key_name = attr_name


class Resource(object):

    __metaclass__ = ResourceMetaClass
    primary_key_name = None
    BASE_URL = 'https://crapi.test.cheggnet.com:1448'

    fields = {}
    api_returns_map = False

    def __init__(self, **kwargs):
        a_dict = {}

        # Translate API key names to Python key names
        for key, value in kwargs.items():
            if key in self.fields:
                key = self.fields[key].attr_name

            a_dict[key] = value

        self.__dict__.update(a_dict)
        self.monkey_patch_associations()

        if self.primary_key_name and hasattr(self, self.primary_key_name):
            self.pk = getattr(self, self.primary_key_name)

    def monkey_patch_associations(self):
        for attr_name in dir(self):
            # print('*** attr_name = %s' % attr_name)
            attr = getattr(self, attr_name)

            if isinstance(attr, ZeroOrMore):
                # print('*** monkey_patch_associations: %s is a ZeroOrMore' % (attr_name))
                setattr(attr, 'owner', self)

    def __str__(self):
        a_dict = self.__dict__.copy()
        a_dict['__class__'] = self.__class__
        return pprint.pformat(a_dict)

    def __repr__(self):
        return str(self)


class ZeroOrMore(object):

    def __init__(self, managed_class):
        # self.owner_class = owner_class
        self.managed_class = managed_class

    def all(self):
        # print('*** pk = %s' % self.owner.pk)

        kwargs = {}
        kwargs[self.owner.__class__.primary_key_name] = self.owner.pk

        return self.managed_class.objects.filter(**kwargs)

    def get(self):
        # print('*** pk = %s' % self.owner.pk)

        kwargs = {}
        kwargs[self.owner.__class__.primary_key_name] = self.owner.pk

        return self.managed_class.objects.get(**kwargs)


class DictManager(ZeroOrMore):

    class ResourceDict(Resource, dict):
    
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                self[key] = value

    def __init__(self, managed_class):
        # self.owner_class = owner_class
        self.managed_class = managed_class
        self.ResourceDict.URI = managed_class.URI

    def all(self, **kwargs):
        # print('*** pk = %s' % self.owner.pk)

        if kwargs is None:
            kwargs = {}

        kwargs = kwargs.copy()

        if hasattr(self, 'owner'):
            kwargs[self.owner.__class__.primary_key_name] = self.owner.pk

        # items_dict = self.managed_class.objects.get(**kwargs)
        items_dict = self.ResourceDict.objects.get(**kwargs)

        objs = []

        for key, value in items_dict.items():
            # print('value = %r' % value)
            obj = self.managed_class.objects.create_object_from_dict(value)
            objs.append(obj)

        return objs
