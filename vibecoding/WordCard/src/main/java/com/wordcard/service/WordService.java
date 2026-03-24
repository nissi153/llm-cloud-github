package com.wordcard.service;

import com.wordcard.dto.WordDto;
import com.wordcard.entity.Word;
import com.wordcard.form.WordForm;
import com.wordcard.repository.WordRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.web.util.HtmlUtils;

import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.regex.Pattern;

@Service
@RequiredArgsConstructor
public class WordService {

    private static final DateTimeFormatter DATE_FMT = DateTimeFormatter.ofPattern("yyyy. M. d.");

    private final WordRepository wordRepository;

    public List<WordDto> searchAndSort(String q, String sortType) {
        Sort sort = "alpha".equals(sortType)
                ? Sort.by(Sort.Direction.ASC, "word")
                : Sort.by(Sort.Direction.DESC, "createdAt");

        List<Word> words = (q != null && !q.isBlank())
                ? wordRepository.searchByQuery("%" + q.trim().toLowerCase() + "%", sort)
                : wordRepository.findAll(sort);

        return words.stream()
                .map(w -> toDto(w, q))
                .toList();
    }

    public long totalCount() {
        return wordRepository.count();
    }

    public void save(WordForm form) {
        Word word = Word.builder()
                .word(form.getWord().trim())
                .pos(form.getPos())
                .phonetic(form.getPhonetic() != null ? form.getPhonetic().trim() : null)
                .ko(form.getKo().trim())
                .example(form.getExample() != null ? form.getExample().trim() : null)
                .build();
        wordRepository.save(word);
    }

    private WordDto toDto(Word w, String q) {
        return new WordDto(
                w.getId(),
                highlight(w.getWord(), q),
                w.getPos(),
                posLabel(w.getPos()),
                highlight(w.getPhonetic(), q),
                highlight(w.getKo(), q),
                highlight(w.getExample(), q),
                w.getCreatedAt() != null ? w.getCreatedAt().format(DATE_FMT) : ""
        );
    }

    private String highlight(String text, String query) {
        if (text == null || text.isBlank()) return "";
        String escaped = HtmlUtils.htmlEscape(text);
        if (query == null || query.isBlank()) return escaped;
        String escapedQuery = Pattern.quote(HtmlUtils.htmlEscape(query.trim()));
        return escaped.replaceAll("(?i)(" + escapedQuery + ")", "<mark>$1</mark>");
    }

    private String posLabel(String pos) {
        if (pos == null) return "";
        return switch (pos) {
            case "noun" -> "n.";
            case "verb" -> "v.";
            case "adj"  -> "adj.";
            case "adv"  -> "adv.";
            default     -> "etc.";
        };
    }
}
