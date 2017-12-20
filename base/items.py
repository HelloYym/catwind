from scrapy_djangoitem import DjangoItem

class BaseItem(DjangoItem):
    django_model = None
    update_fields_list = []
    merge_fields_list = []
    unique_key = ()

    def get_uk(self):
        # Return 'None' or valid 'tuple'.
        if not self.unique_key: return None

        values = [self.get(x) for x in self.unique_key if self.get(x) != None]
        if len(values) != len(self.unique_key): return None

        return tuple(values)

    def get_uk_params(self):
        if not self.unique_key or not self.get_uk(): return None

        return dict(zip(self.unique_key, self.get_uk()))

    def get_merge_fields(self, obj):
        mf = []
        for key in self.merge_fields_list:
            if getattr(obj, key) and self.get(key):
                mf.append(key)

        return mf

    def get_update_fields(self, obj):
        uf = []
        for key in self.update_fields_list:
            if not self.get(key): continue
            if getattr(obj, key) and key in self.merge_fields_list: continue
            uf.append(key)

        return uf

    @classmethod
    def get_object_by_pk(cls, pk):
        try:
            obj = cls.django_model.objects.get(pk=pk)
        except cls.django_model.DoesNotExist:
            return None

        return obj

    @classmethod
    def get_object_by_uk(cls, uk):
        if not cls.unique_key: return None

        both = tuple(set(cls.unique_key).intersection(set(uk.keys())))
        if sorted(both) != sorted(cls.unique_key): return None

        for k in uk.keys():
            if k not in both: uk.pop(k)

        try:
            obj = cls.django_model.objects.get(**uk)
        except cls.django_model.DoesNotExist:
            return None

        return obj


