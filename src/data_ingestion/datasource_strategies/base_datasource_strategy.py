
class BaseDatasourceStrategy:
    schema = {}

    @classmethod
    def get_data_schema(cls):
        return cls.schema