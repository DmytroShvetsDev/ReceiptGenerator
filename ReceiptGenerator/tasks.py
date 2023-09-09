import base64
import json
import os
from typing import Any

import requests
from celery import shared_task
from django.template.loader import render_to_string

from ReceiptGenerator.settings import ROOT_PDF_DIRECTORY
from receipt.models import Receipt, STATUS_RENDERED
from dotenv import load_dotenv


load_dotenv()


@shared_task
def produce_receipt(receipt_id: int) -> None:
    receipt = Receipt.objects.get(pk=receipt_id)

    point_id = receipt.order.get("point_id")
    order_id = receipt.order.get("order_number")

    total = calculate_order_total(receipt.order.get("order_data"))
    html_content = generate_html_content(
        order_id,
        receipt.type,
        receipt.order.get("order_data"),
        point_id,
        total,
    )

    point_directory = os.path.join(ROOT_PDF_DIRECTORY, f"point_{point_id}")
    os.makedirs(point_directory, exist_ok=True)

    pdf_filename = f"{order_id}_{receipt.type}.pdf"
    pdf_file_path = os.path.join(point_directory, pdf_filename)

    generate_pdf(pdf_file_path, html_content)
    receipt.pdf_file.name = pdf_file_path
    receipt.status = STATUS_RENDERED
    receipt.save()


def generate_pdf(target_path: str, html_content: str) -> None:

    docker_host = os.environ["WKHTMLTOPDF_DOCKER_HOST"]
    docker_port = os.environ["WKHTMLTOPDF_DOCKER_PORT"]

    url = f"http://{docker_host}:{docker_port}/"
    data = {
        "contents": base64.b64encode(html_content.encode()).decode(),
    }
    headers = {
        "Content-Type": "application/json",
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:

        with open(target_path, "wb") as pdf_file:
            pdf_file.write(response.content)

    else:
        raise RuntimeError("PDF generation failure")


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


def calculate_order_total(order_data: list[dict[str, Any]]) -> int:
    total = 0

    for item in order_data:
        price = item.get("price", 0)
        count = item.get("count", 0)
        total += price * count

    return total
