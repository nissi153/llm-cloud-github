package com.study.ExPostIt;

import lombok.*;

import java.math.BigDecimal;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class PostitReqDto {
  private Long id;
  private Integer x;
  private Integer y;
  private String content;
  private String color;
  private BigDecimal rotation;
  private Integer z_index;

  public PostitReqDto(Postit e) {
    this.id = e.getId();
    this.x = e.getX();
    this.y = e.getY();
    this.content = e.getContent();
    this.color = e.getColor();
    this.rotation = e.getRotation();
    this.z_index = e.getZ_index();
  }
}
