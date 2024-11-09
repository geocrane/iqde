from iqde.plugins.sqlite_orm import models
from iqde.plugins.sqlite_orm.models import show_model
from iqde.plugins.sqlite_orm.basic_types import IntegerField, TextField


@show_model
class Replics(models.Model):
    id = IntegerField(primary_key=True, autoincrement=True)
    system_name = TextField(unique=True)
    business_name = TextField()
    subscribe_name = TextField(default="prx_")
    is_custom = IntegerField(default=1)


@show_model
class Tables(models.Model):
    id = IntegerField(primary_key=True, autoincrement=True)
    system_name = TextField()
    business_name = TextField()
    short_name = TextField()
    replic_id = IntegerField(null=False)


@show_model
class Attributes(models.Model):
    id = IntegerField(primary_key=True, autoincrement=True)
    system_name = TextField()
    business_name = TextField()
    type = TextField()
    table_id = IntegerField(null=False)


@show_model
class Scripts(models.Model):
    id = IntegerField(primary_key=True, autoincrement=True)
    replic_id = IntegerField()
    from_table = IntegerField()
    script_name = TextField()
    sql = TextField()


@show_model
class ScriptsTables(models.Model):
    id = IntegerField(primary_key=True, autoincrement=True)
    script_id = IntegerField()
    table_id = IntegerField()


@show_model
class ScriptsAttrs(models.Model):
    id = IntegerField(primary_key=True, autoincrement=True)
    script_id = IntegerField()
    attr_id = IntegerField()


@show_model
class Joins(models.Model):
    id = IntegerField(primary_key=True, autoincrement=True)
    replic_left = TextField()
    table_left = TextField()
    attr_left = TextField()
    replic_right = TextField()
    table_right = TextField()
    attr_right = TextField()
