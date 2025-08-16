from django.shortcuts import render
from . models import *
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

# Create your views here.




# def register_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         confirm = request.POST.get('password2')

#         if password != confirm:
#             return render(request, 'register.html', {'error': 'Passwords do not match'})

#         if Register.objects.filter(username=username).exists():
#             return render(request, 'register.html', {'error': 'Username already exists'})

#         hashed_password = make_password(password)
#         user = Register.objects.create(username=username, password=hashed_password)
#         request.session['user_id'] = user.id
#         request.session['username'] = user.username
#         return redirect('login')

#     return render(request, 'register.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # Block if username or password contains a link
        link_pattern = re.compile(r'(https?://|www\.)', re.IGNORECASE)
        if link_pattern.search(username) or link_pattern.search(password):
            return render(request, 'admin_login.html', {
                'error': 'Links are not allowed in username or password.',
                'username': username
            })

        try:
            user = Register.objects.get(username=username)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                return redirect('dashboard')
            else:
                return render(request, 'admin_login.html', {
                    'error': 'Incorrect password',
                    'username': username
                })
        except Register.DoesNotExist:
            return render(request, 'admin_login.html', {
                'error': 'User not found',
                'username': username
            })

    return render(request, 'admin_login.html')


def logout_view(request):
    request.session.flush()
    return redirect('login')

# @login_required
# @never_cache
# def dashboard(request):
#     if request.method == "POST":
#         enquiry_id = request.POST.get("enquiry_id")
#         if enquiry_id:
#             enquiry = get_object_or_404(Enquiry, id=enquiry_id)
#             enquiry.delete()
#             return redirect('admin_enquiry')  # or your dashboard URL name

#     enquiry = Enquiry.objects.all()
#     enquiry_count = Enquiry.objects.count()
#     product_count = Product.objects.count()  # Get total number of products

#     context = {
#         'enquiry': enquiry,
#         'enquiry_count': enquiry_count,
#         'product_count': product_count,
#     }
#     return render(request, 'admin_dashboard.html', context)

@never_cache
def dashboard(request):
    # Manual session check instead of @login_required
    if not request.session.get('user_id'):
        return redirect('login')  # Redirect to your login page if not logged in

    if request.method == "POST":
        enquiry_id = request.POST.get("enquiry_id")
        if enquiry_id:
            enquiry = get_object_or_404(Enquiry, id=enquiry_id)
            enquiry.delete()
            return redirect('admin_enquiry')  # or 'dashboard' if you want to stay here

    enquiry = Enquiry.objects.all().order_by('-id')
    enquiry_count = Enquiry.objects.count()
    product_count = Product.objects.count()

    context = {
        'enquiry': enquiry,
        'enquiry_count': enquiry_count,
        'product_count': product_count,
    }
    return render(request, 'admin_dashboard.html', context)



# def admin_productlisting(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         material = request.POST.get('material')
#         price = request.POST.get('price')
#         dimension = request.POST.get('dimension')
#         color = request.POST.get('color')
#         warranty = request.POST.get('warranty')
#         weight = request.POST.get('weight')
#         seating_capacity = request.POST.get('seating_capacity')
#         availability = request.POST.get('availability')
#         return_policy = request.POST.get('return_policy')

#         # Create Product
#         product = Product.objects.create(
#             name=name,
#             material=material,
#             price=price,
#             dimension=dimension,
#             color=color,
#             warranty=warranty,
#             weight=weight,
#             seating_capacity=seating_capacity,
#             availability=availability,
#             return_policy=return_policy
#         )

#         # Handle multiple images
#         for img in request.FILES.getlist('images'):
#             ProductImage.objects.create(product=product, image=img)

#         return redirect('listing') 
#     return render(request,'admin_productlisting.html')


from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, ProductImage

# def admin_productlisting(request):
#     if request.method == 'POST':
#         action = request.POST.get('action')

