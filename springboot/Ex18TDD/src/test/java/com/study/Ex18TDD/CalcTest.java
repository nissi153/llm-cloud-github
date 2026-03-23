package com.study.Ex18TDD;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class CalcTest {
  static Calc calc = null;

  @BeforeAll  //테스트 케이스 실행전에 한번 호출됨.
  static void init(){
    System.out.println("init() 실행됨");
    calc = new Calc();
  }

  @Test
  //@DisplayName : 테스트 메소드 이름 변경
  @DisplayName("add 함수 테스트")
  void add() {
    assertEquals( 12, calc.add(10, 2) );
  }

  @Test
  void sub() {
    assertEquals( 8, calc.sub(10, 2) );
  }

  @Test
  void mul() {
    assertEquals( 20, calc.mul(10, 2) );
  }

  @Test
  void div() {
    assertEquals( 5, calc.div(10, 2) );
  }
}