
plugins {
    application
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.eclipse.jetty:jetty-server:11.0.11")
}

application {
    mainClass.set("demo.App")
}

tasks.register<Copy>("copyModelResources") {
    from(File("${rootDir}/../mnist/saved_model").absolutePath)
    into(layout.buildDirectory.dir("${buildDir}/classes/java/main/resources/model"))
}

tasks.register<Copy>("copyUIResources") {
    from(File("${rootDir}/../todo/build").absolutePath)
    into(layout.buildDirectory.dir("${buildDir}/classes/java/main/resources/ui"))
}

tasks.jar {
    dependsOn("copyModelResources")
    dependsOn("copyUIResources")
    manifest.attributes["Main-Class"] = "demo.App"
    val dependencies = configurations
            .runtimeClasspath
            .get()
            .map(::zipTree)
    from(dependencies)
    duplicatesStrategy = DuplicatesStrategy.EXCLUDE
}

tasks.withType<AbstractArchiveTask>().configureEach {
    isPreserveFileTimestamps = false
    isReproducibleFileOrder = true
}
