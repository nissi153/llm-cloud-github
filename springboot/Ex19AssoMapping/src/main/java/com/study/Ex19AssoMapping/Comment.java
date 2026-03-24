package com.study.Ex19AssoMapping;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Getter @Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Comment {
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;
  private String content;

//  private Long board_id; //게시글의 id - 외래키(FK)

  // LAZY(느린, 지연) : board 객체를 필요할 때(get)때 가져온다.
  //                 Board엔티티가 준비되고 나서 가져와야 됨.
  // EAGER(열렬, 즉시) : comment엔티티 생성시 가져온다.
  @ManyToOne(fetch = FetchType.LAZY)
  // board_id라는 FK컬럼을 만든다.
  @JoinColumn(name = "board_id")
  private Board board; //Board엔티티의 객체를 매핑해 준다.
}
// 댓글을 조회하려면, 게시글의 id를 fk필드로 가진 레코드들을 검색했다.
// Select * from comment where board_id = 3;
