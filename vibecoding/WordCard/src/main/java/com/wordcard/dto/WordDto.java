package com.wordcard.dto;

public record WordDto(
        Long id,
        String wordHtml,
        String pos,
        String posLabel,
        String phoneticHtml,
        String koHtml,
        String exampleHtml,
        String dateStr
) {}
