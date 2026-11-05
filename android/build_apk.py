#!/usr/bin/env python3
"""Build the Shortcut Guru Android app (APK) without the Android SDK.

The app is a WebView that shows the website bundled inside the APK, so it
works offline. Tools come from Maven Central only:
  - android.jar (com.google.android:android:4.1.1.4) to compile against
  - dx (com.jakewharton.android.repackaged:dalvik-dx) to make classes.dex
  - apksig (com.android.tools.build:apksig) to sign the APK
AndroidManifest.xml and resources.arsc are written in Android's binary
format by this script.

Usage:
  python3 android/build_apk.py [--keystore PATH] [--out PATH]

Keep the keystore safe: phones only accept an update of the app when it is
signed with the same key.
"""
import argparse
import os
import shutil
import struct
import subprocess
import sys
import urllib.request
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.join(ROOT, "android")
BUILD = os.path.join(HERE, ".build")

PACKAGE = "com.shortcutguru.app"
APP_NAME = "Shortcut Guru"
VERSION_CODE = 1
VERSION_NAME = "1.0"
MIN_SDK = 24  # Android 7.0+: APK Signature Scheme v2 only
TARGET_SDK = 34

MAVEN = "https://repo1.maven.org/maven2/"
TOOLS = {
    "android.jar": "com/google/android/android/4.1.1.4/android-4.1.1.4.jar",
    "dx.jar": "com/jakewharton/android/repackaged/dalvik-dx/16.0.1/dalvik-dx-16.0.1.jar",
    "apksig.jar": "com/android/tools/build/apksig/2.3.0/apksig-2.3.0.jar",
}

# android.R.attr / android.R.style ids (public framework resource ids)
ATTR = {
    "theme": 0x01010000,
    "label": 0x01010001,
    "icon": 0x01010002,
    "name": 0x01010003,
    "exported": 0x01010010,
    "authorities": 0x01010018,
    "grantUriPermissions": 0x0101001B,
    "configChanges": 0x0101001F,
    "minSdkVersion": 0x0101020C,
    "versionCode": 0x0101021B,
    "versionName": 0x0101021C,
    "targetSdkVersion": 0x01010270,
    "allowBackup": 0x01010280,
    "hardwareAccelerated": 0x010102D3,
}
THEME_DEVICE_DEFAULT_NO_ACTION_BAR = 0x01030129
ICON_RES_ID = 0x7F010000  # @mipmap/ic_launcher (from resources.arsc below)
ANDROID_NS = "http://schemas.android.com/apk/res/android"

# Res_value data types
T_REF, T_STRING, T_INT_DEC, T_INT_HEX, T_BOOL = 0x01, 0x03, 0x10, 0x11, 0x12


def run(cmd):
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def fetch_tools():
    os.makedirs(os.path.join(BUILD, "tools"), exist_ok=True)
    paths = {}
    for name, rel in TOOLS.items():
        path = os.path.join(BUILD, "tools", name)
        if not os.path.exists(path):
            print("downloading", rel)
            urllib.request.urlretrieve(MAVEN + rel, path)
        paths[name] = path
    return paths


# ---------------------------------------------------------------- binary XML

def string_pool(strings):
    """ResStringPool chunk, UTF-16 strings."""
    offsets, data = [], b""
    for s in strings:
        offsets.append(len(data))
        units = s.encode("utf-16-le")
        n = len(units) // 2
        assert n < 0x8000
        data += struct.pack("<H", n) + units + b"\x00\x00"
    while len(data) % 4:
        data += b"\x00"
    header_size = 28
    strings_start = header_size + 4 * len(strings)
    size = strings_start + len(data)
    return (struct.pack("<HHIIIIII", 0x0001, header_size, size, len(strings), 0, 0,
                        strings_start, 0)
            + b"".join(struct.pack("<I", o) for o in offsets) + data)


class Element:
    def __init__(self, tag, attrs=(), children=()):
        self.tag, self.attrs, self.children = tag, list(attrs), list(children)


def a(name, kind, value, ns=True):
    """Attribute: (android-namespace?, name, type, value)."""
    return (ns, name, kind, value)


