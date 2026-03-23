package com.study.Ex16Security01;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.csrf.CookieCsrfTokenRepository;
import org.springframework.security.web.servlet.util.matcher.PathPatternRequestMatcher;

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
        .csrf( (auth) -> auth
            .csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse())
        )

        //HTTP 요청에 대한 보안을 설정한다. Security 6버전.
        .authorizeHttpRequests( (auth) -> auth
                .requestMatchers("/loginForm").permitAll()
                //.requestMatchers("/").authenticated()
                .requestMatchers("/").permitAll()
                .anyRequest().authenticated()
              )

        //로그인 페이지 설정
        .formLogin( (formLogin) -> formLogin
                .loginPage("/loginForm")
                .loginProcessingUrl("/loginAction")
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
        .logout( (auth) -> auth
            .logoutRequestMatcher(  // 스프링부트 4.x 업데이트 된 클래스함수
                PathPatternRequestMatcher.withDefaults().matcher(HttpMethod.GET, "/logoutAction")
            )
            .logoutSuccessUrl("/")
            .invalidateHttpSession(true) //세션 객체 해제
            .deleteCookies("JSESSIONID")  //쿠키 삭제
        );

    return http.build();
  }
}
