package com.study.Ex16Security01.dto;

import com.study.Ex16Security01.entity.MemberEntity;
import lombok.*;
import org.springframework.format.annotation.DateTimeFormat;

import java.time.LocalDate;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class MemberUpdateDto {   //  DTO  <-> Entity
  private Long id;
  private String username;
  private String password;
  private String nick_name;
  private String user_role;
  @DateTimeFormat(pattern = "yyyy-MM-dd")
  private LocalDate join_date;

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
