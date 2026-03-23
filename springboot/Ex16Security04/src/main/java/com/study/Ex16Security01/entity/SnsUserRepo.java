package com.study.Ex16Security01.entity;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface SnsUserRepo extends JpaRepository< SnsUser, Long  > {
   //기본함수 :  findAll, findById, save, deleteById, count
  //사용자정의함수 : 열이름 + And or where by asc desc limit 조합
  // * SNS 로그인으로 반환되는 값 중에서 email을 통해
  //    이미 회원가입된 사용자인지, 처음 가입한 사용자인지 구분하는 쿼리 메소드
  Optional<SnsUser> findByEmail(String email);

  //@Query : Native Query, JPQL
}
