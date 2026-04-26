package com.study.studentAdmin.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.RestTemplate;

// 브라우저 JS → Spring Boot /api/** → Python FastAPI localhost:8000
@RestController
@RequestMapping("/api/students")
public class StudentApiProxyController {

   // RestTemplate : RestAPI 통신해주는 클래스
    private final RestTemplate restTemplate = new RestTemplate();

    @Value("${python.server.url:http://localhost:8000}")
    private String pythonServerUrl;

//   반환값으로
//  return 클래스객체 --> JSON 바디
//  return ResponseEntity<클래스> ---> JSON 바디 + HTTP 응답코드 + 에러메시지

    // 전체 학생 조회
    @GetMapping
    public ResponseEntity<String> getStudents() {
        try {
            return restTemplate.getForEntity(pythonServerUrl + "/students", String.class);
        } catch (HttpClientErrorException e) {
            return ResponseEntity.status(e.getStatusCode()).body(e.getResponseBodyAsString());
        }
    }

    // 특정 학생 조회
    @GetMapping("/{id}")
    public ResponseEntity<String> getStudent(@PathVariable int id) {
        try {
            return restTemplate.getForEntity(pythonServerUrl + "/students/" + id, String.class);
        } catch (HttpClientErrorException e) {
            return ResponseEntity.status(e.getStatusCode()).body(e.getResponseBodyAsString());
        }
    }

    // 학생 등록
    @PostMapping
    public ResponseEntity<String> createStudent(@RequestBody String body) {
        try {
            HttpEntity<String> entity = jsonEntity(body);
            return restTemplate.postForEntity(pythonServerUrl + "/students", entity, String.class);
        } catch (HttpClientErrorException e) {
            return ResponseEntity.status(e.getStatusCode()).body(e.getResponseBodyAsString());
        }
    }

    // 학생 정보 전체 수정 (PUT)
    @PutMapping("/{id}")
    public ResponseEntity<String> updateStudent(@PathVariable int id, @RequestBody String body) {
        try {
            return restTemplate.exchange(
                pythonServerUrl + "/students/" + id,
                HttpMethod.PUT, jsonEntity(body), String.class
            );
        } catch (HttpClientErrorException e) {
            return ResponseEntity.status(e.getStatusCode()).body(e.getResponseBodyAsString());
        }
    }

    // 학생 정보 부분 수정 (PATCH)
    @PatchMapping("/{id}")
    public ResponseEntity<String> patchStudent(@PathVariable int id, @RequestBody String body) {
        try {
            return restTemplate.exchange(
                pythonServerUrl + "/students/" + id,
                HttpMethod.PATCH, jsonEntity(body), String.class
            );
        } catch (HttpClientErrorException e) {
            return ResponseEntity.status(e.getStatusCode()).body(e.getResponseBodyAsString());
        }
    }

    // 학생 삭제
    @DeleteMapping("/{id}")
    public ResponseEntity<String> deleteStudent(@PathVariable int id) {
        try {
            return restTemplate.exchange(
                pythonServerUrl + "/students/" + id,
                HttpMethod.DELETE, null, String.class
            );
        } catch (HttpClientErrorException e) {
            return ResponseEntity.status(e.getStatusCode()).body(e.getResponseBodyAsString());
        }
    }

    private HttpEntity<String> jsonEntity(String body) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        return new HttpEntity<>(body, headers);
    }
}
