tail -n +380 app/src/main/java/com/example/MainActivity.kt > app/src/main/java/com/example/ui/screens/MainScreen.kt
sed -i '380,$d' app/src/main/java/com/example/MainActivity.kt
