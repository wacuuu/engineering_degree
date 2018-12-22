from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class_list = ["main"]


class main(Model):
    product_type = columns.Ascii(primary_key=True)
    date = columns.Date(primary_key=True)
    product_id = columns.Ascii(primary_key=True)
    parameters = columns.Map(columns.Ascii(),
                             columns.Map(columns.Ascii(),
                                         columns.Ascii()))
