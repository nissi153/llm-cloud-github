package com.study.Ex18TDD;

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

//loginAction() 함수 테스트 한다?       1000개라면?  자동화한다면?
// 휴먼 1인이 필요
// 1. App 실행
// 2. Postman or JS 로 HTTP 요청한다.
// 3. 응답을 휴먼 Eye로 확인한다.

@RestController
@RequestMapping("/api/v1")
@RequiredArgsConstructor
public class ApiController {
  private final MemberService memberService;

  @PostMapping("/loginAction")
  public ResDto loginAction(@RequestBody ReqDto reqDto){

    MemberDto memberDto = MemberDto.builder()
        .loginId(reqDto.getLoginId())
        .loginPw(reqDto.getLoginPw())
        .build();

    int result = memberService.loginAction( memberDto ); // hong/1234
    ResDto resDto = null;
    if( result == 1 ){ //로그인 성공
      resDto = ResDto.builder()
          .status("ok")
          .message("로그인 성공!")
          .build();
    }else{ //로그인 실패
      resDto = ResDto.builder()
          .status("ok")
          .message("로그인 실패!")
          .build();
    }
    return resDto;
  }
}
