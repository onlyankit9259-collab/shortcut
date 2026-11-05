# Shortcut Guru Android app

`app/ShortcutGuru.apk` is the Android app. It shows the website (bundled
inside the APK, so it works offline), opens YouTube/Instagram links in their
apps, opens the PDFs in the phone's PDF viewer, and its Copy buttons copy to
the phone's clipboard. Needs Android 7.0 or newer.

## Rebuild

Needs Python 3 and a JDK (Java 17+). No Android SDK is needed; the build
downloads three jars from Maven Central into `android/.build/tools/`.

```bash
python3 android/build_apk.py --keystore /path/to/shortcutguru-release.p12
```

Use the same keystore (and password, `SG_KEYSTORE_PASSWORD`, default
`shortcutguru`) every time. Phones only install an update over the old app
when both are signed with the same key. If no keystore exists at that path,
a new one is created.

Before each new release, raise `VERSION_CODE` (and `VERSION_NAME`) in
`android/build_apk.py`.
