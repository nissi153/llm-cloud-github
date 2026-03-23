package com.study.Ex16Security01.service;

import com.study.Ex16Security01.dto.MemberJoinDto;
import com.study.Ex16Security01.dto.MemberUpdateDto;
import com.study.Ex16Security01.entity.MemberEntity;
import com.study.Ex16Security01.entity.MemberRepo;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
@RequiredArgsConstructor
public class MemberService {
  private final PasswordEncoder passwordEncoder;
  private final MemberRepo memberRepo;

  //로그인 액션(loginAction)은 시큐리티가 직접 처리함.
  //회원가입 액션은 직접 처리해야 됨.
  public boolean joinAction(MemberJoinDto dto) {
    //비번을 암호화 한다.
    String encodedPassword = passwordEncoder.encode( dto.getPassword() );
    System.out.println( "rawPassword = " + dto.getPassword() );
    System.out.println("encodedPassword = " + encodedPassword);
    dto.setPassword( encodedPassword ); //암호화된 비번 설정!

    //DB에 저장한다.
    try {
      memberRepo.save(dto.toSaveEntity());
    }
    catch ( Exception e) {
      e.printStackTrace(); //예외 로그 출력
      return false;  //회원가입 실패
    }

    return true; //회원가입 성공
  }

  public MemberUpdateDto getDto(Long id) throws Exception {
    //DB id로 레코드 한개 반환
    Optional<MemberEntity> optional = memberRepo.findById( id );
    if(optional.isEmpty()) {
      throw new Exception("member id가 잘못됨.");
      //예외처리하는 방법 2가지
      //1. try catch문 : 내가 해결.
      //2. throws문 : 나를 호출한 주체에게 예외처리를 떠넘김.
    }
    MemberEntity entity = optional.get();
    return entity.toUpdateDto();
  }

  public boolean modifyAction(MemberUpdateDto dto){
    //Argument : 인자 - 함수호출할 때 넣는 변수나 값
    //parameter : 매개변수 - 함수선언부의 입력되는 변수
    try {
      memberRepo.save( dto.toUpdateEntity()  );
    }
    catch (Exception e){
      e.printStackTrace();
      return false;
    }

    return true;
  }

  public boolean deleteDTO(Long id){
    try {
      memberRepo.deleteById(id);
    }
    catch (Exception e){
      e.printStackTrace();
      return false;
    }
    return true;
  }

}//class

