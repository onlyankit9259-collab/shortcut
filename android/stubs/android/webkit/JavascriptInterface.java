package android.webkit;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Compile-time copy of the Android 4.2+ annotation (the android.jar used
 * for building is Android 4.1). Not packaged into the app: the phone's own
 * android.webkit.JavascriptInterface is used at runtime.
 */
@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.METHOD})
public @interface JavascriptInterface {
}
