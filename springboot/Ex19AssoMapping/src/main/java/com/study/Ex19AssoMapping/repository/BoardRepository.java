package com.study.Ex19AssoMapping.repository;

import com.study.Ex19AssoMapping.entity.Board;
import org.springframework.data.jpa.repository.JpaRepository;

public interface BoardRepository extends JpaRepository<Board, Long> {
}
