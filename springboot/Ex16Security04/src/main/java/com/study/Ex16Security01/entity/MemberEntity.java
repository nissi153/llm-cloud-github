package com.study.Ex16Security01.entity;

import com.study.Ex16Security01.dto.MemberUpdateDto;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@Entity
@Table(name = "member_security")
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder //전체 필드를 가진 생성자 빌더 패턴
public class MemberEntity {
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;
  private String username;
  private String password;
  private String nick_name;
  private String user_role;
  //@DateTimeFormat : HTML폼에서 전송된 날짜 문자열을
  //    Java 날짜 객체로 변환하는 어노테이션
  //   ORM(Object Relation Mapping) : JPA에서 자바 객체와 DB테이블간의 매핑
  //   매핑(Mapping) : HTML폼 문자열과 Java 객체 간의 변환
  // 그런데 엔티티를 HTML폼 매핑에 직접 사용하지 않는다. DTO사용하는게 좋다.
  // 엔티티 객체를 잘못 사용하면, 테이블에 직접 Write될 여지가 있음.
  // @Transaction 서비스 클래스에서 setter함수 사용시 바로 DB에 적용됨.
  // @DateTimeFormat(pattern = "yyyy-MM-dd")
  private LocalDate join_date;

  public MemberUpdateDto toUpdateDto(){
    return MemberUpdateDto.builder()
        .id(id)
        .username(username)
        .password(password)
        .nick_name(nick_name)
        .user_role(user_role)
        .join_date(join_date)
        .build();
  }

  //@Builder //일부 필드만 가진 생성자 빌더 패턴
  //public MemberEntity(Long id, ...){
  //}
}
