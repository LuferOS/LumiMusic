sed -i 's/val intent = Intent(Intent.ACTION_SEND).apply {/shareApk(context)/g' app/src/main/java/com/example/ui/screens/ProfileScreen.kt
sed -i '/type = "text\/plain"/d' app/src/main/java/com/example/ui/screens/ProfileScreen.kt
sed -i '/putExtra(Intent.EXTRA_SUBJECT, "Check out this Music App!")/d' app/src/main/java/com/example/ui/screens/ProfileScreen.kt
sed -i '/putExtra(Intent.EXTRA_TEXT, "Hey! Download this awesome AMOLED music player. You can export the .APK directly from AI Studio -> Settings -> Export APK!")/d' app/src/main/java/com/example/ui/screens/ProfileScreen.kt
sed -i '/context.startActivity(Intent.createChooser(intent, "Share App"))/d' app/src/main/java/com/example/ui/screens/ProfileScreen.kt
sed -i '/}/d' app/src/main/java/com/example/ui/screens/ProfileScreen.kt
