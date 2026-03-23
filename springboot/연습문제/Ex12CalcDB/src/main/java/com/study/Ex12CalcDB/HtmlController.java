package com.study.Ex12CalcDB;

import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

//Controller는 HTTP요청에 대해서 1차적인 처리
//1. ViewController : @Controller - html파일을 반환
//2. RestController : @ResponseBody - 문자열(JSON) 반환

// 프론트엔드 html에서 서버에 값을 전달하기 위한 통신 방법 3가지
//1. Form 태그 : GET, POST만 가능, submit 버튼을 통해
//2. Form 태그 + JS Form객체의 submit()함수
//3. JS fetch함수(Axios()함수)

//DB를 접근하기 위해서 JPA를 사용하는데, 필요한 클래스들
//1. Entity : 테이블과 1:1로 매칭
//2. Repository : Entity를 제어하는 JPA 함수들 제공
//3. DTO : 요청, 응답에 맞는 데이터 전달용 클래스, 하나의 엔티티에
//            필요에 따라 여러개 있을 수 있다.
//4. Sevice : 로직(코드)를 분리하여 재사용한다.

@Controller
@RequiredArgsConstructor  //생성자 주입 패턴
public class HtmlController {
  @Autowired
  private final HistoryRepo historyRepo;

  @GetMapping("/")
  public String index(){
    return "index";  //index.html을 내려준다.
  }
  @GetMapping("/calc-submit")
  //http요청 파라미터/바디데이터를 가져오는 어노테이션은?
  //1. @RequestParam : 주로 Get방식
  //2. @RequestBody : 주로 Post, Put, Delete방식
  //    -> 클래스나 Map으로 매핑(ORM)으로 받으면 편하다.
  //        @ModelAttribute
  // * html의 name속성과 변수이름이 동일해야 매핑이 된다.
  public String calcSubmit(@RequestParam Integer num1,
                           @RequestParam Integer num2,
                           @RequestParam String calType,
                           Model model){
    //soutp
    //num1 = 10, num2 = 3, calType = add
    System.out.println("num1 = " + num1 + ", num2 = " + num2 + ", calType = " + calType);

    model.addAttribute("num1", num1);
    model.addAttribute("num2", num2);
    Integer result = 0;
    if( calType.equals("add")){
      result =  num1 + num2;
    }
    model.addAttribute("result", result);

    //히스토리 테이블에 저장한다.
    //레파지토리 인터페이스의 save(e)함수를 사용한다.
    History enity = History.builder()
        .input1(num1)
        .input2(num2)
        .result(result)
        .op(calType)
        .build();
    historyRepo.save( enity );

    return "index"; //index.html을 응답한다.
  }
}
