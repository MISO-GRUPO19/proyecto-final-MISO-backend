#!/bin/bash

ENDPOINT="https://nginx-service-230506421700.us-central1.run.app/orders"
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NTE4Njc1OCwianRpIjoiYWVlYmYyODMtM2ExMi00ZDMzLWFiZjgtYzg3MzRjMjg0NjcxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImNlN2NkYzA1LTBhOGUtNDVjMS1hYmQzLTI3YWU2ZDRiZGM0ZiIsIm5iZiI6MTc0NTE4Njc1OCwiY3NyZiI6IjE2ZjBmMDk2LTAwMTYtNDBkZi1iYzU3LTQ0NjI3ZTYzYzQ4ZCIsImV4cCI6MTc0NTE4NzY1OH0.oQHsIXIp_EFQQrn0R_stioI558VldP8ocKEsARpa1vo"

HEADERS=(-H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json")

declare -a BODIES=(
'{
  "client_id": "65c2537c-fb0e-4c77-b61b-576ba47e40a2",
  "seller_id": "442e301f-f35e-47d6-b6bb-917738e37ed0",
  "date": "2023-10-01T00:00:00",
  "provider_id": "697d7c97-ac98-4179-a89d-57fe3d1c7c3a",
  "total": 23.5,
  "type": "CLIENTE",
  "route_id": "123e4567-e89b-12d3-a456-426614174003",
  "products": [
    {"barcode": "7702011555555", "quantity": 3},
    {"barcode": "7702011999999", "quantity": 4},
    {"barcode": "7702011444444", "quantity": 1},
    {"barcode": "7702011111111", "quantity": 2}
  ]
}'
'{
  "client_id": "65c2537c-fb0e-4c77-b61b-576ba47e40a2",
  "seller_id": "442e301f-f35e-47d6-b6bb-917738e37ed0",
  "date": "2023-10-02T00:00:00",
  "provider_id": "697d7c97-ac98-4179-a89d-57fe3d1c7c3a",
  "total": 12.4,
  "type": "CLIENTE",
  "route_id": "123e4567-e89b-12d3-a456-426614174003",
  "products": [
    {"barcode": "7702011444444", "quantity": 3},
    {"barcode": "7702011111111", "quantity": 2}
  ]
}'
'{
  "client_id": "65c2537c-fb0e-4c77-b61b-576ba47e40a2",
  "seller_id": "442e301f-f35e-47d6-b6bb-917738e37ed0",
  "date": "2023-10-03T00:00:00",
  "provider_id": "697d7c97-ac98-4179-a89d-57fe3d1c7c3a",
  "total": 27.9,
  "type": "CLIENTE",
  "route_id": "123e4567-e89b-12d3-a456-426614174003",
  "products": [
    {"barcode": "7702011777777", "quantity": 5},
    {"barcode": "7702011999999", "quantity": 4},
    {"barcode": "7702011444444", "quantity": 1},
    {"barcode": "7702011888888", "quantity": 2}
  ]
}'
'{
  "client_id": "65c2537c-fb0e-4c77-b61b-576ba47e40a2",
  "seller_id": "442e301f-f35e-47d6-b6bb-917738e37ed0",
  "date": "2023-10-04T00:00:00",
  "provider_id": "697d7c97-ac98-4179-a89d-57fe3d1c7c3a",
  "total": 20.1,
  "type": "CLIENTE",
  "route_id": "123e4567-e89b-12d3-a456-426614174003",
  "products": [
    {"barcode": "7702011777777", "quantity": 2},
    {"barcode": "7702011666666", "quantity": 1},
    {"barcode": "7702011555555", "quantity": 4}
  ]
}'
'{
  "client_id": "65c2537c-fb0e-4c77-b61b-576ba47e40a2",
  "seller_id": "442e301f-f35e-47d6-b6bb-917738e37ed0",
  "date": "2023-10-05T00:00:00",
  "provider_id": "697d7c97-ac98-4179-a89d-57fe3d1c7c3a",
  "total": 14.1,
  "type": "CLIENTE",
  "route_id": "123e4567-e89b-12d3-a456-426614174003",
  "products": [
    {"barcode": "7702011888888", "quantity": 1},
    {"barcode": "7702011777777", "quantity": 4}
  ]
}'
'{
  "client_id": "65c2537c-fb0e-4c77-b61b-576ba47e40a2",
  "seller_id": "442e301f-f35e-47d6-b6bb-917738e37ed0",
  "date": "2023-10-06T00:00:00",
  "provider_id": "697d7c97-ac98-4179-a89d-57fe3d1c7c3a",
  "total": 35.5,
  "type": "CLIENTE",
  "route_id": "123e4567-e89b-12d3-a456-426614174003",
  "products": [
    {"barcode": "7702011444444", "quantity": 4},
    {"barcode": "7702011666666", "quantity": 3},
    {"barcode": "7702011999999", "quantity": 5},
    {"barcode": "7702011222222", "quantity": 5}
  ]
}'
'{
  "client_id": "65c2537c-fb0e-4c77-b61b-576ba47e40a2",
  "seller_id": "442e301f-f35e-47d6-b6bb-917738e37ed0",
  "date": "2023-10-07T00:00:00",
  "provider_id": "697d7c97-ac98-4179-a89d-57fe3d1c7c3a",
  "total": 12.2,
  "type": "CLIENTE",
  "route_id": "123e4567-e89b-12d3-a456-426614174003",
  "products": [
    {"barcode": "7702011888888", "quantity": 2},
    {"barcode": "7702011777777", "quantity": 1},
    {"barcode": "7702011555555", "quantity": 1}
  ]
}'
'{
  "client_id": "65c2537c-fb0e-4c77-b61b-576ba47e40a2",
  "seller_id": "442e301f-f35e-47d6-b6bb-917738e37ed0",
  "date": "2023-10-08T00:00:00",
  "provider_id": "697d7c97-ac98-4179-a89d-57fe3d1c7c3a",
  "total": 38.9,
  "type": "CLIENTE",
  "route_id": "123e4567-e89b-12d3-a456-426614174003",
  "products": [
    {"barcode": "7702011222222", "quantity": 3},
    {"barcode": "7702011999999", "quantity": 3},
    {"barcode": "7702011777777", "quantity": 5},
    {"barcode": "7702011111111", "quantity": 4}
  ]
}'
'{
  "client_id": "65c2537c-fb0e-4c77-b61b-576ba47e40a2",
  "seller_id": "442e301f-f35e-47d6-b6bb-917738e37ed0",
  "date": "2023-10-09T00:00:00",
  "provider_id": "697d7c97-ac98-4179-a89d-57fe3d1c7c3a",
  "total": 24.9,
  "type": "CLIENTE",
  "route_id": "123e4567-e89b-12d3-a456-426614174003",
  "products": [
    {"barcode": "7702011444444", "quantity": 2},
    {"barcode": "7702011666666", "quantity": 5},
    {"barcode": "7702011555555", "quantity": 2}
  ]
}'
'{
  "client_id": "65c2537c-fb0e-4c77-b61b-576ba47e40a2",
  "seller_id": "442e301f-f35e-47d6-b6bb-917738e37ed0",
  "date": "2023-10-10T00:00:00",
  "provider_id": "697d7c97-ac98-4179-a89d-57fe3d1c7c3a",
  "total": 33.6,
  "type": "CLIENTE",
  "route_id": "123e4567-e89b-12d3-a456-426614174003",
  "products": [
    {"barcode": "7702011444444", "quantity": 4},
    {"barcode": "7702011999999", "quantity": 1},
    {"barcode": "7702011222222", "quantity": 3},
    {"barcode": "7702011333333", "quantity": 4}
  ]
}'
'{
  "client_id": "65c2537c-fb0e-4c77-b61b-576ba47e40a2",
  "seller_id": "442e301f-f35e-47d6-b6bb-917738e37ed0",
  "date": "2023-10-11T00:00:00",
  "provider_id": "697d7c97-ac98-4179-a89d-57fe3d1c7c3a",
  "total": 13.5,
  "type": "CLIENTE",
  "route_id": "123e4567-e89b-12d3-a456-426614174003",
  "products": [
    {"barcode": "7702011999999", "quantity": 2},
    {"barcode": "7702011111111", "quantity": 3}
  ]
}'
'{
  "client_id": "65c2537c-fb0e-4c77-b61b-576ba47e40a2",
  "seller_id": "442e301f-f35e-47d6-b6bb-917738e37ed0",
  "date": "2023-10-12T00:00:00",
  "provider_id": "697d7c97-ac98-4179-a89d-57fe3d1c7c3a",
  "total": 15.8,
  "type": "CLIENTE",
  "route_id": "123e4567-e89b-12d3-a456-426614174003",
  "products": [
    {"barcode": "7702011999999", "quantity": 5},
    {"barcode": "7702011555555", "quantity": 1},
    {"barcode": "7702011777777", "quantity": 2}
  ]
}'
'{
  "client_id": "65c2537c-fb0e-4c77-b61b-576ba47e40a2",
  "seller_id": "442e301f-f35e-47d6-b6bb-917738e37ed0",
  "date": "2023-10-13T00:00:00",
  "provider_id": "697d7c97-ac98-4179-a89d-57fe3d1c7c3a",
  "total": 27.5,
  "type": "CLIENTE",
  "route_id": "123e4567-e89b-12d3-a456-426614174003",
  "products": [
    {"barcode": "7702011111111", "quantity": 4},
    {"barcode": "7702011888888", "quantity": 2},
    {"barcode": "7702011999999", "quantity": 1},
    {"barcode": "7702011444444", "quantity": 3}
  ]
}'
'{
  "client_id": "65c2537c-fb0e-4c77-b61b-576ba47e40a2",
  "seller_id": "442e301f-f35e-47d6-b6bb-917738e37ed0",
  "date": "2023-10-14T00:00:00",
  "provider_id": "697d7c97-ac98-4179-a89d-57fe3d1c7c3a",
  "total": 31.0,
  "type": "CLIENTE",
  "route_id": "123e4567-e89b-12d3-a456-426614174003",
  "products": [
    {"barcode": "7702011111111", "quantity": 5},
    {"barcode": "7702011333333", "quantity": 3}
  ]
}'
'{
  "client_id": "65c2537c-fb0e-4c77-b61b-576ba47e40a2",
  "seller_id": "442e301f-f35e-47d6-b6bb-917738e37ed0",
  "date": "2023-10-15T00:00:00",
  "provider_id": "697d7c97-ac98-4179-a89d-57fe3d1c7c3a",
  "total": 28.1,
  "type": "CLIENTE",
  "route_id": "123e4567-e89b-12d3-a456-426614174003",
  "products": [
    {"barcode": "7702011333333", "quantity": 4},
    {"barcode": "7702011111111", "quantity": 2},
    {"barcode": "7702011666666", "quantity": 1}
  ]
}'
'{
  "client_id": "65c2537c-fb0e-4c77-b61b-576ba47e40a2",
  "seller_id": "442e301f-f35e-47d6-b6bb-917738e37ed0",
  "date": "2023-10-16T00:00:00",
  "provider_id": "697d7c97-ac98-4179-a89d-57fe3d1c7c3a",
  "total": 18.0,
  "type": "CLIENTE",
  "route_id": "123e4567-e89b-12d3-a456-426614174003",
  "products": [
    {"barcode": "7702011888888", "quantity": 5},
    {"barcode": "7702011999999", "quantity": 1}
  ]
}'
'{
  "client_id": "65c2537c-fb0e-4c77-b61b-576ba47e40a2",
  "seller_id": "442e301f-f35e-47d6-b6bb-917738e37ed0",
  "date": "2023-10-17T00:00:00",
  "provider_id": "697d7c97-ac98-4179-a89d-57fe3d1c7c3a",
  "total": 23.8,
  "type": "CLIENTE",
  "route_id": "123e4567-e89b-12d3-a456-426614174003",
  "products": [
    {"barcode": "7702011888888", "quantity": 4},
    {"barcode": "7702011999999", "quantity": 1},
    {"barcode": "7702011666666", "quantity": 2},
    {"barcode": "7702011555555", "quantity": 1}
  ]
}'
'{
  "client_id": "65c2537c-fb0e-4c77-b61b-576ba47e40a2",
  "seller_id": "442e301f-f35e-47d6-b6bb-917738e37ed0",
  "date": "2023-10-18T00:00:00",
  "provider_id": "697d7c97-ac98-4179-a89d-57fe3d1c7c3a",
  "total": 16.1,
  "type": "CLIENTE",
  "route_id": "123e4567-e89b-12d3-a456-426614174003",
  "products": [
    {"barcode": "7702011333333", "quantity": 1},
    {"barcode": "7702011555555", "quantity": 4}
  ]
}'
'{
  "client_id": "65c2537c-fb0e-4c77-b61b-576ba47e40a2",
  "seller_id": "442e301f-f35e-47d6-b6bb-917738e37ed0",
  "date": "2023-10-19T00:00:00",
  "provider_id": "697d7c97-ac98-4179-a89d-57fe3d1c7c3a",
  "total": 36.7,
  "type": "CLIENTE",
  "route_id": "123e4567-e89b-12d3-a456-426614174003",
  "products": [
    {"barcode": "7702011000000", "quantity": 3},
    {"barcode": "7702011999999", "quantity": 5},
    {"barcode": "7702011777777", "quantity": 2},
    {"barcode": "7702011111111", "quantity": 5}
  ]
}'
'{
  "client_id": "65c2537c-fb0e-4c77-b61b-576ba47e40a2",
  "seller_id": "442e301f-f35e-47d6-b6bb-917738e37ed0",
  "date": "2023-10-20T00:00:00",
  "provider_id": "697d7c97-ac98-4179-a89d-57fe3d1c7c3a",
  "total": 27.9,
  "type": "CLIENTE",
  "route_id": "123e4567-e89b-12d3-a456-426614174003",
  "products": [
    {"barcode": "7702011888888", "quantity": 4},
    {"barcode": "7702011777777", "quantity": 2},
    {"barcode": "7702011666666", "quantity": 3}
  ]
}'
)

for BODY in "${BODIES[@]}"; do
  echo "Enviando orden de compra..."
  curl -s -X POST "$ENDPOINT" "${HEADERS[@]}" -d "$BODY"
  echo -e "\n✅ Orden enviada\n"
done