
#from api.config.dbConfig import db
from api.model.db import Project, ConnectionDestination, Query, Scripts, Log, Time

class ProjectDeleter:
    def delete_project_and_related_objects(self, id_project):
        type_project = Project.objects(id_project=id_project).first()
        if type_project.type_project == 0:
            Query.objects(id_project=id_project).delete()
        else:
            Scripts.objects(id_project=id_project).delete()
        Log.objects(id_project=id_project).delete()
        Time.objects(id_project=id_project).delete()
        Project.objects(id_project=id_project).delete()

class ConnectionDestinationDeleter:
    def delete_connection_destination(self, id_connection):
        connection_origin1 = Project.objects(connection_origin1=id_connection).first()
        connection_origin2 = Project.objects(connection_origin2=id_connection).first()
        if connection_origin1:
            Project.objects(id_project=connection_origin1.id_project).update(set__connection_origin1=0)
        if connection_origin2:
            Project.objects(id_project=connection_origin2.id_project).update(set__connection_origin2=0)
        ConnectionDestination.objects(id_connection=id_connection).delete()
        
