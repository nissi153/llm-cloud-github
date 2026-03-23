package com.study.Ex18TDD;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

//@BootstrapWith : ApplicationContext(빈 관리) 초기화 방법 결정
//@ExtendWith : JUnit5와 Spring을 연결해주는 역할
// @SpringBootTest : 테스트에서 전체 앱 컨텍스트 로드해 주는 핵심 어노테이션
@SpringBootTest
class Ex18TddApplicationTests {

	//@Test : 단위 테스트 케이스임을 알려주는 어노테이션
	@Test
	void contextLoads() {
		// contextLoads함수 : Application Context가 정상 로드되었음을 알림.
		System.out.println("테스트 준비 완료!");
	}
}
