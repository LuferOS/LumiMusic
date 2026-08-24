package com.example

import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
class CrashCatchTest {
    @Test
    fun testMainActivityLaunches() {
        try {
            val controller = Robolectric.buildActivity(MainActivity::class.java).create().start().resume().visible()
            println("Activity started successfully!")
        } catch (e: Exception) {
            e.printStackTrace()
            throw e
        }
    }
}
