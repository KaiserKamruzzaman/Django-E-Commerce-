# Generated by Django 3.0.3 on 2020-08-06 19:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecom_app', '0008_auto_20200805_0100'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='Customer',
            new_name='customer',
        ),
    ]
