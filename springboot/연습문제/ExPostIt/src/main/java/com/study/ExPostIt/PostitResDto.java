package com.study.ExPostIt;

import lombok.*;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class PostitResDto {
  private Long id;
  private Integer x;
  private Integer y;
  private String content;
  private String color;
  private BigDecimal rotation;
  private Integer z_index;
  private LocalDateTime created_at;
  private LocalDateTime updated_at;

  public PostitResDto(Postit e) {
    this.id = e.getId();
    this.x = e.getX();
    this.y = e.getY();
    this.content = e.getContent();
    this.color = e.getColor();
    this.rotation = e.getRotation();
    this.z_index = e.getZ_index();
  }
}
