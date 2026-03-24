package com.wordcard.repository;

import com.wordcard.entity.Word;
import org.springframework.data.domain.Sort;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface WordRepository extends JpaRepository<Word, Long> {

    @Query("""
            SELECT w FROM Word w
            WHERE LOWER(w.word)     LIKE :q
               OR LOWER(w.ko)       LIKE :q
               OR LOWER(w.example)  LIKE :q
               OR LOWER(w.phonetic) LIKE :q
            """)
    List<Word> searchByQuery(@Param("q") String q, Sort sort);
}
