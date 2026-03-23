package com.study.ExPostIt;

import lombok.RequiredArgsConstructor;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController  //@Controller + @ResponseBody
@RequestMapping("/api")
@RequiredArgsConstructor
public class ApiController {
  private final PostitRepo postitRepo;

  @GetMapping("/list")
  public List<PostitResDto> list(Model model) {
    List<Postit> list = postitRepo.findAll();

    List<PostitResDto> dtoList = list.stream()
        .map(PostitResDto::new)  //DTO 생성자로 매핑한다.
        .toList(); //java 16버전이상에서 지원.

    return dtoList;
  }

  @PostMapping("/update")
  public PostitResDto update( @RequestParam Long id,
                    @RequestParam Integer x,
                     @RequestParam Integer y,
                     @RequestParam String content) {
    Optional<Postit> optional = postitRepo.findById( id );

    if( !optional.isPresent() )
      return null;

    Postit entity = optional.get();
    //@Transaction안에서는 save함수 없이도 저장됨.
    entity.updateInfo(x, y, content);

    Postit newEntity =  postitRepo.save( entity );

    PostitResDto resDto = newEntity.toDto();
    return resDto;
  }


  @PostMapping("/add") //빈 노트 생성
  public PostitResDto add(@RequestBody PostitReqDto dto) {

    Postit entity = Postit.builder()
        //.id()
        .x(dto.getX())
        .y(dto.getY())
        .color(dto.getColor())
        .content("")
        .z_index(dto.getZ_index())
        .rotation(dto.getRotation())
        .build();

    Postit newEntity = postitRepo.save(entity);

    PostitResDto resDto = newEntity.toDto();

    return resDto;
  }

  @GetMapping("/delete")
  public void delete(Long id) {
    postitRepo.deleteById(id);
  }

}//class
