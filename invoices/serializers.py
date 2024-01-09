from rest_framework import serializers
from .models import Invoice, InvoiceDetail

class InvoiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetail
        fields = ['description', 'quantity', 'unit_price', 'price']

class InvoiceSerializer(serializers.ModelSerializer):
    invoice_details = InvoiceDetailSerializer(many=True, required=False)

    class Meta:
        model = Invoice
        fields = '__all__'

    def create(self, validated_data):
        invoice_details_data = validated_data.pop('invoice_details', [])
        invoice = Invoice.objects.create(**validated_data)

        for detail_data in invoice_details_data:
            InvoiceDetail.objects.create(invoice=invoice, **detail_data)

        return invoice
    
    def update(self, instance, validated_data):
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.save()

        invoice_details_data = validated_data.get('invoice_details', [])
        invoice_details_data_ids = [item.get('id', None) for item in invoice_details_data]

        # Delete InvoiceDetails not included in the update
        for detail in instance.invoice_details.all():
            if detail.id not in invoice_details_data_ids:
                detail.delete()

        # Update or create InvoiceDetails
        for detail_data in invoice_details_data:
            detail_id = detail_data.get('id', None)
            if detail_id is not None:
                detail = InvoiceDetail.objects.get(id=detail_id)
                detail.description = detail_data.get('description', detail.description)
                detail.quantity = detail_data.get('quantity', detail.quantity)
                detail.unit_price = detail_data.get('unit_price', detail.unit_price)
                detail.save()
            else:
                InvoiceDetail.objects.create(invoice=instance, **detail_data)

        return instance