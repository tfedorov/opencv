/*
 * This file was generated by the Gradle 'init' task.
 *
 * This is a general purpose Gradle build.
 * To learn more about Gradle by exploring our Samples at https://docs.gradle.org/8.7/samples
 * This project uses @Incubating APIs which are subject to change.
 */

plugins {
	scala
	id("idea")
	application
}

repositories {
	mavenCentral()
}

dependencies {
	implementation("org.scala-lang:scala-library:2.12.17")
	//implementation("org.openpnp:opencv:4.5.3-4")
	implementation("org.openpnp:opencv:4.9.0-0")

}
application {
	mainClass = "com.tfedorov.CameraApp" // Change this to your main class

	applicationDefaultJvmArgs += listOf(
		"-Djava.library.path=/opt/brew/Cellar/opencv/4.9.0_7/share/java/opencv4/"
	)
}
