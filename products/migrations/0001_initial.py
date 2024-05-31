# Generated by Django 5.0.4 on 2024-04-21 18:47

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, unique=True, verbose_name='Title')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Title')),
                ('price', models.IntegerField(default=0, verbose_name='Price')),
                ('short_description', models.CharField(max_length=150, verbose_name='Short description')),
                ('quantity', models.IntegerField(default=0, verbose_name='Quantity')),
                ('sku', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('description', ckeditor.fields.RichTextField(verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ProductsReactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_liked', models.BooleanField(default=False, verbose_name='Liked')),
                ('rating', models.PositiveSmallIntegerField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True)),
            ],
            options={
                'verbose_name': 'Product Reaction',
                'verbose_name_plural': 'Products Reactions',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(verbose_name='Comments')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
            ],
            options={
                'verbose_name': 'Review',
                'verbose_name_plural': 'Reviews',
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, unique=True, verbose_name='Title')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
            ],
            options={
                'verbose_name': 'Size',
                'verbose_name_plural': 'Sizes',
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, unique=True, verbose_name='Title')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
            ],
            options={
                'verbose_name': 'Tags',
                'verbose_name_plural': 'Tags',
            },
        ),
    ]