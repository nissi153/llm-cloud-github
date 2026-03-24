package com.study.Ex19AssoMapping;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.*;

@Entity
@Getter @Setter
@NoArgsConstructor  //기본생성자 - 스프링빈생성(Jackson Lib)오류
@AllArgsConstructor
@Builder
public class Board {
  @Id
  // IDENTITY 옵션 : mysql, h2 DB사용시
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;
  private String title;
  private String content;
}