#         if action == 'add':
#             # Add new product
#             product = Product.objects.create(
#                 name=request.POST.get('name'),
#                 material=request.POST.get('material'),
#                 price=request.POST.get('price'),
#                 dimension=request.POST.get('dimension'),
#                 color=request.POST.get('color'),
#                 warranty=request.POST.get('warranty'),
#                 weight=request.POST.get('weight'),
#                 seating_capacity=request.POST.get('seating_capacity'),
#                 availability=request.POST.get('availability'),
#                 return_policy=request.POST.get('return_policy')
#             )
#             for img in request.FILES.getlist('images'):
#                 ProductImage.objects.create(product=product, image=img)
#             return redirect('admin_productlisting')

#         elif action == 'edit':
#             # Edit existing product
#             product_id = request.POST.get('product_id')
#             product = get_object_or_404(Product, id=product_id)
#             product.name = request.POST.get('name')
#             product.material = request.POST.get('material')
#             product.price = request.POST.get('price')
#             product.dimension = request.POST.get('dimension')
#             product.color = request.POST.get('color')
#             product.warranty = request.POST.get('warranty')
#             product.weight = request.POST.get('weight')
#             product.seating_capacity = request.POST.get('seating_capacity')
#             product.availability = request.POST.get('availability')
#             product.return_policy = request.POST.get('return_policy')
#             product.save()

#             if request.FILES.getlist('images'):
#                 product.images.all().delete()
#                 for img in request.FILES.getlist('images'):
#                     ProductImage.objects.create(product=product, image=img)
#             return redirect('admin_productlisting')

#     elif request.method == 'GET' and request.GET.get('delete'):
#         # Delete product
#         product = get_object_or_404(Product, id=request.GET.get('delete'))
#         product.delete()
#         return redirect('admin_productlisting')

#     products = Product.objects.all()
#     return render(request, 'admin_productlisting.html', {'products': products})


from decimal import Decimal


from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, ProductImage

# def admin_productlisting(request):
#     if request.method == "POST":
#         action = request.POST.get("action")

#         if action == "add":
#             product = Product.objects.create(
#                 name=request.POST.get('name'),
#                 material=request.POST.get('material'),
#                 price=request.POST.get('price'),
#                 dimension=request.POST.get('dimension'),
#                 color=request.POST.get('color'),
#                 weight=request.POST.get('weight'),
#                 seating_capacity=request.POST.get('seating_capacity'),
#                 warranty=request.POST.get('warranty'),
#                 availability=request.POST.get('availability'),
#                 return_policy=request.POST.get('return_policy'),
#             )
#             for img in request.FILES.getlist('images'):
#                 ProductImage.objects.create(product=product, image=img)

#         elif action == "edit":
#             product = get_object_or_404(Product, id=request.POST.get('product_id'))
#             product.name = request.POST.get('name')
#             product.material = request.POST.get('material')
#             product.price = request.POST.get('price')
#             product.dimension = request.POST.get('dimension')
#             product.color = request.POST.get('color')
#             product.weight = request.POST.get('weight')
#             product.seating_capacity = request.POST.get('seating_capacity')
#             product.warranty = request.POST.get('warranty')
#             product.availability = request.POST.get('availability')
#             product.return_policy = request.POST.get('return_policy')
#             product.save()

#             if request.FILES.getlist('images'):
#                 product.images.all().delete()
#                 for img in request.FILES.getlist('images'):
#                     ProductImage.objects.create(product=product, image=img)

#         elif action == "delete":
#             product = get_object_or_404(Product, id=request.POST.get('product_id'))
#             product.delete()

#         return redirect('listing')

#     products = Product.objects.all()
#     return render(request, 'admin_productlisting.html', {'products': products})

from django.http import HttpResponseBadRequest
import json



# @never_cache
# def admin_productlisting(request):
#     if not request.session.get('user_id'):
#         return redirect('login')

#     categories = Category.objects.all()

#     if request.method == "POST":
#         action = request.POST.get("action")
#         product_id = request.POST.get('product_id')

#         if action in ['edit', 'delete']:
#             if not product_id or not product_id.isdigit():
#                 return HttpResponseBadRequest("Invalid or missing product ID.")
#             product_id = int(product_id)

#         if action == "add":
#             category_id = request.POST.get('category')
#             category = get_object_or_404(Category, id=category_id)

