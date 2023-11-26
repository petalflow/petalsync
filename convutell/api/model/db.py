from datetime import datetime, time
from mongoengine import (
    Document,
    SequenceField,
    StringField,
    DateTimeField,
    IntField,
    ValidationError,
    ReferenceField,
    connect,
)
import re

from api.config.dbConfig import db

# Definir as classes de documentos
class ConnectionDestination(Document):
    id_connection = SequenceField(primary_key=True, required=True)
    ds_name_connection = StringField(required= True, max_length=100)
    ds_user = StringField(required=True, max_length=50)
    ds_connection = StringField(required=True, max_length=100)
    ds_password = StringField(required=True, max_length=156)
    ds_port = StringField(required=True, max_length=10)
    ds_database = StringField(required=True, max_length=100)
    ds_connector = StringField(required=True, max_length=100)
    
class Project(Document):
    id_project = SequenceField(primary_key=True, required=True)
    name_project = StringField(unique=True, required=True, max_length=100)
    dt_last_run = DateTimeField(required=True)
    fl_active = IntField(default=0, required=True, max_value=1)
    in_execution = IntField(default=0, required=True, max_value=1)
    type_project = IntField(default=0, required=True, max_value=1) 
    connection_origin1 = IntField(default=0, required=False, unique=False)
    connection_origin2 = IntField(default=0, required=False, unique=False)

class Query(Document):
    id_query = SequenceField(primary_key=True, required=True)
    id_project = IntField(required=True)
    origin_query = StringField()
    query_destination = StringField(max_length=300)
    id_type_query = IntField(required=True)
    nr_execution_order = IntField(required=True, max_value=5)

class Scripts(Document):
    id_script = SequenceField(primary_key=True, required=True)
    id_project = IntField(required=True)
    script_name = StringField(required=True, max_length=50)
    ds_script = StringField(max_length=20000)
    nr_execution_order = IntField(required=True, max_value=5)
    
class Log(Document):
    id_log = SequenceField(primary_key=True, required=True)
    id_project = IntField(required=True)
    dt_execution = DateTimeField(required=True)
    ds_log = StringField(max_length=1000)
    fl_error = IntField(default=0, required=True)

class Time(Document):
    id_time = SequenceField(primary_key=True, required=True)
    id_project = IntField(required=True)
    time = StringField()

    def clean(self):
        super().clean()

        if self.time:
            time_pattern = re.compile(r'^\d{2}:\d{2}:\d{2}$')
            if not time_pattern.match(str(self.time)):
                raise ValidationError("Invalid time format. Expected format: HH:MM")


class TypeQuery(Document):
    id_type_query = SequenceField(primary_key=True, required=True)
    ds_type_query = StringField(unique=True, required=True)

