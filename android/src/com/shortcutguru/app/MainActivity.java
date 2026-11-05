package com.shortcutguru.app;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.view.Window;
import android.webkit.JavascriptInterface;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

/**
 * Shortcut Guru Android app: shows the website bundled in assets/site,
 * so it works offline. Outside links open in the phone's browser or apps,
 * and PDFs open in the phone's PDF viewer.
 */
public class MainActivity extends Activity {

    private static final String HOME = "file:///android_asset/site/index.html";
    private static final String ASSET_PREFIX = "file:///android_asset/site/";

    private WebView webView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        colorSystemBars();

        webView = new WebView(this);
        webView.setBackgroundColor(Color.parseColor("#080808"));
        setContentView(webView);

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(true);

        webView.addJavascriptInterface(new Bridge(), "ShortcutGuruApp");
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                return handleUrl(url);
            }

            @Override
            public void onPageFinished(WebView view, String url) {
                view.loadUrl("javascript:(function(){"
                        // Install buttons are for the website only.
                        + "['installBtn','installHelp','apkBtn'].forEach(function(id){"
                        + "var e=document.getElementById(id);if(e){e.hidden=true;e.style.display='none';}});"
                        // Copy buttons: use Android clipboard.
                        + "var w=function(t){ShortcutGuruApp.copy(String(t));return Promise.resolve();};"
                        + "try{if(navigator.clipboard){navigator.clipboard.writeText=w;}"
                        + "else{Object.defineProperty(navigator,'clipboard',{value:{writeText:w}});}}catch(e){}"
                        + "})()");
            }
        });

        if (savedInstanceState != null) {
            webView.restoreState(savedInstanceState);
        } else {
            webView.loadUrl(HOME);
        }
    }

    private boolean handleUrl(String url) {
        if (url.startsWith(ASSET_PREFIX)) {
            String path = url.substring(ASSET_PREFIX.length());
            String fragment = "";
            int cut = path.indexOf('#');
            if (cut >= 0) {
                fragment = path.substring(cut);
                path = path.substring(0, cut);
            }
            if (path.isEmpty()) {
                // "Home" links point at the folder ("./"); open index.html.
                webView.loadUrl(HOME + fragment);
                return true;
            }
            if (path.toLowerCase().endsWith(".pdf")) {
                openPdf(path);
                return true;
            }
            return false;
        }
        // YouTube, Instagram and any other website: open outside the app.
        try {
            startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url)));
        } catch (ActivityNotFoundException e) {
            Toast.makeText(this, "Link nahi khul paya", Toast.LENGTH_SHORT).show();
        }
        return true;
    }

    private void openPdf(String assetPath) {
        Uri uri = Uri.parse("content://" + AssetProvider.AUTHORITY + "/" + assetPath);
        Intent intent = new Intent(Intent.ACTION_VIEW);
        intent.setDataAndType(uri, "application/pdf");
        intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
        try {
            startActivity(Intent.createChooser(intent, "PDF kholein"));
        } catch (ActivityNotFoundException e) {
            Toast.makeText(this, "PDF kholne ke liye koi PDF app install karein", Toast.LENGTH_LONG).show();
        }
    }

    private void colorSystemBars() {
        // Window.setStatusBarColor exists from Android 5.0; called by reflection
        // so the app still compiles against the older android.jar.
        try {
            Window window = getWindow();
            window.addFlags(0x80000000); // FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS
            int dark = Color.parseColor("#111111");
            Window.class.getMethod("setStatusBarColor", int.class).invoke(window, dark);
            Window.class.getMethod("setNavigationBarColor", int.class).invoke(window, dark);
        } catch (Exception ignored) {
            // Older Android: default bar colors.
        }
    }

    @Override
    protected void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
        webView.saveState(outState);
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }

    private class Bridge {
        @JavascriptInterface
        public void copy(final String text) {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    ClipboardManager cm = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
                    cm.setPrimaryClip(ClipData.newPlainText("Shortcut Guru", text));
                }
            });
        }
    }
}
