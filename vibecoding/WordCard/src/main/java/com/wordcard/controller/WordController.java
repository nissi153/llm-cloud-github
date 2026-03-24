package com.wordcard.controller;

import com.wordcard.form.WordForm;
import com.wordcard.service.WordService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
@RequiredArgsConstructor
public class WordController {

    private final WordService wordService;

    @GetMapping("/")
    public String index(
            @RequestParam(required = false, defaultValue = "") String q,
            @RequestParam(required = false, defaultValue = "newest") String sort,
            Model model) {

        var words = wordService.searchAndSort(q, sort);
        model.addAttribute("words", words);
        model.addAttribute("q", q);
        model.addAttribute("sort", sort);
        model.addAttribute("resultCount", words.size());
        model.addAttribute("totalCount", wordService.totalCount());
        return "index";
    }

    @PostMapping("/words")
    public String addWord(@Valid @ModelAttribute WordForm form) {
        wordService.save(form);
        return "redirect:/";
    }
}
