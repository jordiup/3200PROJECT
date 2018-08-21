# Generated by Django 2.1 on 2018-08-19 08:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archive_number', models.CharField(max_length=100)),
                ('date_written', models.DateTimeField(verbose_name='date written')),
                ('document_type', models.CharField(max_length=16)),
                ('language', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=24)),
                ('last_name', models.CharField(max_length=24)),
                ('full_name', models.CharField(max_length=49)),
                ('date_added', models.DateTimeField(verbose_name='date added')),
            ],
        ),
        migrations.CreateModel(
            name='PersonLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(verbose_name='date added')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.Location')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.Person')),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver',
                                    to='db.PersonLocation'),
        ),
        migrations.AddField(
            model_name='document',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender',
                                    to='db.PersonLocation'),
        ),
    ]
