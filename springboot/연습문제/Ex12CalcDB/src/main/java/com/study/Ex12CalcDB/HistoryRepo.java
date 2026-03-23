package com.study.Ex12CalcDB;

import org.springframework.data.jpa.repository.JpaRepository;

public interface HistoryRepo extends JpaRepository<History, Integer> {
  //기본함수 : findAll, findById, save, delete, count
  //사용자정의함수는 별도로 추가한다.
}
