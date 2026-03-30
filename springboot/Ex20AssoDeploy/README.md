# Ex20AssoDeploy

Spring Boot JPA 연관 매핑 프로젝트 - Railway 배포용

## 기술 스택

- Java 17
- Spring Boot 3.4.4
- Spring Data JPA
- Thymeleaf
- MySQL (배포) / H2 (로컬)
- Lombok

## 프로젝트 구조 (배포 관련 파일)

| 파일 | 설명 |
|------|------|
| `build.gradle` | MySQL 의존성 추가 (`com.mysql:mysql-connector-j`) |
| `Dockerfile` | Java 17 기반 멀티스테이지 빌드 (빌드: `eclipse-temurin:17-jdk`, 실행: `eclipse-temurin:17-jre`) |
| `railway.toml` | Railway 배포 설정 (Dockerfile 빌더 사용) |
| `src/main/resources/application.properties` | 로컬 개발용 설정 (H2 인메모리 DB) |
| `src/main/resources/application-prod.properties` | Railway 배포용 설정 (MySQL 연결) |

## 로컬 실행

```bash
./gradlew bootRun
```

- H2 인메모리 DB 사용
- H2 콘솔: http://localhost:8080/h2console

## Railway 배포 방법

### 1. Railway 프로젝트 생성

- [Railway](https://railway.app)에서 새 프로젝트 생성
- GitHub 레포 연결

### 2. MySQL 서비스 추가

- Railway 대시보드에서 **+ New** → **Database** → **MySQL** 추가
- MySQL 서비스가 자동으로 다음 환경변수를 생성함:
  - `MYSQLHOST`
  - `MYSQLPORT`
  - `MYSQLDATABASE`
  - `MYSQLUSER`
  - `MYSQLPASSWORD`

### 3. 환경변수 연결

- 앱 서비스의 **Variables** 탭에서 MySQL 서비스의 Reference Variables를 추가
- `application-prod.properties`에서 이 환경변수를 자동으로 참조함
- prod 프로필 활성화가 필요하면 **Variables** 탭에서 `SPRING_PROFILES_ACTIVE=prod`를 환경변수로 추가

### 4. 배포

- GitHub에 push하면 Railway가 자동으로 Dockerfile 기반 빌드 및 배포 수행
