with open('app/src/main/java/com/example/data/NetworkClient.kt', 'r') as f:
    content = f.read()

old_builder = """        OkHttpClient.Builder()
            .dispatcher(dispatcher)
            .connectionPool(ConnectionPool(64, 5, TimeUnit.MINUTES))
            .connectTimeout(8, TimeUnit.SECONDS)
            .readTimeout(8, TimeUnit.SECONDS)
            .writeTimeout(8, TimeUnit.SECONDS)
            .retryOnConnectionFailure(true)
            .build()"""

new_builder = """        val cacheSize = 50L * 1024L * 1024L // 50 MB
        val cacheDir = java.io.File(System.getProperty("java.io.tmpdir") ?: "/tmp", "http_cache")
        val cache = okhttp3.Cache(cacheDir, cacheSize)

        OkHttpClient.Builder()
            .dispatcher(dispatcher)
            .connectionPool(ConnectionPool(64, 5, TimeUnit.MINUTES))
            .connectTimeout(8, TimeUnit.SECONDS)
            .readTimeout(8, TimeUnit.SECONDS)
            .writeTimeout(8, TimeUnit.SECONDS)
            .retryOnConnectionFailure(true)
            .cache(cache)
            .build()"""

content = content.replace(old_builder, new_builder)

with open('app/src/main/java/com/example/data/NetworkClient.kt', 'w') as f:
    f.write(content)
