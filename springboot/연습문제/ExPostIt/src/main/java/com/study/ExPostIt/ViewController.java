package com.study.ExPostIt;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.List;

@Controller
@RequiredArgsConstructor
public class ViewController {
  private final PostitRepo postitRepo;

  @GetMapping("/")
  public String index(){
    return "redirect:/list";
  }

  @GetMapping("/list")
  public String list(Model model){
    List<Postit> list = postitRepo.findAll();

    for( Postit postit : list ) {
      System.out.println( postit.getContent() );
    }
    model.addAttribute("list", list);
    return "PostIt";
  }

}
