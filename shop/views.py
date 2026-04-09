from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Comment, News  # Добавили News в импорт


def index(request):
    sort_by = request.GET.get('sort')
    search_query = request.GET.get('search')
    category_id = request.GET.get('category')

    # Получаем базовые наборы данных
    products = Product.objects.all()
    categories = Category.objects.all()

    # --- ЛЕНТА НОВОСТЕЙ ---
    # Берем 3 последние новости (order_by('-created_at') ставит свежие вперед)
    news = News.objects.all().order_by('-created_at')[:3]

    # 1. Фильтр по категориям
    if category_id:
        products = products.filter(category_id=category_id)

    # 2. Фильтр по поиску
    if search_query:
        products = products.filter(name__icontains=search_query)

    # 3. Сортировка
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        products = products.order_by('-rating')

    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories,
        'news': news  # Обязательно передаем новости в шаблон
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        author = request.POST.get('author')
        text = request.POST.get('text')
        if author and text:
            Comment.objects.create(product=product, author=author, text=text)
            return redirect('product_detail', pk=product.pk)

    return render(request, 'shop/product_detail.html', {'product': product})


def support(request):
    """Страница службы поддержки"""
    return render(request, 'shop/support.html')


def compare(request):
    """Страница сравнения товаров"""
    products_to_compare = Product.objects.all()[:3]
    return render(request, 'shop/compare.html', {'products': products_to_compare})


# --- ФУНКЦИЯ УДАЛЕНИЯ КОММЕНТАРИЕВ ---

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    product_pk = comment.product.pk
    if request.user.is_staff:
        comment.delete()
    return redirect('product_detail', pk=product_pk)


# --- ФУНКЦИИ КОРЗИНЫ ---

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('index')


def view_cart(request):
    cart = request.session.get('cart', {})
    items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total_item_price = product.price * quantity
        total_price += total_item_price
        items.append({
            'product': product,
            'quantity': quantity,
            'total_item_price': total_item_price
        })

    return render(request, 'shop/cart.html', {'items': items, 'total_price': total_price})


def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']
    return redirect('view_cart')