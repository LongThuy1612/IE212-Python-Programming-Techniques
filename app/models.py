from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Sản phẩm
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=0, null=True)  # Giá tiền có đơn vị
    motor_type = models.CharField(max_length=100, null=True)  # Loại xe
    description = models.TextField(null=True, blank=True)  # Mô tả chi tiết
    image = models.ImageField(null=True, blank=True)  # Ảnh xe

    def __str__(self):
        return self.name
    
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

# Đơn hàng
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    order_date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"Order {self.id}"
    
    @property
    def get_total_cart_items(self):
        orderitems = self.items.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    @property
    def get_total_cart_price(self):
        orderitems = self.items.all()
        total = sum([item.get_each_item_total_price for item in orderitems])
        return total
    
    @property
    def get_total_cart_items_choiced(self):
        orderitems = self.items.filter(choiced=True)
        total = sum([item.quantity for item in orderitems])
        return total
    
    @property
    def get_total_cart_price_choiced(self):
        orderitems = self.items.filter(choiced=True)
        total = sum([item.get_each_item_total_price for item in orderitems])
        return total


# Chi tiết đơn hàng
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='items')
    quantity = models.PositiveIntegerField(default=0, null = True, blank=True)
    choiced = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"
    
    @property
    def get_each_item_total_price(self):
        total = self.product.price * self.quantity
        return total

# Địa chỉ giao hàng
class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    reci_name = models.CharField(max_length=200, null=True, blank=True)
    reci_phone = models.CharField(max_length=10, null=True, blank=True)

    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=100, null=True)
    province = models.CharField(max_length=100, null=True)  # Tỉnh/Thành phố
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.province}"
    
# User Form
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
