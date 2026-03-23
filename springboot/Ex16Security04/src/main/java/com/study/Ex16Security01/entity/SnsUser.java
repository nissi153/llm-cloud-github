package com.study.Ex16Security01.entity;

import com.study.Ex16Security01.enumeration.UserRole;
import jakarta.persistence.*;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "sns_user")
@Getter
@NoArgsConstructor
public class SnsUser {
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;
  //@Column : DB필드에 대한 제약조건
  @Column(nullable = false)  //NOT NULL 속성
  private String name; // 닉네임(별명)
  @Column(nullable = false)
  private String email;
  @Column(nullable = false)
  private String picture; //프로필 이미지 URL
  @Enumerated(EnumType.STRING)
  @Column(name = "user_role", nullable = false)
  private UserRole role;
  //날짜는 DB자동생성되므로 생략

  @Builder //일부 필드만 가진 생성자 빌더 패턴
  public SnsUser(String name, String email,
                 String picture, UserRole role){
      this.name = name;
      this.email = email;
      this.picture = picture;
      this.role = role;
  }
  public SnsUser update(String name, String picture) {
      this.name = name;
      this.picture = picture;
      return this;
  }
  public String getRoleKey(){
    return this.role.getValue(); //"ROLE_USER" or "ROLE_ADMIN"
  }

}




