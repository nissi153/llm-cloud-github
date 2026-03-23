package com.study.Ex16Security01.service;

import com.study.Ex16Security01.entity.MemberEntity;
import com.study.Ex16Security01.entity.MemberRepo;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class SecurityService implements UserDetailsService {
  private final MemberRepo memberRepo;

  //시큐리티에서 로그인 액션에서 사용자의 정보를 가져오는 메소드.
  @Override
  public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
    //실제 DB에서 사용자 정보를 가져와서 시큐리티에 넘겨준다.
    Optional<MemberEntity> optional = memberRepo.findByUserNameJPQL( username );
    if( optional.isEmpty() ) {
      throw new UsernameNotFoundException("사용자를 찾을 수 없습니다.");
    }
    MemberEntity entity = optional.get();

    List<GrantedAuthority> authorityList = new ArrayList<>();
    authorityList.add( new SimpleGrantedAuthority( entity.getUser_role()  ) );
    System.out.println("시큐리티가 사용자 정보를 조회함." + entity.getUsername() );

    //hong/1234 로그인

    return new User(entity.getUsername(), entity.getPassword(), authorityList);
  }
}
