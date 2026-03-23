package com.study.Ex19AssoMapping.controller;

import com.study.Ex19AssoMapping.repository.BoardRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
@RequiredArgsConstructor
public class BoardController {

    private final BoardRepository boardRepository;

    @GetMapping("/")
    public String list(Model model) {
        model.addAttribute("boards", boardRepository.findAll());
        return "boards";
    }
}
