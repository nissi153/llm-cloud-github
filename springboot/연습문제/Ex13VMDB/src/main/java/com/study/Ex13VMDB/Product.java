package com.study.Ex13VMDB;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

//CREATE TABLE vm2.product(
//    product_no INT AUTO_INCREMENT NOT NULL PRIMARY KEY, -- 고유키
//     product_name VARCHAR(255) NOT NULL, -- 상품이름
//    product_price INT NOT NULL, -- 상품가격
//    product_limit_date DATE DEFAULT (CURRENT_DATE) -- 유통가능일자
//);
@Entity
@Table(name = "product")
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder  //모든 필드를 가진 생성자함수 지원
public class Product {
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Integer productNo;
  private String productName;
  private Integer productPrice;
  private LocalDate productLimitDate;

  @Builder //일부 필드만 가진 생성자함수 지원
  public Product( String productName, Integer productPrice){
    this.productName = productName;
    this.productPrice = productPrice;
  }
}
