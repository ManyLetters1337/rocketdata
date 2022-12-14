# Generated by Django 4.1.3 on 2022-12-01 20:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rocket_app', '0005_alter_element_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='contact',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='rocket_app.contact'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='worker',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='rocket_app.element'),
        ),
        migrations.AlterField(
            model_name='element',
            name='type',
            field=models.CharField(choices=[('Individual Entrepreneur', 'Individual Entrepreneur'), ('Retail Network', 'Retail Network'), ('Dealership', 'Dealership'), ('Factory', 'Factory'), ('Distributor', 'Distributor')], default='Factory', max_length=50),
        ),
    ]
