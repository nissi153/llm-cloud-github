package com.study.Ex16Security01.service;

import com.study.Ex16Security01.entity.SnsUser;
import lombok.Getter;

import java.io.Serializable;

// Serializable : 직렬화 할수있는
// 직렬화 : 객체는 바이트(Byte)로 바꿔서 스트림(물줄기)로 보낼때,
//               파일/네트워크/DB에 보낼때
// 역직렬화(Deserialization) : 파일(..)-> Bytes -> 객체
@Getter
public class SessionUser implements Serializable {
  private  String name;
  private String email;
  private String picture;

  public SessionUser(SnsUser user){
    this.name = user.getName();
    this.email = user.getEmail();
    this.picture = user.getPicture();
  }

}
