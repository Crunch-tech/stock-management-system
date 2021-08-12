from django.contrib.messages.api import error
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import csv
from .models import *
from .forms import StockCreateForm, StockSearchForm, StockUpdateForm, IssueForm, ExpenseForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from .models import Transaction
from datetime import date


# Create your views here.
def home(request):
    title = 'welcome to our homepage'
    form = StockCreateForm(request.POST or None)
    context = {
        "title": title,
        "form": form,
    }
    return render(request, "home.html", context)

@login_required
def list_items(request):
    header = 'LIST OF ITEMS'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    context = {
        "header": header,
        "queryset": queryset,
        "form": form,
    }
    if request.method == 'POST':
        queryset = Stock.objects.filter(category__icontains=form['category'].value(),
                                   item_name__icontains=form['item_name'].value()
                                    )
                                    
        context = {
        "form": form,
        "header": header,
        "queryset": queryset,
        }
    import ipdb;ipdb.set_trace()
    return render(request, "list_items.html", context)

@login_required
def add_items(request):
    form = StockCreateForm(request.POST or None)
    stock = Stock.objects.all().values()
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Saved')
        return redirect('/list_items')
    context = {
        "form": form,
        "title": "Add Item",
        "stock": stock
    }
    return render(request, "add_items.html", context)    

@login_required
def update_items(request, pk):
    queryset = Stock.objects.get(item_name=pk)
    stock = {
        "item_name": queryset.item_name,
        "price": queryset.price,
        "quantity": queryset.quantity
    }
    stock_list = []
    stock_list.append(stock)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save(), messages.success(request, 'Successfully Updated')
            return redirect('/list_items')

    context = {
        'form':form,
        'stock':stock_list
    }
    return render(request, 'add_items.html', context)
    
@login_required	
def delete_items(request, pk):
    queryset = Stock.objects.get(item_name=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Deleted Successfully')
        return redirect('/list_items')
    return render(request, 'delete_items.html')        

def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        "queryset": queryset,
    }
    return render(request, "stock_detail.html", context)


@login_required
def issue_items(request):
    data = request.GET.dict()
    Product_id = list(data.keys())
    pk_list = clean_keys_data(Product_id)
    for keys, values in data.items():
        quantity_list = [values for values in data.values()]
    clean_list = []
    unwanted_list = []
    
    total_transacted = quantity_list.pop()
    
    update_stock_on_issue(pk_list,quantity_list, request,total_transacted)
    
    return redirect("/list_items/")
    context = {
        "title": "Issue " + str(queryset.item_name),
        "queryset": queryset,
        "form": form,
        "username": "Issue By: " + str(request.user),
    }
    return render(request, "add_items.html", context)



class RouteFormView(FormView):
    template_name = 'route.html'
    form_class = ExpenseForm
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            pk_list = []
            unwanted_data = ["vehicle_number", "lap_number"]
            for items in unwanted_data:
                del form.cleaned_data[items]
            pk_list = []
            quantity_list = []
            for key, value in form.cleaned_data.items():
                pk_list.append(key)
                quantity_list.append(value)
            update_stock_on_issue(pk_list, quantity_list, request, 0)
            context = {"Message":"Route form saved"}
            return render(request,"route.html", context)
        form = self.form_class()
        context = { "form": form }
        return render(request, "route.html", context)
    
@login_required
def list_history(request):
    header = 'LIST OF ITEMS'
    queryset = StockHistory.objects.all()
    context = {
        "header": header,
        "queryset": queryset,
    }
    return render(request, "list_history.html",context)

@login_required
def report(request):
    data = Transaction.objects.values("product_ids")
    product_id_list = [items["product_ids"] for items in data]
    product_id_list = [items.split(",") for items in product_id_list]
    #  get names of all products transacted 
    name = get_product_name(product_id_list)
    # get count of all products transacted 
    count_data = Transaction.objects.values("items_count")
    item_count = [items["items_count"] for items in count_data]
    item_count = [items.split(", ") for items in item_count]
    count = get_product_count(item_count)
    # data =Transaction.objects.values('item_name').annotate(Sum('transaction_amount'))
    # categories = [items["item_name"] for items in data]
    # user_count = User.objects.all().count()
    # prices = [items["transaction_amount__sum"] for items in data]
    # total_sales = sum(prices)
    # print(data, categories, prices)
    # {'categories':json.dumps(categories), 'prices':json.dumps(prices), 'user_count':json.dumps(user_count),'total_sales':json.dumps(total_sales) }
    return render(request, "report-1.html")