#             product = Product.objects.create(
#                 name=request.POST.get('name', '').strip(),
#                 subsentence=request.POST.get('subsentence', '').strip(),
#                 category=category,
#                 material=request.POST.get('material', '').strip(),
#                 price=request.POST.get('price', 0),
#                 offer=request.POST.get('offer', '').strip(),
#                 discount=request.POST.get('discount', '').strip(),
#                 dimension=request.POST.get('dimension', '').strip(),
#                 color=request.POST.get('color', '').strip(),
#                 weight=request.POST.get('weight', '').strip(),
#                 seating_capacity=request.POST.get('seating_capacity', '').strip(),
#                 warranty=request.POST.get('warranty', '').strip(),
#                 availability=request.POST.get('availability', '').strip(),
#                 return_policy=request.POST.get('return_policy', '').strip(),
#                 description=request.POST.get('description', '').strip() or ""
#             )
#             for img in request.FILES.getlist('images'):
#                 ProductImage.objects.create(product=product, image=img)

#         elif action == "edit":
#             product = get_object_or_404(Product, id=product_id)
#             category_id = request.POST.get('category')
#             category = get_object_or_404(Category, id=category_id)

#             product.name = request.POST.get('name', '').strip()
#             product.subsentence = request.POST.get('subsentence', '').strip()
#             product.category = category
#             product.material = request.POST.get('material', '').strip()
#             product.price = request.POST.get('price', 0)
#             product.offer = request.POST.get('offer', '').strip()
#             product.discount = request.POST.get('discount', '').strip()
#             product.dimension = request.POST.get('dimension', '').strip()
#             product.color = request.POST.get('color', '').strip()
#             product.weight = request.POST.get('weight', '').strip()
#             product.seating_capacity = request.POST.get('seating_capacity', '').strip()
#             product.warranty = request.POST.get('warranty', '').strip()
#             product.availability = request.POST.get('availability', '').strip()
#             product.return_policy = request.POST.get('return_policy', '').strip()
#             product.description = request.POST.get('description', '').strip() or ""
#             product.save()

#             if request.FILES.getlist('images'):
#                 product.images.all().delete()
#                 for img in request.FILES.getlist('images'):
#                     ProductImage.objects.create(product=product, image=img)

#         elif action == "delete":
#             product = get_object_or_404(Product, id=product_id)
#             product.delete()

#         return redirect('listing')

#     # Prefetch images and prepare JSON for JS
#     products = Product.objects.select_related('category').prefetch_related('images').all()
#     products_json = []
#     for p in products:
#         products_json.append({
#             'id': p.id,
#             'category_id': p.category.id if p.category else None,
#             'name': p.name,
#             'subsentence': p.subsentence,
#             'material': p.material,
#             'price': str(p.price),
#             'offer': p.offer,
#             'discount': p.discount,
#             'dimension': p.dimension,
#             'color': p.color,
#             'weight': p.weight,
#             'seating_capacity': p.seating_capacity,
#             'warranty': p.warranty,
#             'availability': p.availability,
#             'return_policy': p.return_policy,
#             'description': p.description,
#             'images': [img.image.url for img in p.images.all()]
#         })

#     return render(request, 'admin_productlisting.html', {
#         'products': products,
#         'categories': categories,
#         'products_json': json.dumps(products_json)
#     })


