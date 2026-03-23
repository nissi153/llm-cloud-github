package com.study.Ex16Security01;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;

//시큐리티 관련 설정 클래스
@Configuration  //환경설정 클래스로 등록한다.
@EnableWebSecurity  //웹 보안 활성화 어노테이션
public class SecurityConfig {
  @Bean  //메소드 반환객체를 빈으로 등록한다.
  SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http  //HTTP 요청에 대한 보안을 설정한다. Security 6버전.
        .authorizeHttpRequests( (auth) -> auth
               // permitAll() : 모두에게 허용
               // authenticate() : 인증된 사용자에게 허용
               // hasRole("ADMIN") : ADMIN 권한을 가진 사용자에게 허용
                .requestMatchers("/loginForm").permitAll()
                .requestMatchers("/").authenticated()
                // 그외의 경로 요청( /mypage, /admin )에 대해서
               //  인증된 사용자에게만 허용한다.
                .anyRequest().authenticated()
              )
        //로그인 페이지 설정
        .formLogin( (formLogin) -> formLogin
                .loginPage("/loginForm")  //로그인 폼 요청 URL
                // loginAction에 대한 인증처리는 시큐리티가 다 한다. 코드필요없다.
                .loginProcessingUrl("/loginAction") //로그인 액션 요청 URL
                .defaultSuccessUrl("/") //로그인 성공시 리다이렉트 URL
                .permitAll() //모두에게 허용
            );
    return http.build();
  }
}
