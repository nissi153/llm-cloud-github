package com.study.Ex16Security01;

import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class SecurityService implements UserDetailsService {
  @Override
  public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
    //사용자 아이디를 통해, 사용자 정보와 권한(ROLE)을 스프링 시큐리티에 전달해 주는 코드
    List<GrantedAuthority> authorityList = new ArrayList<>();
    //인가 리스트에 추가
    //테스트로 관리자 권한을 한개 추가해 준다.
    authorityList.add( new SimpleGrantedAuthority(UserRole.USER.getValue() ) );
    //권한과 함께 사용자 정보 객체를 반환한다.
    // username : 아이디 - "admin"
    // password  : 암호 - "1234"
    //Given that there is no default password encoder configured
    // password는 반드시 암호화해서 넘겨야 됨.
    // Bcrypt 사이트(bcrypt-generator.com)에서 암호를 생성해서 붙여넣는다.
    // $2a$10$zJKeTxzvmkLaFlxdLYueZup39TcOSJ8x1vYgtxsXdUUzg65kWHGoW
    System.out.println("시큐리티가 사용자 정보를 조회함.");
    return new User("admin", "$2a$10$zJKeTxzvmkLaFlxdLYueZup39TcOSJ8x1vYgtxsXdUUzg65kWHGoW", authorityList);
  }
}
