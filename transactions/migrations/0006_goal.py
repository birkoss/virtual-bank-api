# Generated by Django 3.0.7 on 2020-06-18 22:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_auto_20200616_1123'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=100)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.Account')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]