def encode_axml(root):
    # Attribute names that carry an android resource id come first in the
    # pool, in the same order as the resource map.
    res_names = []

    def walk(el):
        for ns, name, _, _ in el.attrs:
            if ns and name not in res_names:
                res_names.append(name)
        for c in el.children:
            walk(c)

    walk(root)
    strings = list(res_names)

    def idx(s):
        if s not in strings:
            strings.append(s)
        return strings.index(s)

    for s in ("android", ANDROID_NS):
        idx(s)

    body = b""
    ns_uri = idx(ANDROID_NS)

    def attr_sort_key(attr):
        ns, name = attr[0], attr[1]
        return ATTR[name] if ns else 0

    def emit(el):
        nonlocal body
        attrs = sorted(el.attrs, key=attr_sort_key)
        encoded = b""
        for ns, name, kind, value in attrs:
            raw = 0xFFFFFFFF
            if kind == T_STRING:
                data = idx(value)
                raw = data
            elif kind == T_BOOL:
                data = 0xFFFFFFFF if value else 0
            else:
                data = value
            encoded += struct.pack("<IIIHBBI", ns_uri if ns else 0xFFFFFFFF, idx(name), raw,
                                   8, 0, kind, data)
        ext = struct.pack("<IIHHHHHH", 0xFFFFFFFF, idx(el.tag), 20, 20, len(attrs), 0, 0, 0)
        chunk = ext + encoded
        body += struct.pack("<HHIII", 0x0102, 16, 16 + len(chunk), 1, 0xFFFFFFFF) + chunk
        for c in el.children:
            emit(c)
        body += struct.pack("<HHIIIII", 0x0103, 16, 24, 1, 0xFFFFFFFF, 0xFFFFFFFF, idx(el.tag))

    prefix = idx("android")
    start_ns = struct.pack("<HHIIIII", 0x0100, 16, 24, 1, 0xFFFFFFFF, prefix, ns_uri)
    emit(root)
    end_ns = struct.pack("<HHIIIII", 0x0101, 16, 24, 1, 0xFFFFFFFF, prefix, ns_uri)

    pool = string_pool(strings)
    res_map = struct.pack("<HHI", 0x0180, 8, 8 + 4 * len(res_names)) + b"".join(
        struct.pack("<I", ATTR[n]) for n in res_names)
    content = pool + res_map + start_ns + body + end_ns
    return struct.pack("<HHI", 0x0003, 8, 8 + len(content)) + content


def manifest():
    activity = Element("activity", [
        a("name", T_STRING, PACKAGE + ".MainActivity"),
        a("exported", T_BOOL, True),
        a("label", T_STRING, APP_NAME),
        # orientation|keyboardHidden|keyboard|screenSize|screenLayout|smallestScreenSize
        a("configChanges", T_INT_HEX, 0x0080 | 0x0020 | 0x0010 | 0x0400 | 0x0100 | 0x0800),
    ], [
        Element("intent-filter", [], [
            Element("action", [a("name", T_STRING, "android.intent.action.MAIN")]),
            Element("category", [a("name", T_STRING, "android.intent.category.LAUNCHER")]),
        ]),
    ])
    provider = Element("provider", [
        a("name", T_STRING, PACKAGE + ".AssetProvider"),
        a("exported", T_BOOL, False),
        a("authorities", T_STRING, PACKAGE + ".assets"),
        a("grantUriPermissions", T_BOOL, True),
    ])
    application = Element("application", [
        a("label", T_STRING, APP_NAME),
        a("icon", T_REF, ICON_RES_ID),
        a("theme", T_REF, THEME_DEVICE_DEFAULT_NO_ACTION_BAR),
        a("allowBackup", T_BOOL, True),
        a("hardwareAccelerated", T_BOOL, True),
    ], [activity, provider])
    root = Element("manifest", [
        a("package", T_STRING, PACKAGE, ns=False),
        a("versionCode", T_INT_DEC, VERSION_CODE),
        a("versionName", T_STRING, VERSION_NAME),
    ], [
        Element("uses-sdk", [
            a("minSdkVersion", T_INT_DEC, MIN_SDK),
            a("targetSdkVersion", T_INT_DEC, TARGET_SDK),
        ]),
        application,
    ])
    return encode_axml(root)


def resources_arsc(icon_path):
    """resources.arsc with one resource: mipmap/ic_launcher -> icon_path."""
    global_pool = string_pool([icon_path])
    type_pool = string_pool(["mipmap"])
    key_pool = string_pool(["ic_launcher"])

    type_spec = struct.pack("<HHIBBHI", 0x0202, 16, 16 + 4, 1, 0, 0, 1) + struct.pack("<I", 0)

    config = struct.pack("<I", 64) + b"\x00" * 60  # default configuration
    header_size = 20 + len(config)
    entries_start = header_size + 4
    entry = struct.pack("<HHI", 8, 0, 0) + struct.pack("<HBBI", 8, 0, T_STRING, 0)
    type_chunk = (struct.pack("<HHIBBHII", 0x0201, header_size, entries_start + len(entry),
                              1, 0, 0, 1, entries_start)
                  + config + struct.pack("<I", 0) + entry)

    pkg_header_size = 288
    name = PACKAGE.encode("utf-16-le").ljust(256, b"\x00")
    type_strings_off = pkg_header_size
    key_strings_off = type_strings_off + len(type_pool)
    pkg_body = type_pool + key_pool + type_spec + type_chunk
    package = struct.pack("<HHII", 0x0200, pkg_header_size, pkg_header_size + len(pkg_body),
                          0x7F) + name + struct.pack("<IIIII", type_strings_off, 1,
                                                     key_strings_off, 1, 0) + pkg_body
    assert len(package) == pkg_header_size + len(pkg_body)

    content = global_pool + package
    return struct.pack("<HHII", 0x0002, 12, 12 + len(content), 1) + content


# ------------------------------------------------------------------ zip/apk

