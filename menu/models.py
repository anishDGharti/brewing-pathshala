from django.db import models
from django.contrib.auth.models import Group, Permission

from usable.base_models import BaseModel

# Create your models here.


MENU_ITEMS = (
        ('coffee', 'Coffee'),
        ('tea', 'Tea'),
        ('bakery_item', 'Bakery Item'),
        # Add more menu items here if needed
    )



class CoffeeShopMenu(BaseModel):
    menu = models.CharField(max_length=20, choices=MENU_ITEMS)    
    menu_item = models.CharField(max_length=50, help_text="example: espresso mojito, cake")
    ingredients_added=models.TextField(max_length=200, blank=True, null=True, help_text="example:for espresso to prepare:30ml watre, sugar 20gm coffee")
    price = models.DecimalField(max_digits=30, decimal_places=2)
    image = models.BinaryField(null=True)

    class Meta:
        db_table = "coffee_shop_menu"
        indexes = [
            models.Index(fields=['menu_item'], name='idx_coffee_shop_menu_menu_item'),
        ]

    

    def __str__(self):
        return self.menu_item
    






class SideBarMenu(BaseModel):
    menu_name = models.CharField(max_length=200)
    parent = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True,related_name="+")
    ordinal_number  = models.IntegerField(default=0)
    roles = models.ManyToManyField(Group, blank=True)
    permissions = models.ManyToManyField(Permission, blank=True)
    url = models.CharField(max_length=200)  
    icon = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'coffee_sidebar_menu'
