package com.study.ExPostIt;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "postit_notes")
@Getter
//@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Postit {
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;
  private Integer x;
  private Integer y;
  private String content;
  private String color;
  private BigDecimal rotation;
  private Integer z_index;
  @CreationTimestamp
  private LocalDateTime created_at;
  @UpdateTimestamp
  private LocalDateTime updated_at;

  public void updateInfo(Integer x,  //save()함수 호출할 필요 없음.
                         Integer y,
                         String content) {
    this.x = x;
    this.y = y;
    this.content = content;
  }

  public PostitResDto toDto() {
    return PostitResDto.builder()
        .id(this.getId())
        .x(this.getX())
        .y(this.getY())
        .color(this.getColor())
        .content(this.getContent())
        .rotation(this.getRotation())
        .created_at(this.getCreated_at())
        .updated_at(this.getUpdated_at())
        .build();
  }

}
