from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Products, CartItem


# @receiver -> это декоратор, который используется для подключения функций-обработчиков к сигналам.
# Сигналы Django позволяют компонентам приложения получать уведомления о событиях в системе.
@receiver(post_save, sender=Products)
def update_cart_item_quantity(sender, instance, **kwargs):
    # sender -> Тип модели, которая отправила сигнал. В этом случае, это модель Products.
    # instance ->  Экземпляр модели Products
    cart_items = CartItem.objects.filter(product=instance)
    for item in cart_items:
        item.quantity = instance.quantity
        item.save()