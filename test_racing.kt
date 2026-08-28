import kotlinx.coroutines.*
import kotlinx.coroutines.selects.select

fun main() = runBlocking {
    val result = select<String> {
        async { "A" }.onAwait { it }
        async { "B" }.onAwait { it }
    }
    println(result)
}