def write_apk(path, entries):
    """entries: list of (name, bytes, stored?). Stored entries are 4-byte aligned."""
    with zipfile.ZipFile(path, "w") as zf:
        for name, data, stored in entries:
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 0
            if stored:
                info.compress_type = zipfile.ZIP_STORED
                data_start = zf.fp.tell() + 30 + len(name.encode())
                pad = (-(data_start + 6)) % 4
                # 0xD935 = Android zipalign extra field: alignment + padding
                info.extra = struct.pack("<HHH", 0xD935, 2 + pad, 4) + b"\x00" * pad
            else:
                info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, data)
    with zipfile.ZipFile(path) as zf:
        check_alignment(path, zf)


def check_alignment(path, zf):
    with open(path, "rb") as f:
        for info in zf.infolist():
            if info.compress_type != zipfile.ZIP_STORED:
                continue
            f.seek(info.header_offset + 26)
            n, m = struct.unpack("<HH", f.read(4))
            start = info.header_offset + 30 + n + m
            if start % 4:
                raise SystemExit(f"not 4-byte aligned: {info.filename}")


def site_files():
    files = [(n, False) for n in sorted(os.listdir(ROOT)) if n.endswith(".html")]
    for folder in ("pdf", "icons", "assets"):
        for dirpath, _, names in os.walk(os.path.join(ROOT, folder)):
            for n in sorted(names):
                rel = os.path.relpath(os.path.join(dirpath, n), ROOT)
                if n.lower().endswith(".pdf"):
                    files.append((rel, True))  # stored: AssetProvider uses openFd
                elif n.lower().endswith((".png", ".css")):
                    files.append((rel, False))
    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--keystore", default=os.path.join(BUILD, "shortcutguru-release.p12"))
    parser.add_argument("--password", default=os.environ.get("SG_KEYSTORE_PASSWORD", "shortcutguru"))
    parser.add_argument("--out", default=os.path.join(ROOT, "app", "ShortcutGuru.apk"))
    args = parser.parse_args()

    tools = fetch_tools()
    work = os.path.join(BUILD, "work")
    shutil.rmtree(work, ignore_errors=True)
    classes = os.path.join(work, "classes")
    os.makedirs(classes)

    sources = []
    for base in ("src", "stubs"):
        for dirpath, _, names in os.walk(os.path.join(HERE, base)):
            sources += [os.path.join(dirpath, n) for n in names if n.endswith(".java")]
    run(["javac", "-nowarn", "--release", "8", "-cp", tools["android.jar"], "-d", classes] + sources)
    shutil.rmtree(os.path.join(classes, "android"))  # stub; phone provides the real one
    dex = os.path.join(work, "classes.dex")
    run(["java", "-cp", tools["dx.jar"], "com.android.dx.command.Main", "--dex",
         "--min-sdk-version=" + str(MIN_SDK), "--output=" + dex, classes])

    icon_name = "res/mipmap/ic_launcher.png"
    with open(os.path.join(ROOT, "icons", "icon-192.png"), "rb") as f:
        icon = f.read()

    entries = [
        ("AndroidManifest.xml", manifest(), False),
        ("classes.dex", open(dex, "rb").read(), False),
        ("resources.arsc", resources_arsc(icon_name), True),
        (icon_name, icon, True),
    ]
    for rel, stored in site_files():
        with open(os.path.join(ROOT, rel), "rb") as f:
            entries.append(("assets/site/" + rel.replace(os.sep, "/"), f.read(), stored))

    unsigned = os.path.join(work, "unsigned.apk")
    write_apk(unsigned, entries)

    if not os.path.exists(args.keystore):
        os.makedirs(os.path.dirname(args.keystore), exist_ok=True)
        run(["keytool", "-genkeypair", "-keystore", args.keystore, "-storetype", "PKCS12",
             "-alias", "shortcutguru", "-keyalg", "RSA", "-keysize", "2048",
             "-validity", "10000", "-storepass", args.password, "-keypass", args.password,
             "-dname", "CN=Shortcut Guru, O=Shortcut Guru, C=IN"])

    signer_classes = os.path.join(work, "signer")
    run(["javac", "-nowarn", "-cp", tools["apksig.jar"], "-d", signer_classes,
         os.path.join(HERE, "tools", "SignApk.java")])
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    # apksig 2.3.0 uses JDK-internal X.509 classes; allow that on Java 9+.
    run(["java", "--add-exports", "java.base/sun.security.x509=ALL-UNNAMED",
         "--add-exports", "java.base/sun.security.pkcs=ALL-UNNAMED",
         "--add-exports", "java.base/sun.security.util=ALL-UNNAMED",
         "-cp", signer_classes + os.pathsep + tools["apksig.jar"], "SignApk",
         unsigned, args.out, args.keystore, "shortcutguru", args.password, str(MIN_SDK)])
    with zipfile.ZipFile(args.out) as zf:
        check_alignment(args.out, zf)
    print("APK ready:", args.out, os.path.getsize(args.out), "bytes")


if __name__ == "__main__":
    sys.exit(main())
