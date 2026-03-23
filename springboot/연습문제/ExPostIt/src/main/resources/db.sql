USE mydb;

CREATE TABLE postit_notes (
                              id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                              x INT NOT NULL,
                              y INT NOT NULL,
                              content TEXT NOT NULL,
                              color VARCHAR(16) NOT NULL,
                              rotation DECIMAL(5,2) NOT NULL,
                              z_index INT NOT NULL DEFAULT 1,
                              created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                              updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO postit_notes (x, y, content, color, rotation, z_index)
VALUES
    ( 80, 120, '🎉 포스트잇 앱에 오신 것을 환영해요!\n\n드래그해서 옮겨보세요.', '#FFF176', -2.00, 1),
    (340, 180, '+ 버튼을 눌러 새 메모를 추가하세요!',                         '#B3E5FC',  1.50, 2),
    (590, 100, '✕ 버튼으로 메모를 삭제할 수 있어요.',                         '#F8BBD0', -1.00, 3);

SELECT * FROM postit_notes;

