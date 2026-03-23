package com.study.ExPostIt;

import org.springframework.data.jpa.repository.JpaRepository;

public interface PostitRepo extends JpaRepository<Postit, Long> {
  //  기본함수 지원 (CRUD)
}
