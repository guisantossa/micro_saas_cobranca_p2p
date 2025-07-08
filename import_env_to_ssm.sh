#!/bin/bash

echo "🔍 Lendo arquivo .env..."
echo "--------------------------"

while IFS='=' read -r raw_line
do
  # Ignorar linhas em branco ou comentário
  [[ "$raw_line" =~ ^#.*$ || -z "$raw_line" ]] && continue

  key=$(echo "$raw_line" | cut -d '=' -f 1 | tr -d '\r' | xargs)
  value=$(echo "$raw_line" | cut -d '=' -f 2- | tr -d '\r' | xargs)

  param_name="/cobraii/prod/$key"
  echo "➡️  Enviando: $param_name=$value"

  aws ssm put-parameter \
    --name "$param_name" \
    --value "$value" \
    --type "String" \
    --overwrite \
    --region us-east-2

done < .env

echo "✅ Concluído."
