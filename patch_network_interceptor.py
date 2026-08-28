with open('app/src/main/java/com/example/data/NetworkClient.kt', 'r') as f:
    content = f.read()

old_builder = """        OkHttpClient.Builder()
            .dispatcher(dispatcher)
            .connectionPool(ConnectionPool(64, 5, TimeUnit.MINUTES))
            .connectTimeout(8, TimeUnit.SECONDS)
            .readTimeout(8, TimeUnit.SECONDS)
            .writeTimeout(8, TimeUnit.SECONDS)
            .retryOnConnectionFailure(true)
            .cache(cache)
            .build()"""

new_builder = """        val cacheInterceptor = okhttp3.Interceptor { chain ->
            var request = chain.request()
            // Si hay internet, podemos cachear por unos minutos para consultas repetidas rápidas
            request = request.newBuilder().header("Cache-Control", "public, max-age=300").build()
            
            val response = chain.proceed(request)
            response.newBuilder()
                .header("Cache-Control", "public, max-age=300")
                .removeHeader("Pragma")
                .build()
        }

        OkHttpClient.Builder()
            .dispatcher(dispatcher)
            .connectionPool(ConnectionPool(64, 5, TimeUnit.MINUTES))
            .connectTimeout(8, TimeUnit.SECONDS)
            .readTimeout(8, TimeUnit.SECONDS)
            .writeTimeout(8, TimeUnit.SECONDS)
            .retryOnConnectionFailure(true)
            .addNetworkInterceptor(cacheInterceptor)
            .cache(cache)
            .build()"""

content = content.replace(old_builder, new_builder)

with open('app/src/main/java/com/example/data/NetworkClient.kt', 'w') as f:
    f.write(content)
