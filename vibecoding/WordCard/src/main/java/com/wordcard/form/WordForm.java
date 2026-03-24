package com.wordcard.form;

import jakarta.validation.constraints.NotBlank;
import lombok.Getter;
import lombok.Setter;

@Getter @Setter
public class WordForm {

    @NotBlank(message = "영어 단어는 필수입니다.")
    private String word;

    private String pos = "noun";

    private String phonetic;

    @NotBlank(message = "한국어 뜻은 필수입니다.")
    private String ko;

    private String example;
}
