import base64
import json
import os
from typing import Any

import requests
from celery import shared_task
from django.template.loader import render_to_string

from receipt.models import Receipt


@shared_task
def produce_receipt(receipt_id):
    receipt = Receipt.objects.get(pk=receipt_id)

    total = calculate_order_total(receipt.order.get("order_data"))
    html_content = generate_html_content(
        receipt.order.get("order_number"),
        receipt.type,
        receipt.order.get("order_data"),
        receipt.order.get("point_id"),
        total,
    )
    pdf_path = generate_pdf(
        receipt.order.get("order_number"), receipt.type, html_content
    )
    receipt.pdf_file.name = pdf_path
    receipt.status = "rendered"
    receipt.save()


def generate_pdf(order_id, check_type, html_content: str) -> str:
    html_file_path = f"/tmp/{order_id}_{check_type}.html"
    with open(html_file_path, "w") as html_file:
        html_file.write(html_content)

    docker_host = "0.0.0.0"
    docker_port = 32768

    url = f"http://{docker_host}:{docker_port}/"
    data = {
        "contents": base64.b64encode(open(html_file_path, "rb").read()).decode(),
    }
    headers = {
        "Content-Type": "application/json",
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        pdf_filename = f"{order_id}_{check_type}.pdf"
        pdf_file_path = os.path.join("media/pdf", pdf_filename)
        with open(pdf_file_path, "wb") as pdf_file:
            pdf_file.write(response.content)

        return pdf_file_path
    else:
        raise Exception("PDF generating errors")


def generate_html_content(
    order_id: str,
    check_type: str,
    order_data: list[dict[str, Any]],
    point_id: str,
    total: int,
) -> str:
    html_template_path = "receipt.html"
    html_content = render_to_string(
        html_template_path,
        {
            "order_number": order_id,
            "check_type": check_type,
            "order_data": order_data,
            "point_id": point_id,
            "total": total,
        },
    )
    return html_content


def calculate_order_total(order_data):
    total = 0

    for item in order_data:
        price = item.get("price", 0)
        count = item.get("count", 0)
        total += price * count

    return total
