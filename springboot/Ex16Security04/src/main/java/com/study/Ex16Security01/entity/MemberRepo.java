package com.study.Ex16Security01.entity;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.Optional;

public interface MemberRepo extends JpaRepository<MemberEntity, Long> {
  //기본함수 지원  - findAll(), findById(id), save(e), deleteById(id), count()
  //유저 정의 함수는 별도 기입
  //@Query를 이용하여, SQL을 직접 사용하기 : JPQL, Native Query(Select문)

  //JPQL을 이용한 사용자 정의함수
  @Query(value = "select m from MemberEntity m where m.username=:username_param")
  Optional<MemberEntity> findByUserNameJPQL(@Param("username_param") String username);

  //Native Query을 이용한 사용자 정의함수
  @Query(value = "select * from member_security m where m.username = :username_param",
      nativeQuery = true)
  Optional<MemberEntity> findByUserName(@Param("username_param") String username);
}