@never_cache
def admin_productlisting(request):
    if not request.session.get('user_id'):
        return redirect('login')

    categories = Category.objects.all()

    if request.method == "POST":
        action = request.POST.get("action")
        product_id = request.POST.get('product_id')

        if action in ['edit', 'delete']:
            if not product_id or not product_id.isdigit():
                return HttpResponseBadRequest("Invalid or missing product ID.")
            product_id = int(product_id)

        # Helper: convert empty string to None for numeric fields
        def parse_float(value):
            return float(value) if value not in [None, ''] else None

        if action == "add":
            category_id = request.POST.get('category')
            category = get_object_or_404(Category, id=category_id)

            product = Product.objects.create(
                name=request.POST.get('name', '').strip(),
                subsentence=request.POST.get('subsentence', '').strip(),
                category=category,
                material=request.POST.get('material', '').strip(),
                price=parse_float(request.POST.get('price')),
                offer=request.POST.get('offer', '').strip(),
                discount=request.POST.get('discount', '').strip(),
                dimension=request.POST.get('dimension', '').strip(),
                color=request.POST.get('color', '').strip(),
                weight=request.POST.get('weight', '').strip(),
                seating_capacity=request.POST.get('seating_capacity', '').strip(),
                warranty=request.POST.get('warranty', '').strip(),
                availability=request.POST.get('availability', '').strip(),
                return_policy=request.POST.get('return_policy', '').strip(),
                description=request.POST.get('description', '').strip() or ""
            )
            for img in request.FILES.getlist('images'):
                ProductImage.objects.create(product=product, image=img)

        elif action == "edit":
            product = get_object_or_404(Product, id=product_id)
            category_id = request.POST.get('category')
            category = get_object_or_404(Category, id=category_id)

            product.name = request.POST.get('name', '').strip()
            product.subsentence = request.POST.get('subsentence', '').strip()
            product.category = category
            product.material = request.POST.get('material', '').strip()
            product.price = parse_float(request.POST.get('price'))
            product.offer = request.POST.get('offer', '').strip()
            product.discount = request.POST.get('discount', '').strip()
            product.dimension = request.POST.get('dimension', '').strip()
            product.color = request.POST.get('color', '').strip()
            product.weight = request.POST.get('weight', '').strip()
            product.seating_capacity = request.POST.get('seating_capacity', '').strip()
            product.warranty = request.POST.get('warranty', '').strip()
            product.availability = request.POST.get('availability', '').strip()
            product.return_policy = request.POST.get('return_policy', '').strip()
            product.description = request.POST.get('description', '').strip() or ""
            product.save()

            if request.FILES.getlist('images'):
                product.images.all().delete()
                for img in request.FILES.getlist('images'):
                    ProductImage.objects.create(product=product, image=img)

        elif action == "delete":
            product = get_object_or_404(Product, id=product_id)
            product.delete()

        return redirect('listing')

    # Prefetch images and prepare JSON for JS
    products = Product.objects.select_related('category').prefetch_related('images').order_by('-id')
    products_json = []
    for p in products:
        products_json.append({
            'id': p.id,
            'category_id': p.category.id if p.category else None,
            'name': p.name,
            'subsentence': p.subsentence,
            'material': p.material,
            'price': str(p.price) if p.price is not None else "",
            'offer': p.offer,
            'discount': p.discount,
            'dimension': p.dimension,
            'color': p.color,
            'weight': p.weight,
            'seating_capacity': p.seating_capacity,
            'warranty': p.warranty,
            'availability': p.availability,
            'return_policy': p.return_policy,
            'description': p.description,
            'images': [img.image.url for img in p.images.all()]
        })

    return render(request, 'admin_productlisting.html', {
        'products': products,
        'categories': categories,
        'products_json': json.dumps(products_json)
    })



from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

@never_cache
@require_http_methods(["GET", "POST"])
def admin_contact(request):
    if not request.session.get('user_id'):
        return redirect('login') 
    if request.method == "POST":
        contact_id = request.POST.get("contact_id")
        if contact_id:
            contact = get_object_or_404(Contact, id=contact_id)
            contact.delete()
            return redirect('admin_contact')  # Replace with your URL name

    contacts = Contact.objects.all()
    return render(request, 'admin_contact.html', {'contacts': contacts})

@never_cache
@require_http_methods(["GET", "POST"])
def admin_enquiry(request):
    if not request.session.get('user_id'):
        return redirect('login') 
    if request.method == "POST":
        enquiry_id = request.POST.get("enquiry_id")
        if enquiry_id:
            enquiry = get_object_or_404(Enquiry, id=enquiry_id)
            enquiry.delete()
            return redirect('admin_enquiry')  # Replace with your URL name

    
    enquiry = Enquiry.objects.all().order_by('-id')

    return render(request, 'admin_enquiry.html', {'enquiry': enquiry})



def delete_enquiry(request, enquiry_id):
    enquiry = get_object_or_404(Enquiry, id=enquiry_id)
    enquiry.delete()
    return redirect('admin_enquiry')  # Redirect to enquiry list after deletion

