# 1단계: 빌드 (JDK 17 사용)
FROM eclipse-temurin:17-jdk AS build
WORKDIR /app

# Gradle 빌드에 필요한 파일 복사
COPY gradlew .
COPY gradle gradle
COPY build.gradle .
COPY settings.gradle .
COPY src src

# gradlew 스크립트 대신 Gradle Wrapper JAR 직접 실행 (Windows CRLF/BOM 문제 회피)
RUN java -classpath gradle/wrapper/gradle-wrapper.jar org.gradle.wrapper.GradleWrapperMain build -x test --no-daemon

# 2단계: 실행 (JRE 17 사용, 경량 이미지)
FROM eclipse-temurin:17-jre
WORKDIR /app

# 빌드된 JAR 파일 복사
COPY --from=build /app/build/libs/*.jar app.jar

# Railway가 주입하는 PORT 환경변수 사용
ENV PORT=8080
EXPOSE ${PORT}

# 애플리케이션 실행
ENTRYPOINT java -jar -Dserver.port=${PORT} app.jar
