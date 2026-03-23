package com.study.Ex13VMDB;

import org.springframework.data.jpa.repository.JpaRepository;

public interface ProductRepo extends JpaRepository<Product, Integer> {
  //1. Jpa기본함수가 SQL을 자동발생시킨다.
  //  findAll, findById, count, save, delete
  //2. 사용자 정의 함수 :  find by orderby 필드이름 desc/asc and/or 조합해서 사용
  //3. SQL 직접 사용
  //   1) JPQL  2) native SQL
}
