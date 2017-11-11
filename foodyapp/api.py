import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.models import AccessToken

from foodyapp.models import Restaurant, Meal, Order, OrderDetails
from foodyapp.serializers import RestaurantSerializer, MealSerializer, OrderSerializer

from django.utils import timezone

###################
#CUSTOMERS
###################
def customer_get_restaurants(request):
    restaurants = RestaurantSerializer(
        Restaurant.objects.all().order_by("-id"),
        many = True,
        context = {"request": request}
    ).data

    return JsonResponse({"restaurants":restaurants})

def customer_get_meals(request, restaurant_id):
    meals = MealSerializer(
        Meal.objects.filter(restaurant_id = restaurant_id).order_by("-id"),
        many = True,
        context = {"request": request}
    ).data

    return JsonResponse({"meals": meals})

@csrf_exempt
def customer_add_order(request):
    """
        params:
            access_token
            restaurant_id
            address
            order_details  (json format), example:
                [{"meal_id": 1, "quantity": 2},{"meal_id": 2, "quantity": 3}]
            stripe_token

        return {"status": "success"}

    """
    if request.method =="POST":
        #GET TOKEN
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
            expires__gt = timezone.now())

        #GET Profile
        customer = access_token.user.customer

        #Check whether customer has any order that is not delivered
        if Order.objects.filter(customer=customer).exclude(status= Order.DELIVERED):
            return JsonResponse({"status":"failed", "error":"Your last order must be completed."})

        #Check the address
        if not request.POST["address"]:
            return JsonResponse({"status":"failed", "error": "Address is required."})

        #Get Order Details
        order_details = json.loads(request.POST["order_details"])

        order_total = 0
        for meal in order_details:
            order_total += Meal.objects.get(id = meal["meal_id"]).price * meal["quantity"]

        if len(order_details) > 0:  #This mean we do have order details#
            #Step 1 - Create Order
            order = Order.objects.create(
                customer = customer,
                restaurant_id = request.POST["restaurant_id"],
                total = order_total,
                status = Order.COOKING,
                address = request.POST["address"]
            )

            #Step 2 - Create Order Details
            for meal in order_details:
                OrderDetails.objects.create(
                    order = order,
                    meal_id = meal["meal_id"],
                    quantity = meal["quantity"],
                    sub_total = Meal.objects.get(id = meal["meal_id"]).price * meal["quantity"]
                )

            return JsonResponse({"status": "success"})

def customer_get_latest_order(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    customer = access_token.user.customer
    order = OrderSerializer(Order.objects.filter(customer = customer).last()).data


    return JsonResponse({"order": order})

##############
#Restaurant
##############
def restaurant_order_notification(request, last_request_time):
    notification = Order.objects.filter(restaurant = request.user.restaurant,
        created_at__gt = last_request_time).count()
    return JsonResponse({"notification": notification})


#############
#DRIVERS
#############

def driver_get_ready_orders(request):
    orders = OrderSerializer(
        Order.objects.filter(status = Order.READY, driver = None).order_by("-id"),
        many=True
    ).data
    return JsonResponse({"orders": orders})

@csrf_exempt
# POST params: access_token, order_id
def driver_pick_order(request):

    if request.method == "POST":
        #Get Token
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
            expires__gt = timezone.now())
        #Get Driver
        driver = access_token.user.driver

        # Check if driver can only pick up one order at a time.
        if Order.objects.filter(driver = driver).exclude(status = Order.ONTHEWAY):
            return JsonResponse({"status":"failed","Error":"You can only pick one order at the same time. "})

        try:
            order = Order.objects.get(
                id = request.POST["order_id"],
                driver = None,
                status = Order.READY
            )
            order.driver = driver
            order.status = Order.ONTHEWAY
            order.picked_at = timezone.now()
            order.save()

            return JsonResponse({"status": "success"})

        # Only one can pick this order when that driver has saved the order above.
        except Order.DoesNotExist:
            return JsonResponse({"status": "failed", "error": "This order has been picked up by another!"})

    return JsonResponse({})

#get params: access_token
def driver_get_latest_order(request):
    #Get Token
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())
        #Get Driver
    driver = access_token.user.driver

    order = OrderSerializer(
        Order.objects.filter(driver = driver).order_by("picked_at").last()
    ).data

    return JsonResponse({"order": order})


def driver_get_complete_order(request):
    return JsonResponse({})

def driver_get_revenue(request):
    return JsonResponse({})