@login_required
def add_to_cart(request):
    # form = IssueForm()
    employee_name = request.user.username
    data = request.GET.dicts()
    
    # Product = Stock.objects.filter(pk=pk)
    # price = Product.get().price
    # product_name = Product.get().item_name
    # order_item = Order.objects.get_or_create(id=Stock.objects.get(id=pk),employee_name=employee_name, product_name=product_name, price=price, is_complete=False)
    # order_query = Order.objects.filter(employee_name=employee_name, is_complete=0)
    # order_list = [items for items in order_query.values()]
    # queryset = Stock.objects.all()
    # pk_list = [items["id_id"] for items in order_list]
    # context = {
    #     "form": form,
    # }
    # messages.info(request, f"item added to cart ")
    return render(request, "list_items.html", { 'order_list':order_list, 'queryset':queryset, 'pk_list':pk_list, "form":form })

@login_required
def delete_from_cart(request, id):
    Product = Order.objects.filter(id_id=id)
    Product.delete()
    employee_name = request.user.username
    # import ipdb; ipdb.set_trace()
    order_item = Order.objects.all()
    order_query = Order.objects.filter(employee_name=employee_name, is_complete=0)
    order_list = [items for items in order_query.values()]
    queryset = Stock.objects.all()
    pk_list = [items["id_id"] for items in order_list]


    for pk in pk_list:
        queryset = Stock.objects.get(item_name=pk)
        instance = queryset    
        instance.issue_quantity = quantity_list[pk_list.index(pk)]
        instance.quantity -= int(instance.issue_quantity)
        instance.issue_by = str(request.user)
        messages.success(
            request,
            "Issued SUCCESSFULLY. "
            + str(instance.quantity)
            + " "
            + str(instance.item_name)
            + "s now left in Store",
        )
        instance.save()
    
    sell_transaction = Transaction(
        employee_name= request.user.username,
        transaction_amount= total_transacted,
        timestamp= date.today(),
        product_ids= ','.join(pk_list),
        items_count= ','.join(quantity_list)
    )
    sell_transaction.save()
    messages.info(request, f"item added to cart ")
    return render(request, "list_items.html", { 'order_list':order_list, 'queryset':queryset, 'pk_list':pk_list })

def clean_keys_data(list):
    new_list = []
    "removing 'a[' from items in the keys list "

    for items in list:
        data = items.replace("a[", "")
        new_list.append(data)
    
    clean_list = []
    "removing ']' from items in new list "
    for items in new_list:
        data = items.replace("]", "")
        clean_list.append(data)
    clean_list.pop()
    return clean_list 

def get_product_name(products_list):
    # generate product names from a list of product ids
    name = []
    for items in products_list:
        for id in items:
            name.append(Stock.objects.filter(item_name= id))
    
    return name
def get_product_count(products_list):
    # generate product count list
    counts = []
    for items in products_list:
        for count in items:
            counts.append(count)
    return count

def update_stock_on_issue(pk_list, quantity_list, request, total_transacted):
    for (index, pk) in enumerate(pk_list):
        if quantity_list[index] == 0:
            print("item not updated")
        else:
            queryset = Stock.objects.get(item_name=pk.replace("_", " "))
            instance = queryset    
            instance.issue_quantity = quantity_list[pk_list.index(pk)]
            instance.quantity -= int(instance.issue_quantity)
            instance.issue_by = str(request.user)
            messages.success(
                request,
                "Issued SUCCESSFULLY. "
                + str(instance.quantity)
                + " "
                + str(instance.item_name)
                + "s now left in Store",
            )
            print("item updated")
            instance.save()
    if total_transacted == 0:
        pass
    else:
        sell_transaction = Transaction(
            employee_name= request.user.username,
            transaction_amount= total_transacted,
            timestamp= date.today(),
            product_ids= ','.join(pk_list),
            items_count= ','.join(quantity_list)
        )
        return sell_transaction.save()