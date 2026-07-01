#!/usr/bin/env bash
# ── Первичный запуск «Дари Уют» с выпуском TLS-сертификата Let's Encrypt ──────
#
# Запускать ОДИН РАЗ на сервере после того, как:
#   1) заполнен .env (см. .env.example);
#   2) DNS домена указывает A-записью на IP этого сервера.
#
#   chmod +x init-letsencrypt.sh
#   ./init-letsencrypt.sh
#
# Скрипт решает проблему «курицы и яйца»: nginx не стартует без сертификата,
# а сертификат нельзя выпустить без работающего nginx. Поэтому сначала кладём
# временный самоподписанный сертификат, поднимаем nginx, затем заменяем его
# настоящим. Дальнейшее продление делает сервис `certbot` из docker-compose.
set -euo pipefail

# Домены — ДОЛЖНЫ совпадать с server_name в nginx/conf.d/dariyut.conf.
# дари-уют.рф в punycode:
DOMAINS=(xn----7sblr3bog2g.xn--p1ai www.xn----7sblr3bog2g.xn--p1ai)
RSA_KEY_SIZE=4096

cd "$(dirname "$0")"

if [ ! -f .env ]; then
  echo "✖ Нет файла .env. Скопируйте .env.example в .env и заполните значения." >&2
  exit 1
fi

CERTBOT_EMAIL=$(grep -E '^CERTBOT_EMAIL=' .env | head -n1 | cut -d= -f2- \
  | tr -d '\r' | sed 's/^["'\'']//; s/["'\'']$//')
if [ -z "${CERTBOT_EMAIL:-}" ]; then
  echo "✖ CERTBOT_EMAIL не задан в .env." >&2
  exit 1
fi

primary="${DOMAINS[0]}"
cert_dir="/etc/letsencrypt/live/$primary"

echo "### 1/6 Собираю образы и поднимаю db / backend / frontend…"
docker compose up -d --build db backend frontend

echo "### 2/6 Кладу временный самоподписанный сертификат для $primary…"
docker compose run --rm --entrypoint "\
  sh -c 'mkdir -p $cert_dir && \
    openssl req -x509 -nodes -newkey rsa:$RSA_KEY_SIZE -days 1 \
      -keyout $cert_dir/privkey.pem \
      -out    $cert_dir/fullchain.pem \
      -subj   /CN=localhost'" certbot

echo "### 3/6 Запускаю nginx (он слушает :80/:443)…"
docker compose up -d nginx

echo "### 4/6 Удаляю временный сертификат…"
docker compose run --rm --entrypoint "\
  sh -c 'rm -rf /etc/letsencrypt/live/$primary \
               /etc/letsencrypt/archive/$primary \
               /etc/letsencrypt/renewal/$primary.conf'" certbot

echo "### 5/6 Запрашиваю настоящий сертификат Let's Encrypt…"
domain_args=""
for d in "${DOMAINS[@]}"; do domain_args="$domain_args -d $d"; done
docker compose run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
    $domain_args \
    --email $CERTBOT_EMAIL --agree-tos --no-eff-email \
    --rsa-key-size $RSA_KEY_SIZE --non-interactive --force-renewal" certbot

echo "### 6/6 Перезагружаю nginx и поднимаю сервис автопродления…"
docker compose exec nginx nginx -s reload
docker compose up -d          # доводит стек до полного состава (в т.ч. certbot)

echo ""
echo "✔ Готово."
echo "  Сайт:    https://$primary"
echo "  Админка: https://$primary/admin"
echo ""
echo "Продление сертификата происходит автоматически (сервис certbot)."
