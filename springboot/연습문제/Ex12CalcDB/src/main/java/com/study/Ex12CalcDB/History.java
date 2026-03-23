package com.study.Ex12CalcDB;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

/*
CREATE TABLE calc.history(
   history_no INT AUTO_INCREMENT PRIMARY KEY, -- 고유키
   op VARCHAR(255) NOT NULL, -- 연산자 add, sub, mul, div
   input1 INT NOT NULL, -- 입력값1
   input2 INT NOT NULL, -- 입력값2
   result INT NOT NULL -- 연산결과
);
 */
@Entity
@Table(name = "history")
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder  //빌더 패턴에서는 모든 필드를 가진 생성자함수가 필요하다.
public class History {
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Integer history_no;
  private String op;
  private Integer input1;
  private Integer input2;
  private Integer result;

  //DTO to Entity
  public History toEntity(){
    return null;
  }
}