@never_cache
def category(request):
    if not request.session.get('user_id'):
        return redirect('login')

    if request.method == "POST":
        if 'delete_id' in request.POST:
            category_id = request.POST.get('delete_id')
            category = get_object_or_404(Category, id=category_id)
            category.delete()
            return redirect('category')

        elif 'edit_id' in request.POST:
            category_id = request.POST.get('edit_id')
            name = request.POST.get('name', '').strip()
            category = get_object_or_404(Category, id=category_id)
            if name:
                category.name = name
                category.save()
            return redirect('category')

        else:
            # Add category
            name = request.POST.get("name", "").strip()
            if name and not Category.objects.filter(name__iexact=name).exists():
                Category.objects.create(name=name)
            return redirect('category')

    categories = Category.objects.all()
    return render(request, 'admin_categories.html', {'categories': categories})


from django.shortcuts import render, redirect
from django.templatetags.static import static
import re

ALLOWED_PATTERN = re.compile(r'^[a-zA-Z0-9\s\.,\'"@]+$')

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()

        # Validation: fields must not be empty
        if not all([name, email, subject, message]):
            messages.error(request, "Please fill all the fields.")
            return redirect('contact')

        # Validation: no disallowed characters
        for field_value, field_name in [
            (name, "Name"),
            (subject, "Subject"),
            (message, "Message")
        ]:
            if not ALLOWED_PATTERN.match(field_value):
                messages.error(
                    request,
                    f"{field_name} contains invalid characters. Only letters, numbers, spaces, and . , ' \" @ are allowed."
                )
                return redirect('contact')

        # Save to DB if valid
        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')

    return render(request, "contact.html")

def index(request):
    products = Product.objects.all().order_by('-id')[:4]

    for product in products:
        if product.images.exists():
            image_url = product.images.first().image.url
        else:
            image_url = static('images/default-product.jpg')

       
        product.absolute_image_url = request.build_absolute_uri(image_url)

    return render(request, 'index.html', {'products': products})



def product(request):
   
    selected_category = request.GET.get('category')

   
    try:
        selected_category = int(selected_category) if selected_category else None
    except (ValueError, TypeError):
        selected_category = None

   
    categories = Category.objects.all()

   
    products = Product.objects.all().order_by('-id')

   
    if selected_category:
        products = products.filter(category_id=selected_category).order_by('-id')

    return render(request, 'products.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category
    })



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Enquiry
from decimal import Decimal, InvalidOperation
import re



from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.db.models import Q
import random



from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.templatetags.static import static
from .models import Product, Enquiry


def safe_decimal(value, default=Decimal("0.00")):
    """Safely convert to Decimal, returning default if invalid."""
    try:
        if value is None or str(value).strip() == "":
            return default
        return Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return default


from decimal import Decimal, InvalidOperation

# def product_detail(request, product_id):
#     # Get the main product
#     product = get_object_or_404(Product, pk=product_id)

#     # Use offer price if available, else regular price
#     base_price = safe_decimal(product.offer) if product.offer else safe_decimal(product.price)

#     # Related products (same category, exclude itself)
#     related_products_qs = Product.objects.filter(category=product.category).exclude(pk=product_id)

#     # Filter by ±20% price range
#     price_range_min = base_price * Decimal("0.8")
#     price_range_max = base_price * Decimal("1.2")

#     related_products = related_products_qs.filter(
#         price__gte=price_range_min,
#         price__lte=price_range_max
#     )[:6]

#     # Fallbacks if not enough related products
#     if not related_products.exists():
#         related_products = related_products_qs[:6]
#     if not related_products.exists():
#         related_products = Product.objects.exclude(pk=product_id)[:6]

#     # Prepare image absolute URL for meta tags
#     if product.images.exists():
#         image_url = request.build_absolute_uri(product.images.first().image.url)
#     else:
#         image_url = request.build_absolute_uri(static("images/default-product.jpg"))

#     # Prepare page absolute URL
#     page_url = request.build_absolute_uri(request.path)

