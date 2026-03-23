package com.study.Ex19AssoMapping;

import com.study.Ex19AssoMapping.entity.Board;
import com.study.Ex19AssoMapping.entity.Comment;
import com.study.Ex19AssoMapping.repository.BoardRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class DataInit implements CommandLineRunner {

    private final BoardRepository boardRepository;

    @Override
    public void run(String... args) {
        // 게시글 1 + 댓글
        Board b1 = Board.builder().title("JPA 공부").content("JPA 연관관계 매핑을 배워봅시다.").build();
        b1.getComments().add(Comment.builder().content("좋은 글이네요!").board(b1).build());
        b1.getComments().add(Comment.builder().content("잘 배워갑니다.").board(b1).build());
        b1.getComments().add(Comment.builder().content("감사합니다!").board(b1).build());

        // 게시글 2 + 댓글
        Board b2 = Board.builder().title("Spring Boot 시작").content("스프링 부트 프로젝트를 생성해봅시다.").build();
        b2.getComments().add(Comment.builder().content("따라해봤는데 잘 됩니다!").board(b2).build());
        b2.getComments().add(Comment.builder().content("초보자에게 좋은 글이에요.").board(b2).build());

        // 게시글 3 (댓글 없음)
        Board b3 = Board.builder().title("H2 데이터베이스").content("H2 인메모리 DB 사용법을 알아봅시다.").build();

        boardRepository.save(b1);
        boardRepository.save(b2);
        boardRepository.save(b3);
    }
}
