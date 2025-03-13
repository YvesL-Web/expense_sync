# Generated by Django 4.2.11 on 2025-03-13 13:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bank_accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('pkid', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('transaction_id', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('pending', models.BooleanField(default=False)),
                ('category', models.CharField(blank=True, max_length=255, null=True)),
                ('payment_channel', models.CharField(max_length=255)),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='bank_accounts.bankaccount')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SyncCursor',
            fields=[
                ('pkid', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cursor', models.CharField(blank=True, max_length=255, null=True)),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sync_cursor', to='bank_accounts.bankaccount')),
            ],
            options={
                'verbose_name': 'Sync Cursor',
                'verbose_name_plural': 'Sync Cursors',
            },
        ),
    ]
