package com.shortcutguru.app;

import android.content.ContentProvider;
import android.content.ContentValues;
import android.content.res.AssetFileDescriptor;
import android.database.Cursor;
import android.database.MatrixCursor;
import android.net.Uri;

import java.io.FileNotFoundException;
import java.io.IOException;

/**
 * Lets the phone's PDF viewer read the PDFs bundled in assets/site.
 * Not exported: other apps only get access to a single PDF when
 * the app opens it for them.
 */
public class AssetProvider extends ContentProvider {

    public static final String AUTHORITY = "com.shortcutguru.app.assets";

    @Override
    public boolean onCreate() {
        return true;
    }

    private String assetPath(Uri uri) throws FileNotFoundException {
        String path = uri.getPath();
        if (path == null || path.contains("..") || !path.toLowerCase().endsWith(".pdf")) {
            throw new FileNotFoundException(String.valueOf(uri));
        }
        return "site" + path;
    }

    @Override
    public AssetFileDescriptor openAssetFile(Uri uri, String mode) throws FileNotFoundException {
        try {
            return getContext().getAssets().openFd(assetPath(uri));
        } catch (IOException e) {
            throw new FileNotFoundException(e.getMessage());
        }
    }

    @Override
    public String getType(Uri uri) {
        return "application/pdf";
    }

    @Override
    public Cursor query(Uri uri, String[] projection, String selection, String[] selectionArgs, String sortOrder) {
        String name = uri.getLastPathSegment();
        long size = -1;
        try {
            AssetFileDescriptor fd = getContext().getAssets().openFd(assetPath(uri));
            size = fd.getLength();
            fd.close();
        } catch (IOException ignored) {
            // size stays unknown
        }
        MatrixCursor cursor = new MatrixCursor(new String[] {"_display_name", "_size"});
        cursor.addRow(new Object[] {name, size});
        return cursor;
    }

    @Override
    public Uri insert(Uri uri, ContentValues values) {
        return null;
    }

    @Override
    public int delete(Uri uri, String selection, String[] selectionArgs) {
        return 0;
    }

    @Override
    public int update(Uri uri, ContentValues values, String selection, String[] selectionArgs) {
        return 0;
    }
}
