package com.study.Ex18TDD;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.web.context.WebApplicationContext;
import org.springframework.web.filter.CharacterEncodingFilter;
import tools.jackson.databind.ObjectMapper;

import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.verify;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

//@WebMvcTest           vs  @SpringBootTest
// 컨트롤러 레이어만 로딩        전체 애플리케이션 로딩
// 가볍고 빠른 테스트              무겁고 느림
// 단위 테스트                         통합테스트 용도
@WebMvcTest(ApiController.class)
class ApiControllerTest {
  //1. 가상(Mock)의 HTTP 요청을 만들어서 테스트한다.
  //2. 응답 결과를 확인한다.
  @Autowired
  MockMvc mockMvc; //가상의 HTTP요청 생성
  @MockitoBean
  MemberService memberService; //ApiController에서 주입받은 Bean객체를
                                                           //Mock형태로 객체 생성해줌.

  @Autowired                                //전체 설정 정보를 담고있는 객체
  WebApplicationContext ctx;   //ApplicationContext vs WebAppContext
                                                       //스프링 컨테이너             스프링 컨테이너
                                                       //                               + HTTP 요청/응답 처리
  @BeforeEach //각 테스트 케이스마다 한번씩 호출
  public void setup(){
    this.mockMvc = MockMvcBuilders.webAppContextSetup(ctx)
        .addFilter(new CharacterEncodingFilter("UTF-8", true))
        .alwaysDo(print()) //로그를 남긴다.
        .build();
  }
  @Test
  void loginAction() throws Exception {
    //BDD : Behavior Driven Development 행동주도개발
    // given(상태가 주어지고), when(어떤 조건일때), then(어떤 상태를 기대한다)
    // given, when : loginAction함수가 동작하는 조건을 기술한다.
    given(memberService.loginAction(new MemberDto("hong", "1234")))
        .willReturn(1); //로그인 성공 1
    // then
    // 기대하는 응답 DTO 객체 생성
    ResDto resDto = ResDto.builder()
        .status("ok")
        .message("로그인 성공")
        .build();
    MemberDto dto = MemberDto.builder()
        .loginId("hong")
        .loginPw("1234")
        .build();

    //HTTP요청을 날리고 테스트한다.
    mockMvc.perform(post("/api/v1/loginAction")
        //Jackson Lib를 사용하여, 객체의 내용을 문자열로 바꾼다.(직렬화/역직렬화)
        .content(new ObjectMapper().writeValueAsString(dto))
        .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isOk())  //응답코드 200
        .andExpect(jsonPath("$.status").value("ok"))
        .andExpect(jsonPath("$.message").exists())
        .andDo(print());

    //verify : 해당 객체의 메소드가 실행되었는지를 체크해 줌.
    verify(memberService).loginAction(new MemberDto("hong", "1234"));
  }
}//class