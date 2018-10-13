from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):
    #initiate cart
    def __init__(self, request):
        #store the current session
        self.session = request.session
        #get cart if existing
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            #initializa new empty cart
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    #function to add a product
    def add(self, product, quantity=1, update_quantity=False):
        #change to string as json uses only strings to serialize data
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    #return the total items in cart
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    #clear cart session
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

        