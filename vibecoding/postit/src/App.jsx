import { useState } from 'react';
import styles from './app.module.css';

const NOTE_COLORS = [
  { bg: '#fff9c4', header: '#fff176' },
  { bg: '#fce4ec', header: '#f48fb1' },
  { bg: '#e8f5e9', header: '#a5d6a7' },
  { bg: '#e3f2fd', header: '#90caf9' },
  { bg: '#ede7f6', header: '#ce93d8' },
  { bg: '#fff3e0', header: '#ffcc80' },
];

const STORAGE_KEY = 'postit-notes';

function loadNotes() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
  } catch {
    return [];
  }
}

function Note({ note, onDelete, onChange }) {
  const color = NOTE_COLORS[note.colorIdx];
  return (
    <div className={styles.card} style={{ background: color.bg }}>
      <div className={styles.cardHeader} style={{ background: color.header }}>
        <button className={styles.deleteBtn} onClick={() => onDelete(note.id)}>✕</button>
      </div>
      <div className={styles.cardBody}>
        <input
          className={styles.titleInput}
          placeholder="제목"
          value={note.title}
          onChange={(e) => onChange(note.id, 'title', e.target.value)}
        />
        <textarea
          className={styles.contentTextarea}
          placeholder="내용을 입력하세요..."
          value={note.content}
          onChange={(e) => onChange(note.id, 'content', e.target.value)}
        />
      </div>
    </div>
  );
}

export default function App() {
  const [notes, setNotes] = useState(loadNotes);

  function save(updated) {
    setNotes(updated);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
  }

  function addNote() {
    save([...notes, {
      id: Date.now().toString(),
      title: '',
      content: '',
      colorIdx: Math.floor(Math.random() * NOTE_COLORS.length),
    }]);
  }

  function deleteNote(id) {
    save(notes.filter((n) => n.id !== id));
  }

  function changeNote(id, field, value) {
    save(notes.map((n) => n.id === id ? { ...n, [field]: value } : n));
  }

  return (
    <div className={styles.app}>
      <div className={styles.header}>
        <h1 className={styles.title}>📌 포스트잇</h1>
        <button className={styles.addBtn} onClick={addNote}>＋ 추가</button>
      </div>
      <div className={styles.board}>
        {notes.length === 0
          ? <p className={styles.empty}>+ 버튼을 눌러 포스트잇을 추가해보세요!</p>
          : notes.map((note) => (
              <Note
                key={note.id}
                note={note}
                onDelete={deleteNote}
                onChange={changeNote}
              />
            ))
        }
      </div>
    </div>
  );
}
