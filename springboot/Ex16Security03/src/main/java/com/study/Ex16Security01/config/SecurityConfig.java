package com.study.Ex16Security01.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.CsrfConfigurer;
import org.springframework.security.config.annotation.web.configurers.FormLoginConfigurer;
import org.springframework.security.config.annotation.web.configurers.LogoutConfigurer;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.csrf.CookieCsrfTokenRepository;

//시큐리티 관련 설정 클래스
@Configuration  //환경설정 클래스로 등록한다.
@EnableWebSecurity  //웹 보안 활성화 어노테이션
public class SecurityConfig {
  @Bean  //메소드 반환객체를 빈으로 등록한다.
  SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http
        //csrf 보안 설정을 비활성화(개발편의시)
        //.csrf( (auth) -> auth.disable())
        //csrf 활성화(기본)
        // CSRF 보안 방식 2가지
        //1. HttpSession 방식(기본) : 서버에 인증정보 저장한다.
        //2. CookieToken 방식 : JS 기반 앱 제작시 쿠키에 CsrfToken저장해야 됨.

        // CSRF 설정  : 람다매개변수 타입은 생략 가능함. 타입 추정으로.
        .csrf(  ( CsrfConfigurer<HttpSecurity> csrf) -> csrf
            .csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse())
        )

        //경로별  인가(역할) 설정
        // authz : Authorization(인가), authn : Authentication(인증)
        // AuthorizationManagerRequestMatcherRegistry 타입이다.
        .authorizeHttpRequests( (authz) -> authz
                .requestMatchers("/", "/loginForm", "/joinForm", "/joinAction").permitAll()
                .requestMatchers("/admin").hasRole("ADMIN") //403 Forbidden
                //.requestMatchers("/admin").hasAuthority("ROLE_ADMIN")
                .anyRequest().authenticated()
              )

        //로그인 페이지/액션 설정
        .formLogin( ( FormLoginConfigurer<HttpSecurity> login) -> login
                .loginPage("/loginForm")
                .loginProcessingUrl("/loginAction") //시큐리티가 자동처리
                .defaultSuccessUrl("/")
                //로그인 성공 커스텀 핸들러
                .successHandler( (request, response, auth) -> {
                  System.out.println("로그인 성공했습니다.");
                  response.sendRedirect("/");
                } )
                //로그인 실패 에러페이지
                .failureUrl("/loginForm?error")
                .permitAll()
            )
        // 로그아웃 URL/세션 설정
        .logout( (LogoutConfigurer<HttpSecurity> logout) -> logout
            .logoutUrl("/logoutAction") //Post방식 추천(보안)
            .logoutSuccessUrl("/")
            .invalidateHttpSession(true) //세션 객체 해제
            .deleteCookies("JSESSIONID")  //쿠키 삭제
        );

    return http.build();
  }

  //시큐리티 기본 암호화 객체
  //BCrypt 암호화 엔코더
  @Bean
  public PasswordEncoder passwordEncoder(){
    //스프링 시큐리티 6.4.x에서 공식 지원하는 PasswordEncoder 구현 클래스들
    //Bcrypt, Argon2, Pbkdf2, SCrypt
    //암호화 강도는 4 ~ 31까지 지정 가능. (몇번 섞는가?) 기본강도는 10이다.
    return new BCryptPasswordEncoder( 10 );
//    return Argon2PasswordEncoder.defaultsForSpringSecurity_v5_8();
 //   return Pbkdf2PasswordEncoder.defaultsForSpringSecurity_v5_8();
  //  return SCryptPasswordEncoder.defaultsForSpringSecurity_v5_8();
  //  return new BcryptPassword4jPasswordEncoder( );
    // password4j 외부 라이브러리를 이용한다. 공식이 아니므로 비추천. 시큐리티 7에 추가.
  }

}//class
