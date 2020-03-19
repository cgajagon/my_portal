# Generated by Django 2.2.10 on 2020-02-27 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tooling', '0003_auto_20200227_1221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='toolconditionprocess',
            name='supplier',
        ),
        migrations.AddField(
            model_name='toolconditionprocess',
            name='tool_inspected',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tooling.Tool'),
        ),
    ]
