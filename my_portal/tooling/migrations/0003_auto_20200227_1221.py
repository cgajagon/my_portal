# Generated by Django 2.2.10 on 2020-02-27 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_supplier_account_manager'),
        ('tooling', '0002_auto_20200226_1935'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='toolconditionprocess',
            name='audit_status',
        ),
        migrations.RemoveField(
            model_name='toolconditionprocess',
            name='tool',
        ),
        migrations.AddField(
            model_name='toolconditionprocess',
            name='date_audit',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='toolconditionprocess',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.Supplier'),
        ),
    ]
