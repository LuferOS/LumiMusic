package com.example.utils

data class LrcLine(
    val timeMs: Long,
    val text: String
)

object LrcParser {
    fun parse(lrc: String): List<LrcLine> {
        val lines = mutableListOf<LrcLine>()
        val regex = Regex("""\[(\d{2}):(\d{2})\.(\d{2,3})](.*)""")
        
        lrc.lines().forEach { line ->
            val match = regex.find(line)
            if (match != null) {
                val min = match.groupValues[1].toLong()
                val sec = match.groupValues[2].toLong()
                var ms = match.groupValues[3].toLong()
                if (match.groupValues[3].length == 2) ms *= 10 // Convert hundreths to ms
                
                val timeMs = (min * 60 * 1000) + (sec * 1000) + ms
                val text = match.groupValues[4].trim()
                
                if (text.isNotEmpty()) {
                    lines.add(LrcLine(timeMs, text))
                }
            }
        }
        return lines.sortedBy { it.timeMs }
    }
}
