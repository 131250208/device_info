# -*- coding: utf-8 -*-

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from __future__ import unicode_literals

from django.db import models


class Brand(models.Model):
    en_name = models.CharField(max_length=255, blank=True, null=True)
    cn_name = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    product_type = models.CharField(max_length=255, blank=True, null=True)
    brand_link = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'iie_brand'
        unique_together = (('en_name', 'cn_name'),)

    def __unicode__(self):
        return '%s - %s' % (self.en_name, self.cn_name)


class BrandModel(models.Model):
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    model_link = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'iie_brand_model'
        unique_together = (('brand', 'model'),)

    def __unicode__(self):
        return '%s : %s' % (self.brand, self.model)


class DeviceType(models.Model):
    category = models.CharField(max_length=50)
    category_cn_name = models.CharField(max_length=50, blank=True, null=True)
    category_en_name = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=50)
    type_cn_name = models.CharField(max_length=50, blank=True, null=True)
    type_en_name = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'iie_device_type'
        unique_together = (('category', 'type'),)

    def __unicode__(self):
        return '%s : %s : %s : %s : %s : %s' % (self.category, self.category_cn_name, self.category_en_name,
                                                self.type, self.type_cn_name, self.type_en_name)


class Banner(models.Model):
    id = models.IntegerField(primary_key=True)
    accuracy = models.IntegerField(blank=True, null=True)
    device_category = models.CharField(max_length=50, blank=True, null=True)
    device_type = models.CharField(max_length=50, blank=True, null=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50, blank=True, null=True)
    server = models.CharField(max_length=100, blank=True, null=True)
    www_authenticate = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    others = models.CharField(max_length=200, blank=True, null=True)
    match_type = models.IntegerField(blank=True, null=True)
    protocol = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'iie_banner'

    def __unicode__(self):
        return '%s : %s : %s : %s : %s : %s : %s' % (self.device_category, self.device_type, self.brand, self.model,
                                                     self.protocol, self.accuracy, self.match_type)
