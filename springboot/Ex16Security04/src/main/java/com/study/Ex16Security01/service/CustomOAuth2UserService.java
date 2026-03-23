package com.study.Ex16Security01.service;

import com.study.Ex16Security01.entity.SnsUser;
import com.study.Ex16Security01.entity.SnsUserRepo;
import jakarta.servlet.http.HttpSession;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.oauth2.client.userinfo.DefaultOAuth2UserService;
import org.springframework.security.oauth2.client.userinfo.OAuth2UserRequest;
import org.springframework.security.oauth2.client.userinfo.OAuth2UserService;
import org.springframework.security.oauth2.core.OAuth2AuthenticationException;
import org.springframework.security.oauth2.core.user.DefaultOAuth2User;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.stereotype.Service;

import java.util.Collections;

@RequiredArgsConstructor
@Service // @Component - 클래스를 스프린 객체(빈)으로 자동 등록한다.
public class CustomOAuth2UserService
    implements OAuth2UserService<OAuth2UserRequest, OAuth2User> {
  private final HttpSession httpSession; //세션 주입
  private final SnsUserRepo snsUserRepo; //DB저장용 Repo

  @Override
  public OAuth2User loadUser(OAuth2UserRequest userRequest)
                                    throws OAuth2AuthenticationException {
    OAuth2UserService delegate = new DefaultOAuth2UserService();
    OAuth2User oAuth2User = delegate.loadUser(userRequest);

    //registrationId : Google, Kakao, Naver, Github, Apple
    String registrationId = userRequest.getClientRegistration().getRegistrationId();
    String userNameAttributeName = userRequest.getClientRegistration().getProviderDetails()
        .getUserInfoEndpoint().getUserNameAttributeName();

    OAuthAttributes attributes =
        OAuthAttributes.of(registrationId, userNameAttributeName,
            oAuth2User.getAttributes());

    SnsUser user = saveOrUpdate(attributes);
    // 데이터 수명주기
    // model, request : 요청시 -> 응답(Response)때까지, 리다이렉트하면 데이터 사라짐.
    // session : 로그인부터 로그아웃까지( 로그인 아이디, 로그인 여부, 필수정보...저장용도)
    // application : 웹브라우저 닫을 때까지
    httpSession.setAttribute("user", new SessionUser(user));

    return new DefaultOAuth2User(
        Collections.singleton(new SimpleGrantedAuthority(user.getRoleKey())),
        attributes.getAttributes(),
        attributes.getNameAttributeKey()  );
  }
  private SnsUser saveOrUpdate(OAuthAttributes attributes){
    //구글,카카오,네이버... 공통적으로 이메일을 계정으로 사용한다.
    SnsUser snsUser = snsUserRepo.findByEmail(attributes.getEmail())
        .map(entity -> entity.update(attributes.getName(), attributes.getPicture()))
        .orElse(attributes.toEntity());

    return snsUserRepo.save( snsUser );
  }

}//class
