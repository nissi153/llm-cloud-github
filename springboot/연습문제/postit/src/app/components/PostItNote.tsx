import React, { useState, useRef, useCallback } from "react";
import styles from "./PostItNote.module.css";

export interface Note {
  id: string;
  x: number;
  y: number;
  content: string;
  color: string;
  rotation: number;
}

interface PostItNoteProps {
  note: Note;
  onDelete: (id: string) => void;
  onUpdate: (id: string, content: string) => void;
  onMove: (id: string, x: number, y: number) => void;
  onBringToFront: (id: string) => void;
  zIndex: number;
}

export function PostItNote({
  note,
  onDelete,
  onUpdate,
  onMove,
  onBringToFront,
  zIndex,
}: PostItNoteProps) {
  const [isDragging, setIsDragging] = useState(false);
  const dragOffset = useRef({ x: 0, y: 0 });
  const noteRef = useRef<HTMLDivElement>(null);

  const handleMouseDown = useCallback(
    (e: React.MouseEvent) => {
      if ((e.target as HTMLElement).tagName === "TEXTAREA") return;
      if ((e.target as HTMLElement).closest(`.${styles.deleteBtn}`)) return;

      e.preventDefault();
      onBringToFront(note.id);
      setIsDragging(true);

      dragOffset.current = {
        x: e.clientX - note.x,
        y: e.clientY - note.y,
      };

      const handleMouseMove = (moveEvent: MouseEvent) => {
        onMove(
          note.id,
          moveEvent.clientX - dragOffset.current.x,
          moveEvent.clientY - dragOffset.current.y
        );
      };

      const handleMouseUp = () => {
        setIsDragging(false);
        window.removeEventListener("mousemove", handleMouseMove);
        window.removeEventListener("mouseup", handleMouseUp);
      };

      window.addEventListener("mousemove", handleMouseMove);
      window.addEventListener("mouseup", handleMouseUp);
    },
    [note.id, note.x, note.y, onBringToFront, onMove]
  );

  return (
    <div
      ref={noteRef}
      className={`${styles.note} ${isDragging ? styles.dragging : ""}`}
      style={{
        left: note.x,
        top: note.y,
        backgroundColor: note.color,
        transform: `rotate(${note.rotation}deg)`,
        zIndex,
      }}
      onMouseDown={handleMouseDown}
    >
      <div className={styles.header}>
        <div className={styles.lines}>
          <span /><span /><span />
        </div>
        <button
          className={styles.deleteBtn}
          onClick={() => onDelete(note.id)}
          title="삭제"
        >
          ✕
        </button>
      </div>
      <textarea
        className={styles.textarea}
        value={note.content}
        onChange={(e) => onUpdate(note.id, e.target.value)}
        placeholder="메모를 입력하세요..."
        spellCheck={false}
      />
    </div>
  );
}
