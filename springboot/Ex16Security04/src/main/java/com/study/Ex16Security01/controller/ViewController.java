package com.study.Ex16Security01.controller;

import com.study.Ex16Security01.entity.MemberEntity;
import com.study.Ex16Security01.entity.MemberRepo;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.List;

@Controller
@RequiredArgsConstructor
public class ViewController {
  private final MemberRepo memberRepo;

  @GetMapping("/")
  //@ResponseBody
  public String index() {
    return "index";
  }

  @GetMapping("/admin")
  public String adminPage(Model model){
    model.addAttribute("listCount", memberRepo.count());

    List<MemberEntity> list = memberRepo.findAll();
    model.addAttribute("list", list);

    return "admin";
  }

}//class
