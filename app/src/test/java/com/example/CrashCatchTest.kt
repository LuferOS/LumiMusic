package com.example

import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.Robolectric
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config
import org.junit.Ignore

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
class CrashCatchTest {
    @Ignore("MediaController binding in Robolectric throws NPE due to Media3 internals")
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
