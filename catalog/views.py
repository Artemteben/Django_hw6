from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from catalog.models import Product


def home(request):
    return render(request, "home.html")


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        print(name, phone, message)
    return render(request, "contacts.html")


class ProductListView(ListView):
    model = Product

    # catalog/catalog_list.html
    # def base_r(request):


class ProductDetailView(DetailView):
    model = Product

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


# products = Product.objects.all()
# context = {"products": products}
# return render(request, "catalog_list.html", context)


# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     context1 = {'product': product}
#     return render(request, 'product_detail.html', context1)

class ProductCreateView(CreateView):
    model = Product
    fields = ("name", "description", "price", "category", "image", "created_at")
    success_url = reverse_lazy("catalog:product_list")


class ProductUpdateView(UpdateView):
    model = Product
    fields = ("name", "description", "price", "category", "image", "created_at")
    success_url = reverse_lazy("catalog:product_list")

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.kwargs.get("pk")])


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")
