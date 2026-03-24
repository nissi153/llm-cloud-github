package com.study.Ex19AssoMapping;

import jakarta.persistence.*;
import lombok.*;

import java.util.ArrayList;
import java.util.List;

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

  //mappedBy = "board" : 연관관계 주인은 내가 아니다. comment엔티티가 주인이다.
  //cascade : Board에 일어나는 일이 Comment에도 전파되도록 한다.
  //               게시글이 지워지면, 댓글도 지워진다.
  //orphanRemoval : 부모(Board)와 관계가 끊어지면, 자식(Comment) 자동 삭제됨.
  @OneToMany(mappedBy = "board", cascade = CascadeType.ALL,
        orphanRemoval = true)
  @Builder.Default
  //빌더패턴을 사용할때, comments가 null이 아니고 빈리스트를 유지하도록 해줌.
  private List<Comment> comments = new ArrayList<>();
}
