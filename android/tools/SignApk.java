import com.android.apksig.ApkSigner;
import com.android.apksig.ApkVerifier;

import java.io.File;
import java.io.FileInputStream;
import java.security.KeyStore;
import java.security.PrivateKey;
import java.security.cert.X509Certificate;
import java.util.Collections;
import java.util.List;

/** Signs an APK (v2 signature) with apksig, then verifies it. */
public class SignApk {
    public static void main(String[] args) throws Exception {
        if (args.length != 6) {
            System.err.println("usage: SignApk <in.apk> <out.apk> <keystore.p12> <alias> <password> <minSdk>");
            System.exit(2);
        }
        File in = new File(args[0]);
        File out = new File(args[1]);
        char[] pass = args[4].toCharArray();

        KeyStore ks = KeyStore.getInstance("PKCS12");
        try (FileInputStream fis = new FileInputStream(args[2])) {
            ks.load(fis, pass);
        }
        PrivateKey key = (PrivateKey) ks.getKey(args[3], pass);
        X509Certificate cert = (X509Certificate) ks.getCertificate(args[3]);
        List<X509Certificate> chain = Collections.singletonList(cert);

        ApkSigner.SignerConfig signer =
                new ApkSigner.SignerConfig.Builder("CERT", key, chain).build();
        new ApkSigner.Builder(Collections.singletonList(signer))
                .setInputApk(in)
                .setOutputApk(out)
                .setMinSdkVersion(Integer.parseInt(args[5]))
                .setV1SigningEnabled(false) // v2 is enough for Android 7.0+ (minSdk 24)
                .setV2SigningEnabled(true)
                .build()
                .sign();

        ApkVerifier.Result result = new ApkVerifier.Builder(out).build().verify();
        System.out.println("verified=" + result.isVerified()
                + " v1=" + result.isVerifiedUsingV1Scheme()
                + " v2=" + result.isVerifiedUsingV2Scheme());
        for (ApkVerifier.IssueWithParams e : result.getErrors()) {
            System.out.println("ERROR: " + e);
        }
        if (!result.isVerified()) System.exit(1);
    }
}
