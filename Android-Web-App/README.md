# Convert any website into android app

This is a template project for Android Studio that allows you to create an android webview application in minutes. You can use it to create a simple app for your website or as a starting point for your HTML5 based android app.

## [Output](https://github.com/imvickykumar999/Convert_Any_website_into_android_app/blob/master/app/src/main/java/com/example/mahbu/convertanywebsiteintoandroidapp/MainActivity.java)...

[![ss](https://github.com/imvickykumar999/Convert_Any_website_into_android_app/blob/master/WhatsApp%20Image%202021-04-13%20at%2019.47.35.jpeg?raw=true)](https://github.com/imvickykumar999/Convert_Any_website_into_android_app/blob/master/app/src/main/AndroidManifest.xml)

Getting started
Download or clone this repository and import it into Android Studio.

Using a remote source
If you want to create an app that displays the contents of a remote website

uncomment lines 30 and 31 in MainActivity.java and replace http://example.com with your remote source

mWebView.loadUrl("http://example.com");
mWebView.setWebViewClient(new MyWebViewClient());
open the MyWebViewClient.java file and replace example.com on line 12 with your custom hostname

if (Uri.parse(url).getHost().endsWith("example.com")) {
Using a local source
If you want to create a local HTML5 android app

uncomment line 34 in MainActivity.java

mWebView.loadUrl("file:///android_asset/index.html");
put all your files (including your index.html) in the assets directory
