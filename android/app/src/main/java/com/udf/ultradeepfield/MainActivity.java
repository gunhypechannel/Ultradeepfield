package com.udf.ultradeepfield;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.ContentValues;
import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.Looper;
import android.provider.MediaStore;
import android.util.Base64;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowInsets;
import android.webkit.CookieManager;
import android.webkit.JavascriptInterface;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;
import android.widget.Toast;
import android.window.OnBackInvokedDispatcher;

import androidx.core.splashscreen.SplashScreen;

import java.io.File;
import java.io.FileOutputStream;
import java.io.OutputStream;

/**
 * Ultra Deep Field as a WebView app: the game's website runs inside this app (not in Chrome, as the TWA did).
 * The site itself is unchanged; this wrapper adds a splash screen, an offline screen with Retry, the back button,
 * file import (the empire file) and file saving (screenshots and empire exports, which a WebView cannot download by itself).
 */
public class MainActivity extends Activity {
    static final String HOST = "gunhypechannel.github.io";
    static final String PATH = "/Ultradeepfield";
    static final String START = "https://" + HOST + PATH + "/";
    static final int PICK = 41;

    WebView web;
    boolean loaded = false, offline = false;
    ValueCallback<Uri[]> pickCb;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle saved) {
        SplashScreen splash = SplashScreen.installSplashScreen(this);
        super.onCreate(saved);
        final long t0 = System.currentTimeMillis();
        splash.setKeepOnScreenCondition(() -> !loaded && System.currentTimeMillis() - t0 < 4000);

        FrameLayout root = new FrameLayout(this);
        root.setBackgroundColor(Color.parseColor("#05090F"));
        web = new WebView(this);
        web.setBackgroundColor(Color.parseColor("#05090F"));
        root.addView(web, new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
        setContentView(root);
        // keep the page clear of the status bar, navigation bar and camera cutout (edge-to-edge on Android 15+)
        root.setOnApplyWindowInsetsListener((v, ins) -> {
            int l, t, r, b;
            if (Build.VERSION.SDK_INT >= 30) {
                android.graphics.Insets i = ins.getInsets(WindowInsets.Type.systemBars() | WindowInsets.Type.displayCutout() | WindowInsets.Type.ime());
                l = i.left; t = i.top; r = i.right; b = i.bottom;
            } else { l = ins.getSystemWindowInsetLeft(); t = ins.getSystemWindowInsetTop(); r = ins.getSystemWindowInsetRight(); b = ins.getSystemWindowInsetBottom(); }
            v.setPadding(l, t, r, b);
            return ins;
        });

        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setDatabaseEnabled(true);
        s.setMediaPlaybackRequiresUserGesture(false);
        s.setLoadWithOverviewMode(true);
        s.setUseWideViewPort(true);
        s.setSupportZoom(false);
        s.setAllowFileAccess(false);
        s.setAllowContentAccess(false);
        s.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        s.setUserAgentString(s.getUserAgentString() + " UDFApp/1.0.1");
        CookieManager.getInstance().setAcceptCookie(true);
        CookieManager.getInstance().setAcceptThirdPartyCookies(web, true);
        web.addJavascriptInterface(new Native(), "UDFNative");

        web.setWebViewClient(new WebViewClient() {
            @Override public boolean shouldOverrideUrlLoading(WebView v, WebResourceRequest req) {
                if (!req.isForMainFrame()) return false;
                return route(req.getUrl());
            }
            @Override public void onPageFinished(WebView v, String url) {
                loaded = true;
                if (!offline) v.evaluateJavascript(SAVE_JS, null);
            }
            @Override public void onReceivedError(WebView v, WebResourceRequest req, WebResourceError err) {
                if (req.isForMainFrame()) showOffline();
            }
            /* if the page's renderer dies (low memory), start the page again instead of letting Android close the app */
            @Override public boolean onRenderProcessGone(WebView v, android.webkit.RenderProcessGoneDetail d) {
                if (v == web) { ((ViewGroup) v.getParent()).removeView(v); v.destroy(); web = null; recreate(); }
                return true;
            }
        });
        web.setWebChromeClient(new WebChromeClient() {
            @Override public boolean onShowFileChooser(WebView v, ValueCallback<Uri[]> cb, FileChooserParams p) {
                if (pickCb != null) pickCb.onReceiveValue(null);
                pickCb = cb;
                Intent i = new Intent(Intent.ACTION_GET_CONTENT);
                i.addCategory(Intent.CATEGORY_OPENABLE);
                i.setType("*/*");
                try { startActivityForResult(Intent.createChooser(i, "Choose a file"), PICK); }
                catch (ActivityNotFoundException e) { pickCb = null; cb.onReceiveValue(null); return false; }
                return true;
            }
        });

        if (Build.VERSION.SDK_INT >= 33) {
            getOnBackInvokedDispatcher().registerOnBackInvokedCallback(OnBackInvokedDispatcher.PRIORITY_DEFAULT, this::back);
        }

        if (saved != null) web.restoreState(saved);
        else web.loadUrl(START);

        // when the connection comes back while the offline screen is up, load the game again by itself
        try {
            android.net.ConnectivityManager cm = (android.net.ConnectivityManager) getSystemService(CONNECTIVITY_SERVICE);
            netCb = new android.net.ConnectivityManager.NetworkCallback() {
                @Override public void onAvailable(android.net.Network n) {
                    new Handler(Looper.getMainLooper()).postDelayed(() -> { if (offline && web != null) { offline = false; web.loadUrl(START); } }, 1500);
                }
            };
            cm.registerDefaultNetworkCallback(netCb);
        } catch (Exception e) { netCb = null; }
    }
    android.net.ConnectivityManager.NetworkCallback netCb;

    /** Our own pages stay in the app; other websites, email and store links open outside it. */
    boolean route(Uri u) {
        String sc = u.getScheme() == null ? "" : u.getScheme();
        if ((sc.equals("https") || sc.equals("http")) && HOST.equalsIgnoreCase(u.getHost())
                && u.getPath() != null && u.getPath().startsWith(PATH)) return false;
        if (sc.equals("https") || sc.equals("http") || sc.equals("mailto") || sc.equals("market") || sc.equals("tel") || sc.equals("intent")) {
            try {
                Intent i = sc.equals("intent") ? Intent.parseUri(u.toString(), Intent.URI_INTENT_SCHEME) : new Intent(Intent.ACTION_VIEW, u);
                i.addCategory(Intent.CATEGORY_BROWSABLE);
                i.setComponent(null);
                startActivity(i);
            } catch (Exception e) { /* nothing can open it */ }
            return true;
        }
        return true;
    }

    void showOffline() {
        offline = true;
        loaded = true;
        web.loadDataWithBaseURL("https://" + HOST + PATH + "/offline", OFFLINE_HTML, "text/html", "utf-8", null);
    }

    void back() {
        if (web == null) return;
        if (offline) { moveTaskToBack(true); return; }
        if (web.canGoBack()) web.goBack();
        else moveTaskToBack(true);
    }

    @SuppressWarnings("deprecation")
    @Override public void onBackPressed() { back(); }

    @Override protected void onSaveInstanceState(Bundle out) { super.onSaveInstanceState(out); if (web != null) web.saveState(out); }
    @Override protected void onPause() { super.onPause(); if (web != null) web.onPause(); CookieManager.getInstance().flush(); }
    @Override protected void onResume() { super.onResume(); if (web != null) web.onResume(); }
    @Override protected void onDestroy() {
        try { if (netCb != null) ((android.net.ConnectivityManager) getSystemService(CONNECTIVITY_SERVICE)).unregisterNetworkCallback(netCb); } catch (Exception e) { }
        if (web != null) { web.destroy(); } super.onDestroy(); }

    @Override protected void onActivityResult(int req, int res, Intent data) {
        if (req == PICK && pickCb != null) {
            Uri[] out = null;
            if (res == RESULT_OK && data != null) {
                if (data.getClipData() != null) {
                    out = new Uri[data.getClipData().getItemCount()];
                    for (int i = 0; i < out.length; i++) out[i] = data.getClipData().getItemAt(i).getUri();
                } else if (data.getData() != null) out = new Uri[]{data.getData()};
            }
            pickCb.onReceiveValue(out);
            pickCb = null;
            return;
        }
        super.onActivityResult(req, res, data);
    }

    /** Saves files the game offers (screenshots, empire exports) into the phone's Downloads folder. */
    class Native {
        @JavascriptInterface public void saveFile(String b64, String mime, String name) {
            String nm = (name == null || name.isEmpty()) ? "udf-file" : name.replaceAll("[\\\\/:*?\"<>|]", "_");
            String mt = (mime == null || mime.isEmpty()) ? "application/octet-stream" : mime;
            try {
                byte[] bytes = Base64.decode(b64, Base64.DEFAULT);
                if (Build.VERSION.SDK_INT >= 29) {
                    ContentValues cv = new ContentValues();
                    cv.put(MediaStore.Downloads.DISPLAY_NAME, nm);
                    cv.put(MediaStore.Downloads.MIME_TYPE, mt);
                    Uri uri = getContentResolver().insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, cv);
                    if (uri == null) throw new Exception("no uri");
                    try (OutputStream os = getContentResolver().openOutputStream(uri)) { os.write(bytes); }
                    toast("Saved to Downloads: " + nm);
                } else {
                    File dir = getExternalFilesDir(Environment.DIRECTORY_DOWNLOADS);
                    File f = new File(dir, nm);
                    try (FileOutputStream os = new FileOutputStream(f)) { os.write(bytes); }
                    toast("Saved: " + f.getAbsolutePath());
                }
            } catch (Exception e) { toast("Couldn't save the file."); }
        }
        @JavascriptInterface public void retry() {
            new Handler(Looper.getMainLooper()).post(() -> { offline = false; web.loadUrl(START); });
        }
    }

    void toast(String t) { new Handler(Looper.getMainLooper()).post(() -> Toast.makeText(this, t, Toast.LENGTH_LONG).show()); }

    /* A WebView cannot download blob: links, so links the game clicks to save a file are handed to UDFNative.saveFile. */
    static final String SAVE_JS =
        "(function(){if(window.__udfSave)return;window.__udfSave=1;" +
        "document.addEventListener('click',function(e){var a=e.target&&e.target.closest?e.target.closest('a[download]'):null;" +
        "if(!a||!/^(blob:|data:)/.test(a.href))return;e.preventDefault();e.stopPropagation();" +
        "fetch(a.href).then(function(r){return r.blob();}).then(function(b){var fr=new FileReader();fr.onload=function(){" +
        "var s=String(fr.result),i=s.indexOf(',');UDFNative.saveFile(s.slice(i+1),b.type||'',a.download||'udf-file');};fr.readAsDataURL(b);});},true);})();";

    static final String OFFLINE_HTML =
        "<!doctype html><html><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>" +
        "<style>html,body{margin:0;height:100%;background:#05090f;color:#d8e6ef;font-family:sans-serif}" +
        "main{height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;padding:24px;box-sizing:border-box;text-align:center}" +
        "h1{font-size:22px;margin:0;color:#fff}p{margin:0;max-width:300px;line-height:1.45;color:#9fb3c1}" +
        "button{margin-top:8px;font-size:16px;font-weight:700;padding:12px 34px;border-radius:12px;border:1px solid #ffb84a;background:#ffb84a;color:#1a1204}</style></head>" +
        "<body><main><svg width=64 height=64 viewBox='0 0 24 24' fill='none' stroke='#ffb84a' stroke-width='1.6'><path d='M2 9a16 16 0 0 1 20 0M5 12.5a11 11 0 0 1 14 0M8.5 16a6 6 0 0 1 7 0'/><circle cx=12 cy=19.5 r=1.2 fill='#ffb84a'/><path d='M3 3l18 18'/></svg>" +
        "<h1>No signal, Commander</h1><p>Ultra Deep Field needs an internet connection. Check your Wi-Fi or mobile data, then try again.</p>" +
        "<button onclick='UDFNative.retry()'>Retry</button></main></body></html>";
}
