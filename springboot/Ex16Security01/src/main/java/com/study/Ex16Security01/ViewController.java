package com.study.Ex16Security01;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class ViewController {
  @GetMapping("/")
  @ResponseBody
  public String index() {
    return "스프링부트 시큐리티 웹앱입니다.";
  }

  //인증되지 않는 사용자여도, 로그인,회원가입페이지로 접근 가능해야
  @GetMapping("/loginForm")
  public String loginForm(){
    return "loginForm";
  }

}
