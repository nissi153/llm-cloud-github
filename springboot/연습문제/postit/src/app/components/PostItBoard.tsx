import React, { useState, useCallback, useRef } from "react";
import { PostItNote, Note } from "./PostItNote";
import styles from "./PostItBoard.module.css";

const NOTE_COLORS = [
  "#FFF176", // 노란
  "#F8BBD0", // 핑크
  "#B3E5FC", // 하늘
  "#C8E6C9", // 연두
  "#FFE0B2", // 주황
  "#E1BEE7", // 보라
];

function generateId() {
  return Math.random().toString(36).slice(2, 9);
}

const INITIAL_NOTES: Note[] = [
  {
    id: generateId(),
    x: 80,
    y: 120,
    content: "🎉 포스트잇 앱에 오신 것을 환영해요!\n\n드래그해서 옮겨보세요.",
    color: NOTE_COLORS[0],
    rotation: -2,
  },
  {
    id: generateId(),
    x: 340,
    y: 180,
    content: "+ 버튼을 눌러 새 메모를 추가하세요!",
    color: NOTE_COLORS[2],
    rotation: 1.5,
  },
  {
    id: generateId(),
    x: 590,
    y: 100,
    content: "✕ 버튼으로 메모를 삭제할 수 있어요.",
    color: NOTE_COLORS[1],
    rotation: -1,
  },
];

export function PostItBoard() {
  const [notes, setNotes] = useState<Note[]>(INITIAL_NOTES);
  const [zOrders, setZOrders] = useState<string[]>(
    INITIAL_NOTES.map((n) => n.id)
  );
  const boardRef = useRef<HTMLDivElement>(null);
  const colorIndexRef = useRef(3);

  const addNote = useCallback(() => {
    const board = boardRef.current;
    const rect = board?.getBoundingClientRect();
    const bw = rect?.width ?? 800;
    const bh = rect?.height ?? 600;

    const x = Math.random() * (bw - 240) + 40;
    const y = Math.random() * (bh - 260) + 60;
    const rotation = (Math.random() - 0.5) * 6;
    const color = NOTE_COLORS[colorIndexRef.current % NOTE_COLORS.length];
    colorIndexRef.current += 1;

    const newNote: Note = {
      id: generateId(),
      x,
      y,
      content: "",
      color,
      rotation,
    };

    setNotes((prev) => [...prev, newNote]);
    setZOrders((prev) => [...prev, newNote.id]);
  }, []);

  const deleteNote = useCallback((id: string) => {
    setNotes((prev) => prev.filter((n) => n.id !== id));
    setZOrders((prev) => prev.filter((z) => z !== id));
  }, []);

  const updateNote = useCallback((id: string, content: string) => {
    setNotes((prev) =>
      prev.map((n) => (n.id === id ? { ...n, content } : n))
    );
  }, []);

  const moveNote = useCallback((id: string, x: number, y: number) => {
    setNotes((prev) =>
      prev.map((n) => (n.id === id ? { ...n, x, y } : n))
    );
  }, []);

  const bringToFront = useCallback((id: string) => {
    setZOrders((prev) => [...prev.filter((z) => z !== id), id]);
  }, []);

  return (
    <div className={styles.wrapper}>
      {/* 헤더 */}
      <header className={styles.header}>
        <div className={styles.logo}>
          <span className={styles.logoIcon}>📝</span>
          <span className={styles.logoText}>Post-it</span>
        </div>
        <div className={styles.info}>
          메모 {notes.length}개
        </div>
        <button className={styles.addBtn} onClick={addNote} title="메모 추가">
          <span>+</span>
          <span className={styles.addBtnLabel}>새 메모</span>
        </button>
      </header>

      {/* 보드 */}
      <div className={styles.board} ref={boardRef}>
        {/* 격자 배경 */}
        <div className={styles.gridBg} />

        {notes.length === 0 && (
          <div className={styles.empty}>
            <p>📋</p>
            <p>메모가 없습니다</p>
            <p>상단의 <strong>+ 새 메모</strong> 버튼을 눌러보세요!</p>
          </div>
        )}

        {notes.map((note) => (
          <PostItNote
            key={note.id}
            note={note}
            onDelete={deleteNote}
            onUpdate={updateNote}
            onMove={moveNote}
            onBringToFront={bringToFront}
            zIndex={zOrders.indexOf(note.id) + 1}
          />
        ))}
      </div>
    </div>
  );
}
