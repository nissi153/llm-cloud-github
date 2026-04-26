package com.study.studentAdmin.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class StudentPageController {

    // Thymeleaf 관리자 페이지 렌더링
    @GetMapping("/")
    public String index() {
        return "index";
    }
}
