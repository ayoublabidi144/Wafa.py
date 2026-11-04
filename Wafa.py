#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ MATRIX BOT — FINAL FIXED FOR RENDER (Web Port + Full Features)
"""

import requests, time, re, json, threading, logging, sys
import uuid, base64, os, urllib3
from urllib.parse import urlencode, urlparse, urlunparse
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup as Markup, InlineKeyboardButton as Button, LabeledPrice

# ─── تحذيرات SSL + Logger ───
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s",
                    datefmt="%H:%M:%S")
logger = logging.getLogger("matrix_bot")

# ═══════════════════════════ RENDER WEB SERVER ═══════════════════════════
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"<h1>Matrix Bot is Running Successfully 24/7!</h1>")
    def log_message(self, format, *args):
        return

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    try:
        server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        logger.info(f"🌐 Web Server listening on port {port} for Render check...")
        server.serve_forever()
    except Exception as e:
        logger.error(f"Failed to start web server: {e}")

# ═══════════════════════════ CONFIG & EMOJIS ═══════════════════════════
TELEGRAM_BOT_TOKEN = os.environ.get("BOT_TOKEN", "8230898243:AAGugbXgoEfdFHFOo9AJcEnk8M7063-l9p8")
ADMIN_ID      = int(os.environ.get("ADMIN_ID", 8952133268))
LOG_CHANNEL_ID = os.environ.get("LOG_CHANNEL_ID", "@dznet3")

ben = TeleBot(TELEGRAM_BOT_TOKEN, parse_mode="HTML")

PHOTO_WELCOME = "https://t.me/ALGprom/128"
E_ROCKET = "6221996895535896347"
E_STAR = "5938116638355231267"
E_DIAMOND = "5427168083074628963"
E_CHAN = "5456140674028019486" 

def emo(eid, c): return f'<tg-emoji emoji-id="{eid}">{c}</tg-emoji>'

def btn(text, url=None, callback_data=None, emoji_id=None, color=None):
    b = Button(text=text, url=url, callback_data=callback_data)
    if emoji_id:
        try: b.icon_custom_emoji_id = emoji_id
        except: pass
    if color:
        try: b.style = color
        except: pass
    return b

OOREDOO_BFF   = "https://apis.ooredoo.dz/api/ooredoo-bff"
OOREDOO_AUTH  = "https://apis.ooredoo.dz/api/auth/realms/myooredoo/protocol/openid-connect/token"
OOREDOO_CLIENT_ID   = "myooredoo-app"
OOREDOO_X_VERSION   = "1.5.17"
OOREDOO_X_SIG       = "5c7641dbb82cf11066df68afc91541c967640106a95192740b43d51a5ce6777a"
OOREDOO_PLATFORM         = "android"
OOREDOO_PLATFORM_ORIGIN  = "mobile-android"

OOREDOO_INTEGRITY_1 = "JWBTpxXcH7KY9EXYeIRp8NjQMx2dt3vF8ejjoARazyoFzOw6Cu8+wkeV+zSVHSTeI6a12SG/FU+Q/9uBrcN71RlYO4CulD2x375NKwJRAInar8DVUilHBKUfjEsoHd6EwfLCfdYzLNXJu9POfEf6tqKn3PUe0pY6qZxWLhyVAFHw8Qwb52ZqdI2soCH4S3mrz+OZL+YovdGSUKlXKIkxVroAMTAg3jljLF7gvXaEsB/O3uW+tbkBMwSX2uTOwf+rh3sgOF/zPhKCFgRvZmU1o87Fa96Y/+wOcK+UpfXTCBYVrvQ1wG6ryC7vHMSqgUhYJK4tbSoti0zv4av9pwxh9Iv2MgsMENjyKBK/TuFZxEG3xQCKj1LTMgn2xBEeKcbsKrEW3xDRwsccGI3D7GHnbUlhdI4ujDIRQVKHaZSwhTp+32Cr4EB/Qt8p/xRbdgCde9MUlM4AYIGlfyVoHSkOvTu5c0DIIy1EhowtAkbKIJl49wsYKWvpT/nXFWzeXP3R2qzaclCnIb9qihhrarmwz8l8XH2T+f7AK2uSNiuWLG5Fy2mM/YLmuJPZT9Ciag/mpy7JGImKNQAcFbSAInBdKQjUKT+COzZfrXj5rwil9/HDMtuzIovq8hrQGY+roTfVPheTLWmcjkVCOL8VXAHjPb22vOuqrkMioWT9CQ5O8RgW7RKHrObeKQMp8F7tSjOqkxYDFkPVN1G4nkEBrTlPKK9YtPl+j7IuH9fGcDTwhCTTqP8peuBryW0L11tApvAEi7VkJyBxpVxW"
OOREDOO_INTEGRITY_2 = "JWBTpxXcH7KR/kzaHeUUydDWODuU4i3H4fL9gCgKzyYfyN4qLJJE8keV+zSVHSTeI6aEyC2tbSza/NGmkflQ/UgaNZSN9SKxz7tcdQckHY25n6mOaDZ9PPMQmF4sKZqDwebce/c1SNGNn6qvTULW/L348aJvy7Vii6dyPTu3OSPV9AwKwGwQKNHN61HyK3jx/fa8Os5ux9u3Q654YLZrAJ99QGEm/C9nEBPmlHC98RjovLGBnuJOGx6k7fnyrt/Ogy5fNg+tBgi5HEsoXDAwutX7TOWfx4YKHpKW//TvPRQgp69e2Xqa+CvGJJ+a/WlPMPhRCSsfo0OG04mVvlkc8eXiLzV/GPuJCEmcRf9Z6V+xoDyMtU7OZ3XT5BMhI/D/N68LsRn/9dIBH6X7n0WAW3tzeKZK1zENWFKrd7aLlzEdwFzO/1JTQsEDom5TRie0Kd5yic4BGvS1C1BsA2wJhzyiZ2j7RUE9m8tOAkPEIs929FYIfmH8XcCQKHT0TqT0+N+wCiyfNawPlDhZWcObscFZeEmKgvqiUFCoCj6xI1hvyHK0nu7fnZ/sGc6oNT/SrFjubYWjOyoYFL7gMnlYAhyjZhjuAwN1m1/wjwrOx8DbFr2NW8qb3hv+CIzK1zL3LDryKjqNkTxcOp4aJnmSTa73guCEmWc7pnLkLw5O8RgW7RKHrObeeQ0l9lu4HWXwlhdWRxvVMQDimhtTrGASL6sIuaxyhOkrH4HFImP70SaCoK9+euMxnzkPjg9HqPIFj+I0KSMloVxW"

# ═══════════════════════════ SESSIONS ═══════════════════════════
_oo_session = requests.Session()
_tg_session = requests.Session()

_oo_adapter = HTTPAdapter(pool_connections=50, pool_maxsize=100, pool_block=False)
_oo_session.mount("https://", _oo_adapter)
_oo_session.headers.update({"Accept-Encoding": "gzip, deflate", "Connection": "keep-alive"})

_adapter = HTTPAdapter(
    pool_connections=100, pool_maxsize=200,
    max_retries=Retry(total=1, connect=1, read=1, status=1,
                      backoff_factor=0.2, status_forcelist=(502,503,504)),
    pool_block=False)
_tg_session.mount("https://", _adapter)
_tg_session.mount("http://",  _adapter)

DATA_FILE = "bot_data.json"
_lock, _save_lock = threading.Lock(), threading.Lock()
_save_pending = {"flag": False}
_users, _sessions, _devices = {}, {}, {}

_forced_channels = [{"id": "@dznet3", "name": "قناة الإثباتات والجديد"}]

def clean_instagram_url(url):
    try:
        parsed = urlparse(url.strip())
        clean_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))
        return clean_url.rstrip('/')
    except:
        return url.strip()

_forced_instagram = [{"name": "taibreffess", "url": clean_instagram_url("https://www.instagram.com/taibreffess?exln=MWthcGhjOW82ZG9ndg==")}]

_log_channel = LOG_CHANNEL_ID
_bot_stats = {"users": 0, "activations": 0}
_maintenance = False
_otp_cooldown, _otp_cooldown_lock = {}, threading.Lock()
_user_locks, _user_locks_guard = {}, threading.Lock()

def _get_user_lock(cid):
    with _user_locks_guard:
        if cid not in _user_locks:
            _user_locks[cid] = threading.Lock()
        return _user_locks[cid]

def _check_otp_cooldown(cid):
    now = time.time()
    with _otp_cooldown_lock:
        last = _otp_cooldown.get(cid, 0)
        if now - last < 60:
            return int(60 - (now - last))
        _otp_cooldown[cid] = now
    return 0

def _do_save():
    with _save_lock:
        try:
            data = {
                "users": {str(k): v for k, v in _users.items()},
                "devices": {str(k): v for k, v in _devices.items()},
                "channels": _forced_channels,
                "instagram": _forced_instagram,
                "log_channel": _log_channel,
                "stats": _bot_stats,
                "maintenance": _maintenance,
            }
            tmp = DATA_FILE + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
            os.replace(tmp, DATA_FILE)
            _save_pending["flag"] = False
        except Exception as e:
            logger.warning(f"save: {e}")

def _save_async():
    if _save_pending["flag"]: return
    _save_pending["flag"] = True
    def _d():
        time.sleep(2); _do_save()
    threading.Thread(target=_d, daemon=True).start()

def _load_from_disk():
    global _users, _devices, _forced_channels, _forced_instagram, _log_channel, _bot_stats, _maintenance
    if not os.path.exists(DATA_FILE): return
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        _users = {int(k): v for k, v in data.get("users", {}).items()}
        _devices = {int(k): v for k, v in data.get("devices", {}).items()}
        _forced_channels = data.get("channels", [{"id": "@dznet3", "name": "قناة الإثباتات والجديد"}])
        loaded_ig = data.get("instagram", [])
        _forced_instagram = loaded_ig if loaded_ig else [{"name": "taibreffess", "url": "https://www.instagram.com/taibreffess"}]
        _log_channel = data.get("log_channel", LOG_CHANNEL_ID)
        _bot_stats = data.get("stats", {"users": len(_users), "activations": 0})
        _maintenance = data.get("maintenance", False)
        logger.info(f"✅ Loaded {len(_users)} users")
    except Exception as e:
        logger.warning(f"load: {e}")

# ═══════════════════════════ HELPERS ═══════════════════════════
def oo_get_user(cid):
    with _lock:
        return dict(_users.get(cid)) if _users.get(cid) else None

def oo_save_user(cid, data):
    with _lock:
        is_new = cid not in _users
        if is_new:
            _users[cid] = {}
        _bot_stats["users"] = len(_users)
        changed = False
        for k, v in data.items():
            if v is not None and _users[cid].get(k) != v:
                _users[cid][k] = v; changed = True
    if changed: _save_async()

def oo_delete_user(cid):
    with _lock: _users.pop(cid, None)
    _save_async()

def oo_get_session(cid):
    with _lock: return dict(_sessions.get(cid)) if _sessions.get(cid) else {}

def oo_set_session(cid, data):
    with _lock:
        if cid not in _sessions: _sessions[cid] = {}
        _sessions[cid].update({k: v for k, v in data.items() if v is not None})

def oo_clear_session(cid):
    with _lock: _sessions.pop(cid, None)

def oo_get_device(cid):
    iid = oo_new_iid()
    return {"instance_id": iid, "plat_sig": oo_new_psig(iid)}

def oo_now_ms():  return str(int(time.time() * 1000))

def oo_new_iid():
    u = uuid.uuid4().hex
    return f"{u[:8]}-{u[8:12]}-11{u[12:16]}-{u[16:20]}-{u[20:32]}{oo_now_ms()}"

def oo_new_psig(iid):
    p = json.dumps({"platform": "android", "is-physical-device": True, "device-id": iid},
                   separators=(",", ":"))
    return base64.b64encode(p.encode()).decode()

def oo_new_corr(): return uuid.uuid4().hex + oo_now_ms()
def oo_new_fp():   return uuid.uuid4().hex + uuid.uuid4().hex[:32]

def oo_decode_jwt(token):
    if not token: return {}
    try:
        p = token.split(".")[1]; p += "=" * (-len(p) % 4)
        return json.loads(base64.urlsafe_b64decode(p))
    except: return {}

def oo_extract_did(token): return oo_decode_jwt(token).get("device-id")

def mask_phone(m):
    if not m: return "—"
    s = str(m).strip()
    if s.startswith("213") and len(s) == 12: s = "0" + s[3:]
    return s[:2] + "x" * (len(s) - 4) + s[-2:] if len(s) >= 8 else s

def get_user_display(cid):
    u = oo_get_user(cid) or {}
    if u.get("username"):
        return f"@{u['username']}"
    name = u.get("first_name") or "مستخدم"
    return f"<a href='tg://user?id={cid}'>{name}</a>"

# ═══════════════════════════ HTTP & HEADERS ═══════════════════════════
def oo_http(method, url, headers, body="", timeout=6):
    try:
        if method == "GET":
            r = _oo_session.get(url, headers=headers, timeout=timeout, verify=False)
        elif method == "POST":
            r = _oo_session.post(url, headers=headers, data=body, timeout=timeout, verify=False)
        else:
            return None
        txt = r.text
        if "Request Rejected" in txt or "support id" in txt.lower():
            return {"ip_blocked": True, "code": r.status_code}
        try: j = r.json()
        except: j = None
        return {"code": r.status_code, "body": txt,
                "headers": {k.lower(): v for k, v in r.headers.items()}, "json": j}
    except Exception as e:
        logger.debug(f"http err: {e}")
        return None

def oo_base_h(msisdn, fp, corr, ts, iid, psig):
    return {
        "User-Agent": "Dart/3.11 (dart:io)", "Accept-Encoding": "gzip",
        "x-msisdn": msisdn, "x-device-fingerprint": fp,
        "x-platform-origin": OOREDOO_PLATFORM_ORIGIN, "x-correlation-id": corr,
        "platform": OOREDOO_PLATFORM, "x-version": OOREDOO_X_VERSION,
        "x-signature": OOREDOO_X_SIG, "x-platform-data-signature": psig,
        "x-timestamp": ts, "x-instance-id": iid,
    }

def oo_authed_h(msisdn, token, tokh):
    ts   = tokh.get("tok_timestamp")   or oo_now_ms()
    iid  = tokh.get("tok_instance_id") or oo_new_iid()
    psig = tokh.get("tok_plat_sig")    or oo_new_psig(iid)
    return {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        "Accept-Encoding": "gzip, deflate, br",
        "x-msisdn": msisdn, "x-device-fingerprint": oo_new_fp(),
        "x-platform-origin": "web", "authorization": f"Bearer {token}",
        "x-correlation-id": oo_new_corr(), "platform": "web",
        "x-version": OOREDOO_X_VERSION, "x-signature": OOREDOO_X_SIG,
        "x-platform-data-signature": psig, "x-timestamp": ts, "x-instance-id": iid,
        "origin": "https://my.ooredoo.dz", "referer": "https://my.ooredoo.dz/",
    }

# ═══════════════════════════ OTP ═══════════════════════════
def oo_send_otp(msisdn, device=None):
    last_error = "unknown"
    for attempt in range(2):
        try:
            iid = oo_new_iid(); psig = oo_new_psig(iid); ts = oo_now_ms()
            h3 = oo_base_h(msisdn, oo_new_fp(), oo_new_corr(), ts, iid, psig)
            h3["content-type"] = "application/json; charset=utf-8"
            h3["x-native-integrity-token"] = OOREDOO_INTEGRITY_1
            h3["x-path"]   = "/api/auth/realms/myooredoo/protocol/openid-connect/token"
            h3["x-method"] = "POST"
            r3 = oo_http("POST", f"{OOREDOO_BFF}/checkpoint/token", h3, "{}", timeout=8)

            if not r3 or r3.get("ip_blocked"):
                last_error = "ip_blocked"; time.sleep(3); continue
            nonce   = r3["headers"].get("x-nonce-id")
            chronos = r3["headers"].get("x-chronos-id")
            if not nonce or not chronos:
                last_error = "checkpoint_failed"; time.sleep(2); continue

            h4 = {
                "User-Agent": "Dart/3.11 (dart:io)", "Accept-Encoding": "gzip",
                "x-msisdn": msisdn, "x-device-fingerprint": oo_new_fp(),
                "x-nonce-id": nonce, "x-platform-origin": OOREDOO_PLATFORM_ORIGIN,
                "platform": OOREDOO_PLATFORM, "x-version": OOREDOO_X_VERSION,
                "x-signature": OOREDOO_X_SIG, "x-chronos-id": chronos,
                "x-timestamp": ts, "x-platform-info": psig, "x-force-update": "true",
                "x-instance-id": iid, "Content-Type": "application/x-www-form-urlencoded",
            }
            b4 = urlencode({"client_id": OOREDOO_CLIENT_ID,
                            "grant_type": "password", "username": msisdn})
            r4 = oo_http("POST", OOREDOO_AUTH, h4, b4, timeout=10)
            if not r4:
                last_error = "network"; time.sleep(3); continue
            c4 = r4.get("code")
            if c4 in (401, 403, 200): return {"ok": True}
            if c4 == 429:
                last_error = "rate_limit"; time.sleep(5); continue
            last_error = f"http_{c4}"; time.sleep(2)
        except Exception as e:
            last_error = str(e); time.sleep(2)
    return {"error": last_error}

def oo_verify_otp(msisdn, otp, device):
    iid, psig, ts = device["instance_id"], device["plat_sig"], oo_now_ms()
    h6 = oo_base_h(msisdn, oo_new_fp(), oo_new_corr(), ts, iid, psig)
    h6["content-type"] = "application/json; charset=utf-8"
    h6["x-native-integrity-token"] = OOREDOO_INTEGRITY_2
    h6["x-path"]   = "/api/auth/realms/myooredoo/protocol/openid-connect/token"
    h6["x-method"] = "POST"
    r6 = oo_http("POST", f"{OOREDOO_BFF}/checkpoint/token", h6, "{}", timeout=6)
    if not r6 or r6.get("ip_blocked"): return False
    n2 = r6["headers"].get("x-nonce-id"); c2 = r6["headers"].get("x-chronos-id")
    if not n2 or not c2: return False

    fp7 = oo_new_fp()
    h7 = {
        "User-Agent": "Dart/3.11 (dart:io)", "Accept-Encoding": "gzip",
        "x-msisdn": msisdn, "x-device-fingerprint": fp7, "x-nonce-id": n2,
        "x-platform-origin": OOREDOO_PLATFORM_ORIGIN, "platform": OOREDOO_PLATFORM,
        "x-version": OOREDOO_X_VERSION, "x-signature": OOREDOO_X_SIG,
        "x-chronos-id": c2, "x-timestamp": ts, "x-platform-info": psig,
        "x-force-update": "true", "x-instance-id": iid,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    b7 = urlencode({"client_id": OOREDOO_CLIENT_ID, "grant_type": "password",
                    "username": msisdn, "otp": otp})
    r7 = oo_http("POST", OOREDOO_AUTH, h7, b7, timeout=8)
    c7 = r7.get("code") if r7 else None
    if c7 in (401, 403): return "wrong_otp"
    if c7 == 200 and r7.get("json") and "access_token" in r7["json"]:
        j = r7["json"]
        return {
            "access_token": j["access_token"], "refresh_token": j.get("refresh_token", ""),
            "tok_fingerprint": fp7, "tok_timestamp": ts,
            "tok_instance_id": oo_extract_did(j["access_token"]) or iid,
            "tok_plat_sig": psig, "tok_correlation": oo_new_corr(),
        }
    return False

# ═══════════════════════════ Refresh / Session ═══════════════════════════
def oo_refresh_token(user, device):
    rt = user.get("refresh_token", "")
    if not rt: return "expired"
    iid  = user.get("tok_instance_id") or device["instance_id"]
    psig = user.get("tok_plat_sig")    or device["plat_sig"]
    ts   = oo_now_ms()
    payload = {"grant_type": "refresh_token", "client_id": OOREDOO_CLIENT_ID, "refresh_token": rt}
    headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/x-www-form-urlencoded",
               "Origin": "https://my.ooredoo.dz", "Referer": "https://my.ooredoo.dz/"}
    try:
        r = _oo_session.post(OOREDOO_AUTH, data=payload, headers=headers, timeout=8, verify=False)
        if r.status_code == 200:
            res = r.json()
            if res.get("access_token"):
                return {
                    "access_token": res["access_token"], "refresh_token": res.get("refresh_token", rt),
                    "tok_fingerprint": oo_new_fp(), "tok_timestamp": ts,
                    "tok_instance_id": oo_extract_did(res["access_token"]) or iid,
                    "tok_plat_sig": psig, "tok_correlation": oo_new_corr(),
                }
        return "expired"
    except: return False

def oo_call_refresh(cid, func, msisdn, user, *a):
    res = func(msisdn, user, *a)
    if isinstance(res, dict) and (res.get("_need_refresh") or res.get("auth_error")):
        dev = oo_get_device(cid)
        nt  = oo_refresh_token(user, dev)
        if nt == "expired": return {"error": "expired"}
        if not nt:          return {"error": "refresh_failed"}
        user.update(nt); oo_save_user(cid, user)
        res = func(msisdn, user, *a)
    return res

# ═══════════════════════════ Ooredoo endpoints ═══════════════════════════
def oo_buy_cvm(msisdn, user, bundle_code):
    h = oo_authed_h(msisdn, user.get("access_token"), {
        "tok_timestamp": user.get("tok_timestamp"),
        "tok_instance_id": user.get("tok_instance_id"),
        "tok_plat_sig": user.get("tok_plat_sig")})
    h["content-type"] = "application/json; charset=utf-8"
    payload = {"bundleCode": bundle_code}
    r = oo_http("POST", f"{OOREDOO_BFF}/cvm/dynamic-bundle-purchase",
                h, json.dumps(payload), timeout=10)
    if not r: return {"error": "net"}
    code = r["code"]
    body_lower = (r.get("body") or "").lower()
    if code in (200, 201, 204): return {"success": True}
    if code == 401: return {"auth_error": True}
    if code in (400, 409, 500):
        if any(k in body_lower for k in ["already", "deja", "مسبق", "استفدت", "used", "24h"]):
            return {"error": "already_used"}
    if code == 409: return {"error": "💰 رصيد غير كافي"}
    if code == 400: return {"error": "⚠️ العرض غير متاح لشريحتك"}
    if code == 500: return {"error": "already_used"}
    return {"error": f"HTTP {code}"}

# ═══════════════════════════ Telegram ═══════════════════════════
def tg_request(method, **kwargs):
    try:
        r = _tg_session.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/{method}", json=kwargs, timeout=5)
        return r.json()
    except: return None

def send_log(text):
    try: 
        tg_request("sendMessage", chat_id=LOG_CHANNEL_ID, text=text, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Failed to send log to channel: {e}")

# ═══════════════════════════ Subscription Verification ═══════════════════════════
def check_telegram_channels(cid):
    if cid == ADMIN_ID or not _forced_channels:
        return True
    for ch in _forced_channels:
        ch_id = ch.get("id")
        try:
            res = tg_request("getChatMember", chat_id=ch_id, user_id=cid)
            if res and res.get("ok"):
                status = res["result"].get("status")
                if status in ("left", "kicked"):
                    return False
            else:
                return False
        except:
            return False
    return True

def check_user_subscription(cid):
    if cid == ADMIN_ID:
        return True
    if not check_telegram_channels(cid):
        return "telegram_missing"
    
    u = oo_get_user(cid) or {}
    if _forced_instagram and not u.get("instagram_verified", False):
        return "instagram_missing"
        
    return True

# ═══════════════════════════ Menus & Support/Donation Markup ═══════════════════════════
def get_main_menu_markup(cid):
    markup = Markup(row_width=1)
    markup.add(btn('تفعيل عرض 2 جيغا', callback_data="do_2g", emoji_id=E_ROCKET, color='success'))
    markup.add(btn('ربط أو تغيير الرقم', callback_data="change_phone", emoji_id=E_DIAMOND, color='primary'))
    markup.add(btn('دعـم البوت 🌟', callback_data="support_bot", emoji_id=E_STAR, color='primary'))
    if cid == ADMIN_ID:
        markup.add(btn('لوحة تحكم المالك 🛠️', callback_data="admin_panel", color='danger'))
    return markup

def get_donate_markup():
    prices = [15, 50, 100, 150, 200, 250, 300, 400, 500, 600, 13]
    links = {}
    for p in prices:
        try:
            link = ben.create_invoice_link(
                title="التبرع بالنجوم",
                description=f"دعم البوت بـ {p} نجمة",
                payload=f"donate_{p}",
                provider_token="", 
                currency="XTR",
                prices=[LabeledPrice(label="تبرع", amount=p)]
            )
            links[p] = link
        except Exception as e:
            logger.warning(f"خطأ في إنشاء الرابط {p}: {e}")
            links[p] = "https://t.me/"
            
    return Markup(
        [
            [btn('تعزيز القناة', url="https://t.me/boost/solitube31", emoji_id=E_CHAN, color='success')],
            [btn('15', url=links[15], emoji_id=E_STAR, color='success'), btn('50', url=links[50], emoji_id=E_STAR, color='success'), btn('100', url=links[100], emoji_id=E_STAR, color='success')],
            [btn('150', url=links[150], emoji_id=E_STAR, color='success'), btn('200', url=links[200], emoji_id=E_STAR, color='success'), btn('250', url=links[250], emoji_id=E_STAR, color='success')],
            [btn('300', url=links[300], emoji_id=E_STAR, color='success'), btn('400', url=links[400], emoji_id=E_STAR, color='success'), btn('500', url=links[500], emoji_id=E_STAR, color='success')],
            [btn('600', url=links[600], emoji_id=E_STAR, color='success')],
            [btn('13', url=links[13], emoji_id=E_STAR, color='success')],
            [btn('القائمة الرئيسية 🔙', callback_data="main_menu", emoji_id=E_ROCKET, color='primary')]
        ]
    )

def oo_menu(cid, user=None, message_id=None):
    welcome_msg = (
        f"👋 أهلاً بك عزيزي المستخدم!\n\n"
        f"للبدء و التفعيل، 2G 🎁 اوريدو يرجى ⌨\n\n"
        f"إرسال رقم هاتف أوريدو الخاص بك 📨\n\n"
        f"(05XXXXXXXX) 📱"
    )
    markup = get_main_menu_markup(cid)
    
    if message_id:
        try:
            ben.edit_message_text(text=welcome_msg, chat_id=cid, message_id=message_id, parse_mode="HTML", reply_markup=markup)
        except:
            ben.send_message(cid, welcome_msg, parse_mode="HTML", reply_markup=markup)
    else:
        ben.send_message(cid, welcome_msg, parse_mode="HTML", reply_markup=markup)

def admin_panel_menu(cid, message_id):
    total_users = len(_users)
    activations = _bot_stats.get("activations", 0)
    
    panel_text = (
        f"🛠️ <b>لوحة تحكم المالك والإذاعة</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 <b>إجمالي المستخدمين:</b> <code>{total_users}</code>\n"
        f"🎉 <b>إجمالي التفعيلات:</b> <code>{activations}</code>\n"
        f"📌 <b>قنوات تليجرام:</b> <b>{len(_forced_channels)}</b>\n"
        f"📸 <b>حسابات إنستغرام:</b> <b>{len(_forced_instagram)}</b>"
    )
    
    inline_kb = Markup(row_width=2)
    inline_kb.row(
        btn("إضافة قناة 📢", callback_data="add_sub_ch", color='success'),
        btn("حذف القنوات 🗑️", callback_data="del_sub_ch", color='danger')
    )
    inline_kb.row(
        btn("إضافة إنستغرام 📸", callback_data="add_insta_ch", color='success'),
        btn("حذف إنستغرام 🗑️", callback_data="del_insta_ch", color='danger')
    )
    inline_kb.add(btn("إرسال رسالة للمستخدمين ✉️", callback_data="broadcast_msg", color='success'))
    inline_kb.add(btn("عرض أيدي المستخدمين 🆔", callback_data="list_users_ids", color='primary'))
    inline_kb.add(btn("الإحصائيات الشاملة 📊", callback_data="bot_stats", color='primary'))
    inline_kb.add(btn("القائمة الرئيسية 🔙", callback_data="main_menu", color='primary'))
    
    try:
        ben.edit_message_text(panel_text, chat_id=cid, message_id=message_id, parse_mode="HTML", reply_markup=inline_kb)
    except:
        ben.send_message(cid, panel_text, parse_mode="HTML", reply_markup=inline_kb)

def send_subscription_warning(cid, message_id=None):
    sub_status = check_user_subscription(cid)
    kb = Markup(row_width=1)
    
    if sub_status == "telegram_missing":
        msg = (
            f"⚠️ <b>المرحلة 1: الاشتراك الإجباري في قنوات تليجرام!</b>\n\n"
            f"يرجى الاشتراك في القنوات التالية أولاً ثم اضغط على زر التحقق:"
        )
        for ch in _forced_channels:
            name = ch.get("name", "قناة")
            url = f"https://t.me/{ch.get('id').replace('@', '')}"
            kb.add(btn(f"الانضمام إلى {name}", url=url, color='success'))
        kb.add(btn("تحقق من اشتراك تليجرام ✅", callback_data="check_sub", color='primary'))
        
    elif sub_status == "instagram_missing":
        msg = (
            f"⚠️ <b>المرحلة 2: الاشتراك الإجباري في إنستغرام!</b>\n\n"
            f"لقد اشتركت في قنوات تليجرام بنجاح! 🎉\n"
            f"الآن يرجى متابعة الحساب عبر الزر أدناه (Instagram) ثم اضغط تحقق:"
        )
        for ig in _forced_instagram:
            ig_url = clean_instagram_url(ig.get("url"))
            kb.add(btn("Instagram", url=ig_url, color='success'))
            
        kb.add(btn("تحقق من متابعة إنستغرام ✅", callback_data="check_insta", color='primary'))
    else:
        return
        
    if message_id:
        try:
            ben.edit_message_text(msg, chat_id=cid, message_id=message_id, parse_mode="HTML", reply_markup=kb)
        except:
            ben.send_message(cid, msg, parse_mode="HTML", reply_markup=kb)
    else:
        ben.send_message(cid, msg, parse_mode="HTML", reply_markup=kb)

# ═══════════════════════════ Actions ═══════════════════════════
def oo_do_free_2go(cid, user, message_id=None):
    lock = _get_user_lock(cid)
    if not lock.acquire(blocking=False):
        return
    try:
        if check_user_subscription(cid) != True:
            send_subscription_warning(cid, message_id)
            return

        if not user or not user.get("access_token"):
            oo_set_session(cid, {"state": "awaiting_phone"})
            text = (
                f"👋 أهلاً بك عزيزي المستخدم!\n\n"
                f"للبدء و التفعيل، 2G 🎁 اوريدو يرجى ⌨\n\n"
                f"إرسال رقم هاتف أوريدو الخاص بك 📨\n\n"
                f"(05XXXXXXXX) 📱"
            )
            if message_id:
                try: ben.edit_message_text(text, chat_id=cid, message_id=message_id, parse_mode="HTML")
                except: ben.send_message(cid, text, parse_mode="HTML")
            else:
                ben.send_message(cid, text, parse_mode="HTML")
            return

        m = user.get("msisdn", "")
        if message_id:
            try: ben.edit_message_text("⏳ جاري تفعيل 2 جيقا...", chat_id=cid, message_id=message_id, parse_mode="HTML")
            except: pass
        else:
            ben.send_message(cid, "⏳ جاري تفعيل 2 جيقا...", parse_mode="HTML")
            
        res = oo_call_refresh(cid, oo_buy_cvm, m, user, "BTL_24H_DATA_Free_2Go")

        if isinstance(res, dict) and res.get("error") == "expired":
            oo_delete_user(cid)
            oo_set_session(cid, {"state": "awaiting_phone"})
            text = (
                f"👋 أهلاً بك عزيزي المستخدم!\n\n"
                f"للبدء و التفعيل، 2G 🎁 اوريدو يرجى ⌨\n\n"
                f"إرسال رقم هاتف أوريدو الخاص بك 📨\n\n"
                f"(05XXXXXXXX) 📱"
            )
            if message_id:
                try: ben.edit_message_text(text, chat_id=cid, message_id=message_id, parse_mode="HTML")
                except: ben.send_message(cid, text, parse_mode="HTML")
            return
            
        if res and res.get("success"):
            masked_num = mask_phone(m)
            text = f"🎉 <b>تم تفعيل 2g بنجاح 🥳</b>\n📱 <b>الرقم:</b> <code>{masked_num}</code>"
            
            _bot_stats["activations"] = _bot_stats.get("activations", 0) + 1
            _save_async()

            markup = get_main_menu_markup(cid)
            if message_id:
                try: ben.edit_message_text(text, chat_id=cid, message_id=message_id, parse_mode="HTML", reply_markup=markup)
                except: ben.send_message(cid, text, parse_mode="HTML", reply_markup=markup)
            else:
                ben.send_message(cid, text, parse_mode="HTML", reply_markup=markup)
            
            log_msg = (
                f"🎉 <b>عملية تفعيل 2G ناجحة جديدة!</b>\n\n"
                f"👤 <b>المستخدم:</b> {get_user_display(cid)}\n"
                f"📱 <b>رقم الهاتف:</b> <code>{masked_num}</code>\n"
                f"🎁 <b>العرض:</b> 2GB Ooredoo Free 2Go\n"
                f"⏰ <b>الوقت:</b> <code>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</code>"
            )
            send_log(log_msg)
            
        elif res and res.get("error") == "already_used":
            text = "⚠️ <b>لقد استفدت من العرض مسبقاً</b>\nحاول بعد <b>24 ساعة</b> ⏳"
            markup = get_main_menu_markup(cid)
            if message_id:
                try: ben.edit_message_text(text, chat_id=cid, message_id=message_id, parse_mode="HTML", reply_markup=markup)
                except: ben.send_message(cid, text, parse_mode="HTML", reply_markup=markup)
            else:
                ben.send_message(cid, text, parse_mode="HTML", reply_markup=markup)
        else:
            err_msg = res.get('error') if isinstance(res, dict) else 'خطأ غير معروف'
            text = f"❌ فشل التفعيل: {err_msg}"
            markup = get_main_menu_markup(cid)
            if message_id:
                try: ben.edit_message_text(text, chat_id=cid, message_id=message_id, parse_mode="HTML", reply_markup=markup)
                except: ben.send_message(cid, text, parse_mode="HTML", reply_markup=markup)
            else:
                ben.send_message(cid, text, parse_mode="HTML", reply_markup=markup)
    finally:
        lock.release()

# ═══════════════════════════ Message Handlers ═══════════════════════════
@ben.message_handler(commands=['start'])
def start(message):
    cid = message.chat.id
    if _maintenance and cid != ADMIN_ID:
        return ben.send_message(cid, "🔧 البوت في حالة صيانة حالياً.")
        
    if check_user_subscription(cid) != True:
        return send_subscription_warning(cid)

    user = oo_get_user(cid)
    oo_menu(cid, user)

@ben.message_handler(content_types=['successful_payment'])
def successful_payment(message):
    amount = message.successful_payment.total_amount
    ben.reply_to(message, f"{emo(E_DIAMOND, '💎')} <b>شكراً لك!</b>\nلقد تبرعت بـ {amount} نجمة لدعم البوت 🌟.")

@ben.pre_checkout_query_handler(func=lambda query: True)
def pre_checkout(query):
    ben.answer_pre_checkout_query(query.id, ok=True)

@ben.message_handler(func=lambda message: True)
def handle_text(message):
    cid = message.chat.id
    text = message.text.strip()
    
    if _maintenance and cid != ADMIN_ID:
        return ben.send_message(cid, "🔧 البوت في حالة صيانة.")
        
    if check_user_subscription(cid) != True:
        return send_subscription_warning(cid)

    sess  = oo_get_session(cid)
    state = sess.get("state", "")
    user  = oo_get_user(cid)

    if state == "admin_add_channel":
        if cid != ADMIN_ID: return
        oo_clear_session(cid)
        parts = text.split("|")
        ch_id = parts[0].strip()
        ch_name = parts[1].strip() if len(parts) > 1 else "قناة"
        _forced_channels.append({"id": ch_id, "name": ch_name})
        _do_save()
        kb = Markup()
        kb.add(btn("لوحة التحكم 🛠️", callback_data="admin_panel", color='primary'))
        return ben.send_message(cid, f"✅ تمت إضافة القناة ({ch_name}) بنجاح.", parse_mode="HTML", reply_markup=kb)

    if state == "admin_add_insta":
        if cid != ADMIN_ID: return
        oo_clear_session(cid)
        parts = text.split("|")
        ig_name = parts[0].strip()
        raw_url = parts[1].strip() if len(parts) > 1 else "https://instagram.com/"
        ig_url = clean_instagram_url(raw_url)
        _forced_instagram.append({"name": ig_name, "url": ig_url})
        _do_save()
        kb = Markup()
        kb.add(btn("لوحة التحكم 🛠️", callback_data="admin_panel", color='primary'))
        return ben.send_message(cid, f"✅ تمت إضافة حساب إنستغرام بنجاح بالرابط النظيف.", parse_mode="HTML", reply_markup=kb)

    if state == "admin_broadcast":
        if cid != ADMIN_ID: return
        oo_clear_session(cid)
        
        def _do_broadcast():
            success_count = 0
            fail_count = 0
            ben.send_message(cid, "📤 جاري إرسال الرسالة لجميع المستخدمين...")
            for uid in _users.keys():
                try:
                    r = tg_request("sendMessage", chat_id=uid, text=text, parse_mode="HTML")
                    if r and r.get("ok"):
                        success_count += 1
                    else:
                        fail_count += 1
                    time.sleep(0.05)
                except:
                    fail_count += 1
            
            res_text = (
                f"📊 <b>تقرير الإذاعة:</b>\n\n"
                f"✅ تم الإرسال بنجاح إلى: <b>{success_count}</b> مستخدم\n"
                f"❌ فشل الإرسال إلى: <b>{fail_count}</b> مستخدم"
            )
            kb = Markup()
            kb.add(btn("لوحة التحكم 🛠️", callback_data="admin_panel", color='primary'))
            ben.send_message(cid, res_text, parse_mode="HTML", reply_markup=kb)

        threading.Thread(target=_do_broadcast, daemon=True).start()
        return

    if state == "awaiting_phone":
        dg = "".join(c for c in text if c.isdigit())
        if not re.match(r"^05\d{8}$", dg):
            return ben.send_message(cid, "❌ رقم غير صحيح (مثال: 0550123456)")
        msisdn = "213" + dg[1:]
        wait = _check_otp_cooldown(cid)
        if wait > 0:
            return ben.send_message(cid, f"⚠️ انتظر {wait} ثانية قبل إعادة طلب الرمز.")
        oo_set_session(cid, {"state": "awaiting_otp", "msisdn": msisdn})
        
        ben.send_message(cid, "✅ جاري إرسال رمز التحقق إلى رقمك...", parse_mode="HTML")
        
        def _bg():
            res = oo_send_otp(msisdn)
            if res.get("ok"):
                kb = Markup(row_width=1)
                kb.add(btn("إعادة إرسال الرمز", callback_data="resend_otp", color='primary'))
                kb.add(btn("إلغاء", callback_data="change_phone", color='danger'))
                ben.send_message(cid, "📩 أدخل رمز OTP المكون من 6 أرقام:", parse_mode="HTML", reply_markup=kb)
            else:
                kb = Markup()
                kb.add(btn("إلغاء", callback_data="change_phone", color='danger'))
                ben.send_message(cid, "⚠️ فشل إرسال الرمز، حاول مجدداً.", parse_mode="HTML", reply_markup=kb)
        threading.Thread(target=_bg, daemon=True).start()
        return

    if state == "awaiting_otp":
        if not text.isdigit() or len(text) != 6:
            return ben.send_message(cid, "❌ الرمز يجب أن يكون 6 أرقام فقط.")
        dev = oo_get_device(cid)
        res = oo_verify_otp(sess.get("msisdn"), text, dev)
        if res == "wrong_otp":
            return ben.send_message(cid, "❌ الرمز خاطئ، أعد المحاولة:")
        if not res: return ben.send_message(cid, "❌ سيرفر أوريدو غير متاح حالياً.")
        oo_save_user(cid, {"msisdn": sess.get("msisdn"), **res})
        oo_clear_session(cid)
        ben.send_message(cid, "🎉 تم تسجيل الدخول بنجاح!")
        return oo_menu(cid, oo_get_user(cid))

    dg = "".join(c for c in text if c.isdigit())
    if re.match(r"^05\d{8}$", dg):
        msisdn = "213" + dg[1:]
        wait = _check_otp_cooldown(cid)
        if wait > 0:
            return ben.send_message(cid, f"⚠️ انتظر {wait} ثانية.")
        oo_set_session(cid, {"state": "awaiting_otp", "msisdn": msisdn})
        
        ben.send_message(cid, "✅ جاري إرسال رمز التحقق...", parse_mode="HTML")
        
        def _bg2():
            res = oo_send_otp(msisdn)
            if res.get("ok"):
                kb = Markup(row_width=1)
                kb.add(btn("إعادة إرسال", callback_data="resend_otp", color='primary'))
                kb.add(btn("إلغاء", callback_data="change_phone", color='danger'))
                ben.send_message(cid, "📩 أدخل رمز OTP المكون من 6 أرقام:", parse_mode="HTML", reply_markup=kb)
            else:
                kb = Markup()
                kb.add(btn("إلغاء", callback_data="change_phone", color='danger'))
                ben.send_message(cid, "⚠️ فشل إرسال الرمز، حاول مجدداً.", parse_mode="HTML", reply_markup=kb)
        threading.Thread(target=_bg2, daemon=True).start()
        return

    oo_menu(cid, user)

# ═══════════════════════════ Callback Handlers ═══════════════════════════
@ben.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    try:
        cid = call.message.chat.id
        message_id = call.message.message_id
        data = call.data
        user = oo_get_user(cid)

        if data == "check_sub":
            if check_telegram_channels(cid):
                if _forced_instagram:
                    try: ben.answer_callback_query(call.id, "✅ ممتاز! انتقل لمتابعة إنستغرام الآن.", show_alert=True)
                    except: pass
                    send_subscription_warning(cid, message_id)
                else:
                    try: ben.answer_callback_query(call.id, "✅ تم التحقق بنجاح!", show_alert=True)
                    except: pass
                    oo_menu(cid, user, message_id)
            else:
                try: ben.answer_callback_query(call.id, "❌ لم تقم بالاشتراك في قنوات تليجرام بعد!", show_alert=True)
                except: pass

        elif data == "check_insta":
            oo_save_user(cid, {"instagram_verified": True})
            if check_user_subscription(cid) == True:
                try: ben.answer_callback_query(call.id, "✅ تم التحقق من إنستغرام بنجاح!", show_alert=True)
                except: pass
                oo_menu(cid, user, message_id)
            else:
                try: ben.answer_callback_query(call.id, "❌ يرجى الضغط ومتابعة الحساب أولاً!", show_alert=True)
                except: pass

        elif data == "support_bot":
            try: ben.answer_callback_query(call.id)
            except: pass
            support_caption = (
                f"{emo(E_ROCKET, '🚀')} <b>مرحبا بك عزيزي</b>\n\n"
                f"{emo(E_DIAMOND, '💎')} <b>يمكنك اختيار باقة التبرع بالنجوم لدعم البوت من الأزرار أدناه</b>.\n"
                f"{emo(E_ROCKET, '🚀')} <b>دعـم ولو بسيـط = استمرار وتطوير دائـم</b>\n"
                f"{emo(E_STAR, '⭐')} <b>كل نجمة تساهم في استمرار عمل البوت</b>."
            )
            markup = get_donate_markup()
            try:
                ben.edit_message_text(text=support_caption, chat_id=cid, message_id=message_id, parse_mode="HTML", reply_markup=markup)
            except:
                ben.send_message(cid, support_caption, parse_mode="HTML", reply_markup=markup)

        elif data == "admin_panel":
            if cid != ADMIN_ID:
                try: ben.answer_callback_query(call.id, "للمالك فقط!", show_alert=True)
                except: pass
                return
            try: ben.answer_callback_query(call.id)
            except: pass
            admin_panel_menu(cid, message_id)

        elif data == "main_menu":
            try: ben.answer_callback_query(call.id)
            except: pass
            oo_menu(cid, user, message_id)

        elif data == "add_sub_ch":
            if cid != ADMIN_ID: return
            try: ben.answer_callback_query(call.id)
            except: pass
            oo_set_session(cid, {"state": "admin_add_channel"})
            ben.send_message(cid, "➕ أرسل معرف القناة واسمها بالشكل التالي:\n\n<code>@channel | اسم القناة</code>", parse_mode="HTML")

        elif data == "del_sub_ch":
            if cid != ADMIN_ID: return
            try: ben.answer_callback_query(call.id)
            except: pass
            _forced_channels.clear()
            _do_save()
            kb = Markup()
            kb.add(btn("رجوع", callback_data="admin_panel", color='primary'))
            try: ben.edit_message_text("✅ تم حذف جميع قنوات تليجرام الإجبارية.", chat_id=cid, message_id=message_id, reply_markup=kb)
            except: ben.send_message(cid, "✅ تم حذف جميع قنوات تليجرام الإجبارية.", reply_markup=kb)

        elif data == "add_insta_ch":
            if cid != ADMIN_ID: return
            try: ben.answer_callback_query(call.id)
            except: pass
            oo_set_session(cid, {"state": "admin_add_insta"})
            ben.send_message(cid, "📸 أرسل اسم الحساب ورابطه بالشكل التالي:\n\n<code>اسم الحساب | https://instagram.com/username</code>", parse_mode="HTML")

        elif data == "del_insta_ch":
            if cid != ADMIN_ID: return
            try: ben.answer_callback_query(call.id)
            except: pass
            _forced_instagram.clear()
            for u_id in _users:
                _users[u_id].pop("instagram_verified", None)
            _do_save()
            kb = Markup()
            kb.add(btn("رجوع", callback_data="admin_panel", color='primary'))
            try: ben.edit_message_text("✅ تم حذف جميع حسابات إنستغرام الإجبارية.", chat_id=cid, message_id=message_id, reply_markup=kb)
            except: ben.send_message(cid, "✅ تم حذف جميع حسابات إنستغرام الإجبارية.", reply_markup=kb)

        elif data == "broadcast_msg":
            if cid != ADMIN_ID: return
            try: ben.answer_callback_query(call.id)
            except: pass
            oo_set_session(cid, {"state": "admin_broadcast"})
            ben.send_message(cid, "✉️ <b>أرسل الآن نص الرسالة (يدعم HTML) التي تريد إذاعتها لجميع المستخدمين:</b>", parse_mode="HTML")

        elif data == "list_users_ids":
            if cid != ADMIN_ID: return
            try: ben.answer_callback_query(call.id)
            except: pass
            user_list_text = "🆔 <b>قائمة أيدي المستخدمين المسجلين:</b>\n\n"
            for uid, info in list(_users.items())[:40]:
                u_name = info.get("first_name", "مستخدم")
                u_username = f"@{info.get('username')}" if info.get('username') else "بدون يوزر"
                user_list_text += f"• <code>{uid}</code> | {u_name} ({u_username})\n"
            
            if len(_users) > 40:
                user_list_text += f"\n... و {len(_users) - 40} مستخدمين آخرين."
                
            kb = Markup()
            kb.add(btn("رجوع للوحة التحكم", callback_data="admin_panel", color='primary'))
            try: ben.edit_message_text(user_list_text, chat_id=cid, message_id=message_id, parse_mode="HTML", reply_markup=kb)
            except: ben.send_message(cid, user_list_text, parse_mode="HTML", reply_markup=kb)

        elif data == "bot_stats":
            if cid != ADMIN_ID: return
            try: ben.answer_callback_query(call.id)
            except: pass
            total_u = len(_users)
            acts = _bot_stats.get("activations", 0)
            stats_text = (
                f"📊 <b>الإحصائيات الشاملة للبوت:</b>\n\n"
                f"👥 إجمالي المستخدمين: <b>{total_u}</b>\n"
                f"🎉 عمليات التفعيل الناجحة: <b>{acts}</b>\n"
                f"📌 قنوات تليجرام: <b>{len(_forced_channels)}</b>\n"
                f"📸 حسابات إنستغرام: <b>{len(_forced_instagram)}</b>"
            )
            kb = Markup()
            kb.add(btn("رجوع للوحة التحكم", callback_data="admin_panel", color='primary'))
            try: ben.edit_message_text(stats_text, chat_id=cid, message_id=message_id, parse_mode="HTML", reply_markup=kb)
            except: ben.send_message(cid, stats_text, parse_mode="HTML", reply_markup=kb)

        elif data == "change_phone":
            if check_user_subscription(cid) != True:
                try: ben.answer_callback_query(call.id, "⚠️ يجب إتمام الاشتراكات الإجبارية أولاً!", show_alert=True)
                except: pass
                return
            try: ben.answer_callback_query(call.id, "جاري الإعداد...")
            except: pass
            oo_delete_user(cid)
            oo_clear_session(cid)
            oo_set_session(cid, {"state": "awaiting_phone"})
            try: ben.edit_message_text("📱 أدخل رقم أوريدو (05XXXXXXXX):", chat_id=cid, message_id=message_id, parse_mode="HTML")
            except: ben.send_message(cid, "📱 أدخل رقم أوريدو (05XXXXXXXX):", parse_mode="HTML")
            
        elif data == "resend_otp":
            wait = _check_otp_cooldown(cid)
            if wait > 0:
                try: ben.answer_callback_query(call.id, f"انتظر {wait} ثانية", show_alert=True)
                except: pass
                return
            try: ben.answer_callback_query(call.id, "جاري الإعادة...")
            except: pass
            sess = oo_get_session(cid)
            msisdn = sess.get("msisdn") or (user.get("msisdn") if user else None)
            if msisdn:
                oo_send_otp(msisdn)
                ben.send_message(cid, "✅ تم إرسال رمز جديد.")

        elif data == "do_2g":
            if check_user_subscription(cid) != True:
                try: ben.answer_callback_query(call.id, "⚠️ يجب إتمام الاشتراكات الإجبارية أولاً!", show_alert=True)
                except: pass
                send_subscription_warning(cid, message_id)
                return
            try: ben.answer_callback_query(call.id, "جاري المعالجة...")
            except: pass
            threading.Thread(target=oo_do_free_2go, args=(cid, user, message_id), daemon=True).start()

    except Exception as e:
        logger.exception(f"callback error: {e}")

# ═══════════════════════════ Main Execution ═══════════════════════════
def run():
    _load_from_disk()
    # تشغيل خادم الويب الخفي في الخلفية لإرضاء Render وفتح المنفذ
    threading.Thread(target=run_web_server, daemon=True).start()
    print('[+] Bot Started Successfully with Web Port & /start Fixed!')
    ben.infinity_polling(skip_pending=True)

if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        with _lock: _do_save()
