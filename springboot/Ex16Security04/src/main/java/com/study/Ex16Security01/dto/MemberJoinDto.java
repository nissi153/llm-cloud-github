package com.study.Ex16Security01.dto;

import com.study.Ex16Security01.entity.MemberEntity;
import lombok.*;
import org.springframework.format.annotation.DateTimeFormat;

import java.time.LocalDate;

@Getter
@Setter
//Java 컴파일러에서는 자동생성하나, 스피링 빈 생성시에는 자동생성하지 않음.
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class MemberJoinDto {   //  DTO  <-> Entity
  private Long id;
  private String username;
  private String password;
  private String nick_name;
  private String user_role;
  @DateTimeFormat(pattern = "yyyy-MM-dd")
  private LocalDate join_date;

  public MemberEntity toSaveEntity(){
    //빌더패턴 왜 사용? 생성자함수를 편하게 쓰고자
    // 1.  new MemberEntity(id, username, ....) : 매개변수와 갯수와 순서가 정확해야.
    // 2. MemberEntity.builder().id(id).username(username).build() :
    //        매개변수 갯수와 순서에서 자유롭게 사용가능.
    return MemberEntity.builder()
        .username(username)
        .password(password)
        .nick_name(nick_name)
        .user_role(user_role)
        .join_date(join_date)
        .build();
  }

  public MemberEntity toUpdateEntity(){
    return MemberEntity.builder()
        .id(id)
        .username(username)
        .password(password)
        .nick_name(nick_name)
        .user_role(user_role)
        .join_date(join_date)
        .build();
  }
}//class
