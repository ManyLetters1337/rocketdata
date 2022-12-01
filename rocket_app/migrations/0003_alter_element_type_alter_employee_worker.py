# Generated by Django 4.1.3 on 2022-12-01 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rocket_app', '0002_alter_element_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='element',
            name='type',
            field=models.CharField(choices=[('Retail Network', 'Retail Network'), ('Factory', 'Factory'), ('Distributor', 'Distributor'), ('Dealership', 'Dealership'), ('Individual Entrepreneur', 'Individual Entrepreneur')], default='Factory', max_length=50),
        ),
        migrations.AlterField(
            model_name='employee',
            name='worker',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='rocket_app.element'),
            preserve_default=False,
        ),
    ]
