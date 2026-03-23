package com.study.Ex16Security01.controller;

import com.study.Ex16Security01.dto.MemberJoinDto;
import com.study.Ex16Security01.dto.MemberUpdateDto;
import com.study.Ex16Security01.service.MemberService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

// 프론트 -> HTTP요청 -> Controller -> Service(로직처리) -> DTO
//    -> Repo -> Enitity -> DBMS
// DBMS -> Entity -> Repo -> Sevice -> DTO -> Controller
 //                   ->(View Resolver) html 선택 -> 타임리프 -> html 응답
// JS(React)  -> DTO -> JSON문자열(시리얼라이즈) -> HTTP BODY응답

// 회원(로그인, 회원가입) 요청에 대한 처리
@Controller
@RequiredArgsConstructor
public class MemberController {
  private final MemberService memberService;

  @GetMapping("/loginForm")
  public String loginForm(){
    return "loginForm";
  }
  @GetMapping("/joinForm")
  public String joinForm(){
    return "joinForm2";
  }
  //컨트롤러가 HTTP 데이터를 받는 방법
  // @RequestParam - GET방식(주소줄 KV), POST방식(BODY에)
  //   데이터 형식: application/x-www-form-urlencoded
  //   데이터 모양: name=hong&age=20
  //  주로 Form태그에서 보낼때
  // @RequsetBody - GET방식(못보냄), POST방식(BODY에)
  //  형식: application/json
  //  모양: { "name" : "hong", "age" : 20 }
  //  JS(리액트)에서 보낼  때, REST API SERVER에서 받을 떄
  // @ModelAttribute - 클래스와 맵과 매핑(바인딩)해주는 어노테이션
  //  ORM : Enitity와 DB 테이블과 매핑할 때
  // @DateTimeFormat - 데이터 바인딩
  // @PathVariable : 경로에 있는 문구를 변수로 변환하는 것.
  //     localhost:8080/api/post/{id}
  //     getPost(@PathVariable("id") Long postId)
  @PostMapping("/joinAction")
  @ResponseBody
  public String joinAction(@ModelAttribute MemberJoinDto dto){
     //dto에 데이터 바인딩이 되었는가 검증필요.
     System.out.println(dto.getUsername());
      //회원가입 로직 처리
      boolean isSuccess = memberService.joinAction( dto );
      if( isSuccess ) {
        //회원가입 성공후 어디로? 메인화면 또는 로그인화면
        return "<script>alert('회원가입 성공'); location.href='/loginForm';</script>";
      }else{
        return "<script>alert('회원가입 실패'); history.back();</script>";
      }
  }
  // HTTP 요청시 데이터 받는 법
  //1. @RequestParm
  //2. @RequestBody
  //3. @ModelAttribue : 클래스나 맵에 매핑
  // 응답할 때
  //1. return "html파일이름"  타임리프나 JSP 동적 HTML(뷰템플릿)
  //2. @ReponseBody : 문자열이나 JS, JSON, XML 문자열로 반환
  @GetMapping("/viewDTO")
  public String viewDTO(@RequestParam Long id,
                        Model model) throws Exception{
    //타임리프html에 데이터 넘길 때, 쓰는 객체
    //1. Model   2. Request   3. session X 4. application X
    //Model : 순수하게 뷰템플릿에 데이터 넘겨줄 때만
    //Request : Model기능 + HTTP요청에 대한 정보(헤더,바디)를 다 가짐.
    //Session : 로그인했을때 -> 로그아웃까지의 데이터(기억)를 가짐.
    //                예) 저장해야할 정보? 로그인 아이디/
    //                      전체앱에서 필요한 정보(프로필이미지,아이디,로그인여부...)
    //Applicaton : 웹브라우저 닫을때까지 정보 보관. 전체 앱에 사용할때
    //사용자 PC에 로컬에 저장
    //1. 쿠키 : Key-Value의 고전적인 방식
    //2. localstorage : Key-Value의 현대적 방식
    MemberUpdateDto dto = memberService.getDto( id );
    model.addAttribute("member", dto);

    return "modifyForm"; //수정폼에는 데이터가 들어가 있어야 편하다.
  }

  //1. @ModelAttribue : 파라미터 갯수가 많을 때 편하다.
  //2. @RequestParam
  //3. @RequestBody
  @PostMapping("/modifyAction")
  @ResponseBody
  public String modifyAction(@ModelAttribute MemberUpdateDto dto){
    System.out.println(dto.getUsername());

    //반환값  1. 불린 성공여부만 2. 정수 : 여러상태를 알기위해
    boolean isOk = memberService.modifyAction( dto );

    if( isOk ){
      return "<script>alert('회원정보 수정성공');  location.href='/admin'; </script>";
    }else {
      //history.back() : 유저가 입력한 정보가 유실되지 않는다.
      return "<script>alert('회원정보 수정실패');  history.back(); </script>";
    }
  }

  @GetMapping("/deleteDTO")
  @ResponseBody
  public String deleteDTO(@RequestParam Long id){

    boolean isOk = memberService.deleteDTO( id );
    if( isOk ){
      return "<script>alert('회원정보 삭제성공'); location.href='/admin';</script>";
    }else {
      return "<script>alert('회원정보 삭제실패'); histroy.back();</script>";
    }
  }

}//class
