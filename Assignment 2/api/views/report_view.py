from rest_framework import views
from rest_framework.response import Response

from django.utils.dateparse import parse_date
from django.shortcuts import get_object_or_404
from django.http import FileResponse

from ..models.items_model import Items
from ..models.purchases_model import PurchaseDetails
from ..models.sells_model import SellDetails

from ..utils.report_pdf import generate

class Report(views.APIView):

    def get(self, request, item_code):
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        pdf = request.GET.get("pdf") == "true"

        # Get the item
        item = get_object_or_404(Items, code=item_code)
        
        # Get all transactions of the item
        if start_date and end_date:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)

            purchases = PurchaseDetails.objects.filter(
                item_code=item,
                header_code__date__range=(start_date, end_date)
            ).select_related("header_code")

            sells = SellDetails.objects.filter(
                item_code=item,
                header_code__date__range=(start_date, end_date)
            ).select_related("header_code")
        else:
            purchases = PurchaseDetails.objects.filter(item_code=item).select_related("header_code")
            sells = SellDetails.objects.filter(item_code=item).select_related("header_code")

        # Combine purchases and sells
        transactions = list(purchases) + list(sells)

        # Sort transactions by date from the oldest to the newest
        transactions.sort(key=lambda item: item.created_at)

        report = {
            "items": [],
            "item_code": item.code,
            "name": item.name,
            "unit": item.unit,
            "summary": {
                "in_qty": 0,
                "out_qty": 0,
                "balance_qty": 0,
                "balance": 0
            }
        }

        # Generate report
        for transaction in transactions:
            # Check if the transaction is a purchase or a sell
            if isinstance(transaction, PurchaseDetails):
                transaction_type = "in"
            else:
                transaction_type = "out"

            report["items"].append({
                "date": transaction.header_code.date.strftime('%d-%m-%Y'),
                "description": transaction.header_code.description,
                "code": transaction.header_code.code,
                "in_qty": 0,
                "in_price": 0,
                "in_total": 0,
                "out_qty": 0,
                "out_price": 0,
                "out_total": 0,
                "stock_qty": [],
                "stock_price": [],
                "stock_total": [],
                "balance_qty": 0,
                "balance": 0
            })

            
            # Initial data
            if transaction_type == "in":
                report["items"][-1]["stock_price"].append( 0 if (transaction.balance_quantity - transaction.quantity) == 0 else (transaction.balance - transaction.unit_price * transaction.quantity) // (transaction.balance_quantity - transaction.quantity))
                report["items"][-1]["stock_qty"].append(transaction.balance_quantity - transaction.quantity)
                report["items"][-1]["stock_total"].append(transaction.balance - transaction.unit_price * transaction.quantity)

                report["items"][-1]["balance_qty"] = transaction.balance_quantity - transaction.quantity
                report["items"][-1]["balance"] = transaction.balance - transaction.unit_price * transaction.quantity

                report["summary"]["balance_qty"] = transaction.balance_quantity - transaction.quantity 
                report["summary"]["balance"] = transaction.balance - transaction.unit_price * transaction.quantity
            else:
                report["items"][-1]["stock_qty"].append(0)
                report["items"][-1]["stock_price"].append(0)
                report["items"][-1]["stock_total"].append(0)

                report["items"][-1]["balance_qty"] = transaction.balance_quantity + transaction.quantity
                report["items"][-1]["balance"] = transaction.balance + transaction.unit_price * transaction.quantity

                report["summary"]["balance_qty"] = transaction.balance_quantity + transaction.quantity
                report["summary"]["balance"] = transaction.balance + transaction.unit_price * transaction.quantity

            # Transaction data
            if transaction_type == "in":
                report["items"][-1]["in_price"] += ( report["items"][-1]["in_price"] * report["items"][-1]["in_qty"] + transaction.unit_price * transaction.quantity ) // ( report["items"][-1]["in_qty"] + transaction.quantity )
                report["items"][-1]["in_qty"] += transaction.quantity
                report["items"][-1]["in_total"] += transaction.quantity * transaction.unit_price

                report["items"][-1]["balance_qty"] += transaction.quantity
                report["items"][-1]["balance"] += transaction.quantity * transaction.unit_price

                report["items"][-1]["stock_qty"].append(transaction.quantity)
                report["items"][-1]["stock_price"].append(transaction.unit_price)
                report["items"][-1]["stock_total"].append(transaction.quantity * transaction.unit_price)

                report["summary"]["in_qty"] += transaction.quantity
                report["summary"]["balance_qty"] += transaction.quantity
                report["summary"]["balance"] += transaction.quantity * transaction.unit_price
            else:
                report["items"][-1]["out_price"] += (report["items"][-1]["out_price"] * report["items"][-1]["out_qty"] + transaction.unit_price * transaction.quantity) // (report["items"][-1]["out_qty"] + transaction.quantity)
                report["items"][-1]["out_qty"] += transaction.quantity
                report["items"][-1]["out_total"] += transaction.quantity * transaction.unit_price

                report["items"][-1]["balance_qty"] -= transaction.quantity
                report["items"][-1]["balance"] -= transaction.quantity * transaction.unit_price

                report["items"][-1]["stock_qty"].append(transaction.balance_quantity)
                report["items"][-1]["stock_price"].append(transaction.unit_price)
                report["items"][-1]["stock_total"].append(transaction.balance)

                report["summary"]["out_qty"] += transaction.quantity
                report["summary"]["balance_qty"] -= transaction.quantity
                report["summary"]["balance"] -= transaction.quantity * transaction.unit_price

            print(report["items"][-1]["balance"])


        # Return the report
        if not pdf:
            return Response(report)
        else:
            # Generate PDF
            buffer = generate(report)

            # Return the PDF
            response = FileResponse(buffer, as_attachment=True, filename=f"{item.code}-Report.pdf")
            return response
            
    
    def post(self, request, item_code):
        return Response({"message": "POST method is not allowed"}, status=405)
    
    def put(self, request, item_code):
        return Response({"message": "PUT method is not allowed"}, status=405)
    
    def patch(self, request, item_code):
        return Response({"message": "PATCH method is not allowed"}, status=405)

    def delete(self, request, item_code):
        return Response({"message": "DELETE method is not allowed"}, status=405)