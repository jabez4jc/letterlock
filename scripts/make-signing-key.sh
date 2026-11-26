#!/usr/bin/env bash
# Creates the Letterlock release signing key and prints what to paste into GitHub secrets.
# Run it once, on your own computer (needs a JDK for `keytool`).
#   bash scripts/make-signing-key.sh [output-dir]      (default: ~/letterlock-signing)
# Back up the output folder somewhere safe (a password manager or private drive). Without this key you
# cannot ship updates that install over existing copies of the app. Never commit it to the repo.
set -euo pipefail
out="${1:-$HOME/letterlock-signing}"
command -v keytool >/dev/null || { echo "keytool not found: install a JDK (e.g. Temurin 21) first." >&2; exit 1; }
mkdir -p "$out"; chmod 700 "$out"
ks="$out/letterlock-release.jks"
[ -e "$ks" ] && { echo "$ks already exists. Delete it first if you really want a new key." >&2; exit 1; }
pass="$(od -An -N24 -tx1 /dev/urandom | tr -d ' \n')"   # 48 hex chars
alias=letterlock
keytool -genkeypair -keystore "$ks" -storetype PKCS12 -alias "$alias" -keyalg RSA -keysize 4096 -validity 10000 \
  -storepass "$pass" -keypass "$pass" -dname "CN=Letterlock" >/dev/null
base64 < "$ks" | tr -d '\n' > "$out/keystore.base64.txt"
printf 'storeFile=%s\nstorePassword=%s\nkeyAlias=%s\nkeyPassword=%s\n' "$ks" "$pass" "$alias" "$pass" > "$out/keystore.properties"
chmod 600 "$out"/*
here="$(cd "$(dirname "$0")/.." && pwd)"
cp "$out/keystore.properties" "$here/android/keystore.properties"   # lets `npm run apk:release` sign locally (git-ignored)
cat <<MSG

Key created in $out
Add these 4 repository secrets on GitHub (Settings → Secrets and variables → Actions → New repository secret):

  ANDROID_KEYSTORE_BASE64   = the contents of $out/keystore.base64.txt
  ANDROID_KEYSTORE_PASSWORD = $pass
  ANDROID_KEY_ALIAS         = $alias
  ANDROID_KEY_PASSWORD      = $pass

Then back up $out and keep it private.
MSG
