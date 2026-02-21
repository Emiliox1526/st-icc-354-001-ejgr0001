# ====== Stage 1: build ======
FROM eclipse-temurin:21-jdk-jammy AS builder
LABEL authors="Emilio"

WORKDIR /app

# Herramientas + protoc (protobuf-compiler)
RUN apt-get update \
  && apt-get install -y --no-install-recommends curl unzip protobuf-compiler \
  && rm -rf /var/lib/apt/lists/*

COPY . .

# Descarga Gradle y construye directamente (sin wrapper)
ARG GRADLE_VERSION=8.7
RUN curl -fsSL https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip -o /tmp/gradle.zip \
  && unzip -q /tmp/gradle.zip -d /opt \
  && ln -s /opt/gradle-${GRADLE_VERSION}/bin/gradle /usr/local/bin/gradle

RUN gradle shadowJar --no-daemon

RUN set -eux; \
    JAR="$(ls -1 build/libs/*-all.jar 2>/dev/null | head -n 1 || true)"; \
    if [ -z "$JAR" ]; then JAR="$(ls -1 build/libs/*.jar | head -n 1)"; fi; \
    cp "$JAR" /app/app.jar


# ====== Stage 2: runtime ======
FROM eclipse-temurin:21-jre-jammy
LABEL authors="Emilio"

WORKDIR /app
ENV APP_PORT=7070

RUN mkdir -p /app/logs
VOLUME ["/app/logs"]

COPY --from=builder /app/app.jar /app/app.jar

EXPOSE 7070
ENTRYPOINT ["sh", "-c", "java -jar /app/app.jar --port=${APP_PORT} >> /app/logs/app.log 2>&1"]
