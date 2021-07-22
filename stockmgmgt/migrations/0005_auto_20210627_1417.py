# Generated by Django 3.2 on 2021-06-27 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmgt', '0004_transaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='stockmgmgt.stock')),
                ('employee_name', models.CharField(max_length=50)),
                ('product_name', models.CharField(max_length=50)),
                ('price', models.IntegerField(default=0)),
                ('is_complete', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='OrderQuantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default='0', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='item_name',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='transaction_type',
        ),
        migrations.AddField(
            model_name='transaction',
            name='items_count',
            field=models.CharField(default=1, max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='product_ids',
            field=models.CharField(default=1, max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='stock',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
