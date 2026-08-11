#!/usr/bin/env bash
# Oracle Cloud VM 배포 스크립트 — 서버에서 실행
#   ssh ubuntu@<IP> 'bash -s' < judge/deploy_oracle.sh
set -e

APP=~/algo-hub
PORT=12014

echo "── 1. repo 갱신 ──"
cd "$APP" && git pull -q && git log --oneline -1

echo
echo "── 2. algo-hub 서비스 등록 ──"
sudo tee /etc/systemd/system/algo-hub.service >/dev/null <<EOF
[Unit]
Description=algo-hub (채점 + repo 저장)
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=$APP
Environment=PYTHONIOENCODING=utf-8
Environment=PYTHONUNBUFFERED=1
ExecStart=/usr/bin/python3 $APP/judge/server.py --port $PORT --quiet
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

echo
echo "── 3. cloudflare 터널 서비스 등록 ──"
# quick tunnel: 계정·도메인 불필요. URL 은 재시작마다 바뀌므로 로그에서 읽어 publish 한다.
sudo tee /etc/systemd/system/algo-tunnel.service >/dev/null <<EOF
[Unit]
Description=cloudflared quick tunnel for algo-hub
After=network.target algo-hub.service

[Service]
Type=simple
User=ubuntu
ExecStart=/usr/bin/cloudflared tunnel --no-autoupdate --url http://127.0.0.1:$PORT
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now algo-hub.service algo-tunnel.service >/dev/null 2>&1
sleep 6

echo
echo "── 4. 상태 ──"
systemctl is-active algo-hub.service  | sed 's/^/  algo-hub  : /'
systemctl is-active algo-tunnel.service | sed 's/^/  algo-tunnel: /'
echo
echo "  로컬 응답:"
curl -s --max-time 5 "http://127.0.0.1:$PORT/" | head -c 300
echo
echo
echo "── 5. 터널 URL ──"
for i in $(seq 1 20); do
  U=$(journalctl -u algo-tunnel.service --since "-3min" --no-pager 2>/dev/null \
      | grep -oE 'https://[a-z0-9-]+\.trycloudflare\.com' | tail -1)
  [ -n "$U" ] && break
  sleep 3
done
if [ -n "$U" ]; then
  echo "  $U"
  echo "$U" > "$APP/.tunnel_url"
else
  echo "  ⚠️ URL 을 아직 못 찾음 — journalctl -u algo-tunnel -f 로 확인"
fi
