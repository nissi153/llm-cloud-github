package com.study.Ex13VMDB;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Controller
@RequiredArgsConstructor
public class HtmlController {
  private final ProductRepo productRepo;
  //생성자 주입 : final - 빈이 재주입(생성)되는 것을 막아준다.
  //                  : 생성자함수에서 가장 먼저 주입(생성)되므로, 우선순위가 높다.
//  public  HtmlController(ProductRepo productRepo){
//    System.out.println( productRepo );
//    this.productRepo = productRepo;
//  }

  @GetMapping("/")
  public String index() {
    return "redirect:/list";  //HTTP 응답 헤더에 Location에 URL을 보낸다.
  }                                        //웹브라우저가 받은 URL로 다시 요청한다.

  //Get방식 : 단순 페이지 이동/보안이 필요하지 않는 요청/a태그/location.href
  //           : 파라미터값이 주소줄에 노출됨.
  //Post방식 : 보안이 필요한 요청(로그인,회원가입,결제정보) - body data감춤.
  @GetMapping("/list")
  public String list(Model model) {
    List<Product> list = productRepo.findAll();
    model.addAttribute("list", list);
    //System.out.println(list.size());

    return "index";
  }

  @GetMapping("/addForm")
  public String addForm() {
    return "add";
  }

  //상품추가
  @PostMapping("/addAction")
  //HTTP요청의 데이터받기
  //1. @RequestParam로 하나씩 받기
  //2. @ModuleAttribute로 클래스/맵 매핑으로 받기(ORM)
  //3. @RequestBody로 body데이터를 String/클래스,맵 매핑, REST API
  public String addAction(@RequestParam String productName,
                          @RequestParam Integer productPrice,
                          @RequestParam LocalDate productLimitDate) {
    System.out.println("productName = " + productName +
        ", productPrice = " + productPrice +
        ", productLimitDate = " + productLimitDate);

    //DB에 저장하기, repo.save(e)
    Product entity = Product.builder()
        //.productNo(0)
        .productName(productName)
        .productPrice(productPrice)
        .productLimitDate(productLimitDate)
        .build();
    productRepo.save(entity);

    //리스트보여주기
    return "redirect:/list";
  }

  @GetMapping("/deleteAction")
  public String deleteAction(@RequestParam Integer productNo) {
    System.out.println("productNo = " + productNo);

    productRepo.deleteById(productNo);

    return "redirect:/list";
  }

  @GetMapping("/updateForm")
  public String updateForm(@RequestParam Integer productNo,
                           Model model) {
    System.out.println("productNo = " + productNo);

    //Optional : 널체크 용도
    Optional<Product> optional = productRepo.findById(productNo);

    if (optional.isPresent()) {
      Product product = optional.get();
      model.addAttribute("product", product);
    } else {
      System.out.println("ProdcutNo가 없습니다.");
      return "redirect:/list";
    }

    return "update";
  }

  @PostMapping("/updateAction")
  public String updateAction(
      @RequestParam Integer productNo,
      @RequestParam String productName,
      @RequestParam Integer productPrice,
      @RequestParam LocalDate productLimitDate) {

    //업데이트하려면, entity를 생성해야 됨.
    //1. new해서 새로 만들기 : 수정해야할 모든 정보를 가지고 있을때.
    //2. findById로 찾아오기 : 입력된 데이터가 부족할때 DB정보를 읽어야 됨.
    Product entity = Product.builder()
        .productNo(productNo) //DB 인덱스가 동일해야 업데이트가 됨.
        .productPrice(productPrice)
        .productName(productName)
        .productLimitDate(productLimitDate)
        .build();

    //DB에 수정내용 저장(repo.save(e))
    productRepo.save(entity);

    return "redirect:/list";
  }

}//class
