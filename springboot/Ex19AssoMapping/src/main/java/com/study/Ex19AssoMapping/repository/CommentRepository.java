package com.study.Ex19AssoMapping.repository;

import com.study.Ex19AssoMapping.entity.Comment;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CommentRepository extends JpaRepository<Comment, Long> {
}
