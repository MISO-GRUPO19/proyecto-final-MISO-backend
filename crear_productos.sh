#!/bin/bash

ENDPOINT="http://127.0.0.1:8080/products"
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NTI4MTQzMiwianRpIjoiNTVhOGM2NTUtMTQwMi00NzMyLWIxMTItMjExODZhNzNiYWE4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImEzZjQ4YWE3LWY2OGUtNDkyMy04ZTQ3LTBkNDJlN2QwMjNlYiIsIm5iZiI6MTc0NTI4MTQzMiwiY3NyZiI6IjVjN2RmMzYzLTNlMzAtNGRiNS1iZDUzLTIzNzMxZjY2MTVjMCIsImV4cCI6MTc0NTI4MjMzMn0.e98ZUh62gnjhe2Gq1SVXejZ2EVoRgQAWsfo-BfsrGO8"

HEADERS=(-H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json")

declare -a BODIES=(
'{
  "name": "Galleta Festival Fresa",
  "description": "Galletas rellenas con sabor a fresa",
  "price": 2.5,
  "category": "Snacks y Dulces",
  "weight": 0.15,
  "barcode": "7702011111111",
  "provider_id": "c9953c9a-846e-4542-8a87-bd38ee478177",
  "batch": "Batch001",
  "best_before": "2025-12-31T23:59:59",
  "quantity": 100
}'
'{
  "name": "Bon Bon Bum Mora",
  "description": "Bombón con chicle sabor mora",
  "price": 0.8,
  "category": "Snacks y Dulces",
  "weight": 0.03,
  "barcode": "7702011222222",
  "provider_id": "c9953c9a-846e-4542-8a87-bd38ee478177",
  "batch": "Batch002",
  "best_before": "2025-11-30T23:59:59",
  "quantity": 200
}'
'{
  "name": "Chocobreak Leche",
  "description": "Chocolate de leche Colombina",
  "price": 1.5,
  "category": "Snacks y Dulces",
  "weight": 0.05,
  "barcode": "7702011333333",
  "provider_id": "c9953c9a-846e-4542-8a87-bd38ee478177",
  "batch": "Batch003",
  "best_before": "2026-01-15T23:59:59",
  "quantity": 150
}'
'{
  "name": "Galletas Ducales",
  "description": "Galletas saladas clásicas",
  "price": 3.0,
  "category": "Panadería y Repostería",
  "weight": 0.2,
  "barcode": "7702011444444",
  "provider_id": "c9953c9a-846e-4542-8a87-bd38ee478177",
  "batch": "Batch004",
  "best_before": "2025-10-10T23:59:59",
  "quantity": 80
}'
'{
  "name": "Mentas Spicy",
  "description": "Caramelos mentolados picantes",
  "price": 0.9,
  "category": "Snacks y Dulces",
  "weight": 0.02,
  "barcode": "7702011555555",
  "provider_id": "c9953c9a-846e-4542-8a87-bd38ee478177",
  "batch": "Batch005",
  "best_before": "2025-09-01T23:59:59",
  "quantity": 300
}'
'{
  "name": "Arequipe Colombina",
  "description": "Arequipe tradicional en envase individual",
  "price": 1.2,
  "category": "Lácteos y Huevos",
  "weight": 0.1,
  "barcode": "7702011666666",
  "provider_id": "c9953c9a-846e-4542-8a87-bd38ee478177",
  "batch": "Batch006",
  "best_before": "2025-12-01T23:59:59",
  "quantity": 250
}'
'{
  "name": "Gomitas Fruticas",
  "description": "Gomitas surtidas con sabor a frutas",
  "price": 1.7,
  "category": "Snacks y Dulces",
  "weight": 0.08,
  "barcode": "7702011777777",
  "provider_id": "c9953c9a-846e-4542-8a87-bd38ee478177",
  "batch": "Batch007",
  "best_before": "2025-08-20T23:59:59",
  "quantity": 120
}'
'{
  "name": "Chocolatina Jet",
  "description": "Chocolatina con tarjeta coleccionable",
  "price": 1.0,
  "category": "Snacks y Dulces",
  "weight": 0.03,
  "barcode": "7702011888888",
  "provider_id": "c9953c9a-846e-4542-8a87-bd38ee478177",
  "batch": "Batch008",
  "best_before": "2026-01-01T23:59:59",
  "quantity": 180
}'
'{
  "name": "Colombina Coffee Delight",
  "description": "Caramelo sabor café",
  "price": 0.95,
  "category": "Snacks y Dulces",
  "weight": 0.02,
  "barcode": "7702011999999",
  "provider_id": "c9953c9a-846e-4542-8a87-bd38ee478177",
  "batch": "Batch009",
  "best_before": "2025-07-15T23:59:59",
  "quantity": 220
}'
'{
  "name": "Mini Chocoramo",
  "description": "Ponqué con cobertura de chocolate",
  "price": 1.8,
  "category": "Panadería y Repostería",
  "weight": 0.07,
  "barcode": "7702012000001",
  "provider_id": "c9953c9a-846e-4542-8a87-bd38ee478177",
  "batch": "Batch010",
  "best_before": "2025-09-10T23:59:59",
  "quantity": 140
}'
)

for BODY in "${BODIES[@]}"; do
  echo "Enviando producto..."
  curl -s -X POST "$ENDPOINT" "${HEADERS[@]}" -d "$BODY"
  echo -e "\n✅ Producto enviado\n"
done