#     # Handle POST (Enquiry Form)
#     if request.method == "POST":
#         try:
#             product_name = request.POST.get("product_name", "").strip()
#             product_material = request.POST.get("product_material", "").strip()
#             product_offer_raw = request.POST.get("product_offer", "").strip()
#             product_color = request.POST.get("product_color", "").strip()
#             product_quantity_raw = request.POST.get("product_quantity", "").strip()
#             customer_name = request.POST.get("customer_name", "").strip()
#             contact_number = request.POST.get("contact_number", "").strip()

#             # Clean & convert values
#             cleaned_price = (
#                 product_offer_raw.replace("₹", "").replace(",", "").strip() or "0"
#             )
#             product_offer_val = safe_decimal(cleaned_price, default=Decimal("0.00"))
#             product_quantity_val = int(product_quantity_raw) if product_quantity_raw.isdigit() else 0

#             # Save enquiry
#             Enquiry.objects.create(
#                 product_name=product_name,
#                 product_material=product_material,
#                 product_offer=product_offer_val,
#                 product_color=product_color,
#                 product_quantity=product_quantity_val,
#                 customer_name=customer_name,
#                 contact_number=contact_number
#             )

#             messages.success(request, "Your enquiry has been submitted successfully!")
#             return redirect("product_detail", product_id=product.id)

#         except Exception as e:
#             messages.error(request, f"Error saving enquiry: {e}")

#     return render(request, "detail_product.html", {
#         "product": product,
#         "related_products": related_products,
#         "image_url": image_url,
#         "page_url": page_url
#     })

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    base_price = safe_decimal(product.offer) if product.offer else safe_decimal(product.price)

    related_products_qs = Product.objects.filter(category=product.category).exclude(pk=product_id)

    price_range_min = base_price * Decimal("0.8")
    price_range_max = base_price * Decimal("1.2")

    related_products = related_products_qs.filter(
        price__gte=price_range_min,
        price__lte=price_range_max
    )[:6]

    if not related_products.exists():
        related_products = related_products_qs[:6]
    if not related_products.exists():
        related_products = Product.objects.exclude(pk=product_id)[:6]

    if product.images.exists():
        image_url = request.build_absolute_uri(product.images.first().image.url)
    else:
        image_url = request.build_absolute_uri(static("images/default-product.jpg"))

    page_url = request.build_absolute_uri(request.path)

    if request.method == "POST":
        try:
            product_name = request.POST.get("product_name", "").strip()
            product_material = request.POST.get("product_material", "").strip()
            product_offer_raw = request.POST.get("product_offer", "").strip()
            product_color = request.POST.get("product_color", "").strip()
            product_quantity_raw = request.POST.get("product_quantity", "").strip()
            customer_name = request.POST.get("customer_name", "").strip()
            contact_number = request.POST.get("contact_number", "").strip()

            cleaned_price = (
                product_offer_raw.replace("₹", "").replace(",", "").strip() or "0"
            )
            product_offer_val = safe_decimal(cleaned_price, default=Decimal("0.00"))

            # Validate quantity
            if not product_quantity_raw.isdigit():
                messages.error(request, "Invalid quantity entered.")
                return redirect("product_detail", product_id=product.id)

            product_quantity_val = int(product_quantity_raw)

            if product_quantity_val < 1:
                messages.error(request, "Quantity must be at least 1.")
                return redirect("product_detail", product_id=product.id)

            if product_quantity_val > 999:
                messages.error(request, "Quantity cannot be more than 999.")
                return redirect("product_detail", product_id=product.id)

        # Save enquiry
            Enquiry.objects.create(
            product_name=product_name,
            product_material=product_material,
            product_offer=product_offer_val,
            product_color=product_color,
            product_quantity=product_quantity_val,
            customer_name=customer_name,
            contact_number=contact_number
        )

            messages.success(request, "Your enquiry has been submitted successfully!")
            return redirect("product_detail", product_id=product.id)

        except Exception as e:
            messages.error(request, f"Error saving enquiry: {e}")


    return render(request, "detail_product.html", {
        "product": product,
        "related_products": related_products,
        "image_url": image_url,
        "page_url": page_url
    })

def about(request):
    return render(request, 'about.html')

def base(request):
    return render(request, 'base.html')











